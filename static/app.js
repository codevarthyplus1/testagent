// Global state
let currentCustomer = null;
let currentTab = 'chat';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Check if user is logged in
    checkLoginStatus();

    // Set up event listeners
    setupEventListeners();

    // Load initial data
    loadCategories();
    loadProducts();
}

function setupEventListeners() {
    // Login/Logout
    document.getElementById('login-btn').addEventListener('click', login);
    document.getElementById('logout-btn').addEventListener('click', logout);
    document.getElementById('customer-id-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') login();
    });

    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });

    // Chat
    document.getElementById('send-btn').addEventListener('click', sendQuestion);
    document.getElementById('question-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendQuestion();
    });

    // Quick questions
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('question-input').value = this.textContent;
            sendQuestion();
        });
    });

    // Products
    document.getElementById('category-filter').addEventListener('change', filterProducts);
    document.getElementById('search-btn').addEventListener('click', searchProducts);
    document.getElementById('product-search').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') searchProducts();
    });

    // Orders
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            loadOrders(this.dataset.status);
        });
    });
}

function switchTab(tab) {
    currentTab = tab;

    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tab) {
            btn.classList.add('active');
        }
    });

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tab}-tab`).classList.add('active');

    // Load tab-specific data
    if (tab === 'orders' && currentCustomer) {
        loadOrderSummary();
        loadOrders();
    } else if (tab === 'account' && currentCustomer) {
        loadAccountInfo();
    } else if (tab === 'products') {
        loadProducts();
    }
}

async function checkLoginStatus() {
    try {
        const response = await fetch('/api/customer');
        const data = await response.json();

        if (data.logged_in) {
            currentCustomer = data.customer;
            updateLoginUI(true);
        } else {
            currentCustomer = null;
            updateLoginUI(false);
        }
    } catch (error) {
        console.error('Error checking login status:', error);
    }
}

async function login() {
    const customerId = document.getElementById('customer-id-input').value.trim();

    if (!customerId) {
        alert('Please enter a Customer ID');
        return;
    }

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ customer_id: customerId })
        });

        const data = await response.json();

        if (data.success) {
            currentCustomer = data.customer;
            updateLoginUI(true);
            addChatMessage(`Welcome back, ${data.customer.name}! You are now logged in.`, 'assistant');
            document.getElementById('customer-id-input').value = '';
        } else {
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed. Please try again.');
    }
}

async function logout() {
    try {
        await fetch('/api/logout', {
            method: 'POST'
        });

        currentCustomer = null;
        updateLoginUI(false);
        addChatMessage('You have been logged out.', 'assistant');
    } catch (error) {
        console.error('Logout error:', error);
    }
}

function updateLoginUI(loggedIn) {
    const loginSection = document.getElementById('login-section');
    const userInfo = document.getElementById('user-info');
    const userName = document.getElementById('user-name');

    if (loggedIn && currentCustomer) {
        loginSection.classList.add('hidden');
        userInfo.classList.remove('hidden');
        userName.textContent = `${currentCustomer.name} (${currentCustomer.id})`;
    } else {
        loginSection.classList.remove('hidden');
        userInfo.classList.add('hidden');
    }
}

async function sendQuestion() {
    const input = document.getElementById('question-input');
    const question = input.value.trim();

    if (!question) return;

    // Add user message to chat
    addChatMessage(question, 'user');
    input.value = '';

    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (data.success) {
            addChatMessage(data.answer, 'assistant');
        } else {
            addChatMessage('Sorry, there was an error processing your question.', 'assistant');
        }
    } catch (error) {
        console.error('Error sending question:', error);
        addChatMessage('Sorry, there was an error. Please try again.', 'assistant');
    }
}

function addChatMessage(text, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Convert newlines to <br> and preserve formatting
    const formattedText = text.replace(/\n/g, '<br>');
    contentDiv.innerHTML = formattedText;

    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const data = await response.json();

        if (data.success) {
            const select = document.getElementById('category-filter');
            data.categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function loadProducts(category = '', search = '') {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = '<p class="loading">Loading products...</p>';

    try {
        let url = '/api/products';
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (search) params.append('search', search);
        if (params.toString()) url += '?' + params.toString();

        const response = await fetch(url);
        const data = await response.json();

        if (data.success) {
            displayProducts(data.products);
        }
    } catch (error) {
        console.error('Error loading products:', error);
        grid.innerHTML = '<p class="error-message">Error loading products</p>';
    }
}

function displayProducts(products) {
    const grid = document.getElementById('products-grid');

    if (products.length === 0) {
        grid.innerHTML = '<p class="info-message">No products found</p>';
        return;
    }

    grid.innerHTML = products.slice(0, 50).map(product => `
        <div class="product-card">
            <span class="product-category">${product.category}</span>
            <h3>${product.name}</h3>
            <div class="product-brand">${product.brand}</div>
            <div class="product-price">$${product.price.toFixed(2)}</div>
            <div class="product-rating">⭐ ${product.rating}/5.0</div>
            <div class="product-stock ${product.stock > 0 ? 'in-stock' : 'out-of-stock'}">
                ${product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
            </div>
            <p class="product-description">${product.description}</p>
        </div>
    `).join('');

    if (products.length > 50) {
        grid.innerHTML += '<p class="info-message">Showing first 50 products</p>';
    }
}

function filterProducts() {
    const category = document.getElementById('category-filter').value;
    loadProducts(category);
}

function searchProducts() {
    const search = document.getElementById('product-search').value;
    loadProducts('', search);
}

async function loadOrderSummary() {
    try {
        const response = await fetch('/api/order-summary');
        const data = await response.json();

        if (data.success) {
            const summary = data.summary;
            const summaryDiv = document.getElementById('order-summary');

            summaryDiv.innerHTML = `
                <h3>Order Summary</h3>
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-label">Total Orders</div>
                        <div class="stat-value">${summary.total_orders || 0}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Pending</div>
                        <div class="stat-value">${summary.pending || 0}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Processing</div>
                        <div class="stat-value">${summary.processing || 0}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Shipped</div>
                        <div class="stat-value">${summary.shipped || 0}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Delivered</div>
                        <div class="stat-value">${summary.delivered || 0}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Total Spent</div>
                        <div class="stat-value">$${(summary.total_spent || 0).toFixed(2)}</div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading order summary:', error);
    }
}

async function loadOrders(status = '') {
    if (!currentCustomer) {
        document.getElementById('orders-list').innerHTML = '<p class="info-message">Please login to view your orders.</p>';
        return;
    }

    const ordersList = document.getElementById('orders-list');
    ordersList.innerHTML = '<p class="loading">Loading orders...</p>';

    try {
        let url = '/api/orders';
        if (status) url += `?status=${status}`;

        const response = await fetch(url);
        const data = await response.json();

        if (data.success) {
            displayOrders(data.orders);
        } else {
            ordersList.innerHTML = `<p class="error-message">${data.error}</p>`;
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        ordersList.innerHTML = '<p class="error-message">Error loading orders</p>';
    }
}

function displayOrders(orders) {
    const ordersList = document.getElementById('orders-list');

    if (orders.length === 0) {
        ordersList.innerHTML = '<p class="info-message">No orders found</p>';
        return;
    }

    ordersList.innerHTML = orders.slice(0, 20).map(order => `
        <div class="order-card">
            <div class="order-header">
                <div class="order-id">${order.id}</div>
                <span class="order-status ${order.status}">${order.status.toUpperCase()}</span>
            </div>
            <div class="order-details">
                <div>
                    <strong>Date:</strong> ${order.order_date}
                </div>
                <div>
                    <strong>Items:</strong> ${order.items.length}
                </div>
                ${order.tracking_number ? `<div><strong>Tracking:</strong> ${order.tracking_number}</div>` : ''}
            </div>
            <div class="order-total">Total: $${order.total.toFixed(2)}</div>
        </div>
    `).join('');

    if (orders.length > 20) {
        ordersList.innerHTML += '<p class="info-message">Showing first 20 orders</p>';
    }
}

async function loadAccountInfo() {
    if (!currentCustomer) {
        document.getElementById('account-info').innerHTML = '<p class="info-message">Please login to view your account information.</p>';
        return;
    }

    try {
        const response = await fetch('/api/customer');
        const data = await response.json();

        if (data.logged_in) {
            const customer = data.customer;
            const accountInfo = document.getElementById('account-info');

            accountInfo.innerHTML = `
                <div class="account-info-grid">
                    <div class="info-section">
                        <h3>Personal Information</h3>
                        <div class="info-row">
                            <div class="info-label">Customer ID</div>
                            <div class="info-value">${customer.id}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Name</div>
                            <div class="info-value">${customer.name}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Email</div>
                            <div class="info-value">${customer.email}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Phone</div>
                            <div class="info-value">${customer.phone}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Member Since</div>
                            <div class="info-value">${customer.member_since}</div>
                        </div>
                    </div>
                    <div class="info-section">
                        <h3>Address</h3>
                        <div class="info-row">
                            <div class="info-value">
                                ${customer.address.street}<br>
                                ${customer.address.city}, ${customer.address.state} ${customer.address.zip}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading account info:', error);
    }
}
