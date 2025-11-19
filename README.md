# Shopping Cart Customer Service Agent

An intelligent customer service agent for a shopping cart system that can answer questions about products, orders, and customer information.

## Features

- Product information queries (availability, pricing, details)
- Order tracking and status updates
- Natural language question processing
- Sample data included for testing

## Project Structure

```
.
├── data/
│   ├── products.json    # Sample product catalog
│   ├── users.json       # Sample customer data
│   └── orders.json      # Sample order history
├── shopping_cart_agent.py  # Main agent implementation
└── README.md
```

## Sample Data

### Products
- 8 products across 4 categories:
  - Electronics (Headphones, LED Lamp, Laptop Stand)
  - Clothing (T-Shirts)
  - Home & Kitchen (Water Bottle, Coffee Maker)
  - Sports & Fitness (Yoga Mat, Running Shoes)

### Users
- 5 sample customers with complete profile information

### Orders
- 6 sample orders with various statuses:
  - Pending
  - Processing
  - Shipped
  - Delivered

## Usage

### Interactive Mode

Run the agent in interactive mode to chat with it:

```bash
python3 shopping_cart_agent.py
```

### Example Queries

The agent can answer questions like:

**Product Information:**
- "What products are available?"
- "Tell me about the wireless headphones"
- "What electronics do you have?"
- "How much does the coffee maker cost?"
- "Is the yoga mat in stock?"

**Order Tracking:**
- "What's the status of order ORD001?"
- "Track order ORD002"

**Category Browsing:**
- "Show me electronics"
- "What fitness products do you have?"

### Python API

You can also use the agent programmatically:

```python
from shopping_cart_agent import ShoppingCartAgent

# Initialize the agent
agent = ShoppingCartAgent()

# Find products
products = agent.find_product(name="headphones")

# Get order details
order_details = agent.get_order_details("ORD001")

# Answer natural language questions
response = agent.answer_question("What's the status of my order ORD001?")
print(response)
```

## API Methods

### ShoppingCartAgent Class

- `find_product(product_id, name, category)` - Search for products
- `find_user(user_id, email, name)` - Look up user information
- `find_orders(user_id, order_id, status)` - Find orders by various criteria
- `get_order_details(order_id)` - Get complete order information with product details
- `answer_question(question)` - Process natural language queries

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Future Enhancements

- Integration with real database
- User authentication
- Order placement functionality
- Payment processing
- Email notifications
- Advanced search with filters
- Recommendation engine
- Multi-language support
