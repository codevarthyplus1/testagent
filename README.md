# Shopping Cart Customer Service Agent

An intelligent customer service agent for a shopping cart system using SQL database. Available as both a **command-line interface** and a **web application** with customer ID authentication.

## Features

- **Web Interface**: Modern, responsive web UI with chat, product browsing, and order management
- **Customer Authentication**: Login with customer ID to access personalized information
- **Order Management**: View orders, track shipments, check order history by status
- **Account Information**: View profile, order summary, and spending history
- **Product Catalog**: Browse 278+ products across 8 categories
- **Access Control**: Customers can only access their own orders and information
- **Natural Language Processing**: Ask questions in plain English
- **Large Dataset**: 1,000 users with 100,000+ orders for realistic testing

## Quick Start

### Option 1: Web Application (Recommended)

1. **Install Dependencies:**
```bash
pip3 install -r requirements.txt
```

2. **Start the Web Server:**
```bash
python3 web_app.py
# Or use the startup script:
chmod +x start_web_app.sh
./start_web_app.sh
```

3. **Open in Browser:**
Navigate to `http://localhost:5000`

4. **Login:**
Use any customer ID from `U000001` to `U001000` (e.g., `U000001`)

### Option 2: Command Line Interface

1. **Initialize Database:**
```bash
python3 init_database.py
```

2. **Run the CLI Agent:**
```bash
python3 shopping_cart_agent_db.py
```

3. **Login and Query:**
```
You: login U000001
Agent: Welcome back, Ralph Roberts!

You: Show my account information
You: What's my order summary?
```

## Project Structure

```
.
├── web_app.py                  # Flask web application
├── templates/
│   └── index.html              # Web interface HTML
├── static/
│   ├── style.css               # Web interface styles
│   └── app.js                  # Frontend JavaScript
├── shopping_cart_agent_db.py   # CLI database agent
├── init_database.py            # Database initialization
├── test_agent_db.py            # CLI test suite
├── test_web_app.py             # Web API test suite
├── generate_database_dump.py   # MySQL dump generator
├── shopping_cart.db            # SQLite database (40MB)
├── database_dump.sql           # MySQL dump
├── requirements.txt            # Python dependencies
├── start_web_app.sh            # Web server startup script
├── README.md                   # This file
└── README_DATABASE.md          # Technical documentation
```

## Database Schema

### users
- 1,000 customers with complete profile information
- Fields: id, name, email, phone, address, member_since

### products
- 278+ products across 8 categories:
  - Electronics (40 products: Headphones, Speakers, Chargers, Accessories, etc.)
  - Clothing (34 products: Shirts, Pants, Accessories, etc.)
  - Home & Kitchen (39 products: Appliances, Cookware, Linens, etc.)
  - Sports & Fitness (40 products: Exercise Equipment, Athletic Shoes, Gear, etc.)
  - Beauty & Personal Care (35 products: Skincare, Haircare, Hygiene, etc.)
  - Books & Media (30 products: Books, Audiobooks, Media, etc.)
  - Toys & Games (30 products: Board Games, Toys, Gaming, etc.)
  - Office Supplies (30 products: Stationery, Organizers, Tools, etc.)

### orders
- 100,000 orders with various statuses (pending, processing, shipped, delivered)
- Fields: id, user_id, order_date, status, totals, shipping address, tracking

### order_items
- 300k+ individual items across all orders
- Linked to products and orders via foreign keys

## Usage Examples

### Web Application

The web interface provides a complete customer service experience with:
- **Chat Interface**: Ask questions in natural language
- **Product Catalog**: Browse and search 278+ products
- **Order Management**: View and track all your orders
- **Account Dashboard**: View personal information and statistics

**Features:**
- Responsive design works on desktop and mobile
- Real-time chat with the AI agent
- Filter products by category
- Filter orders by status (pending, processing, shipped, delivered)
- Session-based authentication

**Sample Customer IDs for Testing:**
- `U000001` - Ralph Roberts (119 orders, $60,161 spent)
- `U000010` - Christina Stone (103 orders, $39,475 spent)
- `U000100` - Various customers with different order histories

### Command Line Interface

```bash
python3 shopping_cart_agent_db.py

# Login with customer ID
login U000001

# Ask questions about your account
You: Show my account information
You: What's my order summary?

# View orders by status
You: Show my pending orders
You: Show my delivered orders

# Track specific orders
You: What's the status of order ORD000001?
You: Track order ORD000001

# Check spending
You: How much have I spent?

# Browse products (no login required)
logout
You: What products are available?
You: Tell me about wireless headphones
```

### Programmatic Usage

```python
from shopping_cart_agent_db import ShoppingCartAgentDB

# Initialize agent
agent = ShoppingCartAgentDB(db_path="shopping_cart.db")

# Login as customer
agent.set_customer("U000001")

# Get customer info
customer = agent.get_customer_info()
print(f"Welcome {customer['name']}!")

# Get order summary
summary = agent.get_order_summary()
print(f"Total orders: {summary['total_orders']}")
print(f"Total spent: ${summary['total_spent']:.2f}")

# Get orders by status
pending_orders = agent.get_customer_orders(status="pending")
print(f"You have {len(pending_orders)} pending orders")

# Track specific order
order = agent.get_order_details("ORD000001", verify_customer=True)
if order:
    print(f"Order status: {order['status']}")
    print(f"Total: ${order['total']:.2f}")

# Ask questions
response = agent.answer_question("What's my order summary?")
print(response)

# Close connection
agent.close()
```

## Supported Queries

### Account Queries (Requires Login)
- "Show my account information"
- "What's my profile?"
- "Show my orders"
- "What's my order summary?"
- "How much have I spent?"

### Order Queries (Requires Login)
- "Show my pending orders"
- "Show my processing orders"
- "Show my shipped orders"
- "Show my delivered orders"
- "What's the status of order ORD000001?"
- "Track order ORD000001"

### Product Queries (No Login Required)
- "What products are available?"
- "Tell me about wireless headphones"
- "What electronics do you have?"
- "Show me clothing items"
- "What fitness products do you have?"
- "How much does the coffee maker cost?"

## Sample Customer IDs

You can login with any customer ID from U000001 to U001000. Examples:

- **U000001** - Ralph Roberts (99 orders, $34,770 spent)
- **U000010** - Christina Stone (103 orders, $39,475 spent)
- **U000100** - Various customers with different order histories

## Security Features

- **Customer Authentication**: Must login with valid customer ID
- **Order Access Control**: Customers can only view their own orders
- **Data Isolation**: Verify customer ownership before returning order details
- **Public Product Info**: Product catalog accessible without authentication

## API Methods

### ShoppingCartAgentDB Class

**Authentication:**
- `set_customer(customer_id)` - Login as customer
- `get_customer_info()` - Get current customer's information

**Order Methods:**
- `find_orders(user_id, order_id, status)` - Find orders by criteria
- `get_order_details(order_id, verify_customer)` - Get complete order information
- `get_customer_orders(status)` - Get current customer's orders
- `get_order_summary()` - Get order statistics for customer

**Product Methods:**
- `find_product(product_id, name, category)` - Search for products
- `find_user(user_id, email, name)` - Look up user information

**Query Processing:**
- `answer_question(question)` - Process natural language queries

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
- SQLite3 (included with Python)

## Testing

Run the comprehensive test suite:

```bash
python3 test_agent_db.py
```

Tests include:
- Customer-specific queries for multiple users
- Order tracking and status queries
- Access control verification
- Product queries without authentication
- Unauthorized access attempts

## Files

**Web Application:**
- **web_app.py** - Flask web server with REST API
- **templates/index.html** - Single-page web interface
- **static/style.css** - Modern, responsive CSS styling
- **static/app.js** - Frontend JavaScript for interactivity
- **requirements.txt** - Python package dependencies
- **start_web_app.sh** - Convenient startup script

**Command Line:**
- **shopping_cart_agent_db.py** - CLI agent with database support
- **test_agent_db.py** - CLI test suite
- **test_web_app.py** - Web API test suite

**Database:**
- **init_database.py** - Generate SQLite database (no JSON dependencies)
- **generate_database_dump.py** - Generate MySQL-compatible SQL dump
- **shopping_cart.db** - SQLite database (created by init_database.py)
- **database_dump.sql** - MySQL dump (created by generate_database_dump.py)

**Documentation:**
- **README.md** - This file
- **README_DATABASE.md** - Detailed technical documentation

## Performance

- Database Size: ~40MB SQLite file
- Products: 278 across 8 categories
- Query Response: < 100ms for most queries
- Indexed fields: user_id, order_date, status, email
- Supports 100k+ orders and 300+ products without performance degradation

## REST API Endpoints

The web application provides the following REST API endpoints:

**Authentication:**
- `POST /api/login` - Login with customer ID
- `POST /api/logout` - Logout current customer
- `GET /api/customer` - Get current customer information

**Queries:**
- `POST /api/ask` - Ask a natural language question

**Products:**
- `GET /api/products` - Get all products (supports ?category= and ?search=)
- `GET /api/categories` - Get all product categories

**Orders (requires login):**
- `GET /api/orders` - Get customer orders (supports ?status=)
- `GET /api/order/<order_id>` - Get specific order details
- `GET /api/order-summary` - Get customer order statistics

## Documentation

For detailed technical documentation, see [README_DATABASE.md](README_DATABASE.md)

## Future Enhancements

- ✅ ~~Session management~~ (Implemented)
- ✅ ~~REST API interface~~ (Implemented)
- Order placement functionality
- Shopping cart management
- Payment processing integration
- Email notifications
- Advanced analytics and reporting
- Recommendation engine
- Multi-language support
- User registration and password authentication
