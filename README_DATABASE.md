# Shopping Cart Agent - Database Version

Customer service agent that uses SQL database for handling customer-specific queries based on customer ID.

## Features

- **Customer Authentication**: Login with customer ID to access personalized information
- **Order Management**: View orders, track shipments, check order history
- **Account Information**: View profile and account details
- **Product Catalog**: Browse products without authentication
- **Access Control**: Customers can only access their own orders and information

## Database Schema

The system uses a SQLite database with the following tables:

### users
- Customer information (1,000 records)
- Fields: id, name, email, phone, address, member_since

### products
- Product catalog (8 products)
- Fields: id, name, category, price, stock, description, brand, rating

### orders
- Order records (100,000 records)
- Fields: id, user_id, order_date, status, totals, shipping address, tracking

### order_items
- Individual items in each order (300k+ records)
- Fields: id, order_id, product_id, quantity, price

## Setup

### 1. Initialize the Database

```bash
python3 init_database.py
```

This creates `shopping_cart.db` with:
- 1,000 users
- 100,000 orders
- 300k+ order items
- 8 products

### 2. Run the Interactive Agent

```bash
python3 shopping_cart_agent_db.py
```

### 3. Run Tests

```bash
python3 test_agent_db.py
```

## Usage

### Interactive Mode

```python
# Start the agent
python3 shopping_cart_agent_db.py

# Login with customer ID
login U000001

# Ask questions
You: Show my account information
You: What's my order summary?
You: Show my pending orders
You: Track order ORD000001
You: How much have I spent?

# Logout
logout

# Ask about products (no login required)
You: What products are available?
You: Tell me about wireless headphones
```

### Programmatic Usage

```python
from shopping_cart_agent_db import ShoppingCartAgentDB

# Initialize agent
agent = ShoppingCartAgentDB(db_path="shopping_cart.db")

# Set customer ID
agent.set_customer("U000001")

# Get customer info
customer = agent.get_customer_info()
print(f"Welcome {customer['name']}!")

# Get order summary
summary = agent.get_order_summary()
print(f"Total orders: {summary['total_orders']}")

# Get customer orders
orders = agent.get_customer_orders(status="pending")

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
- "Show my shipped orders"
- "Show my delivered orders"
- "What's the status of order ORD000001?"
- "Track order ORD000001"

### Product Queries (No Login Required)
- "What products are available?"
- "Tell me about wireless headphones"
- "What electronics do you have?"
- "Show me clothing items"
- "How much does the coffee maker cost?"

## Sample Customer IDs

- U000001 - Ralph Roberts (99 orders)
- U000010 - Christina Stone (103 orders)
- U000100 - Various users
- ... up to U001000

You can query any customer from U000001 to U001000.

## Security Features

- **Order Access Control**: Customers can only view their own orders
- **Customer Verification**: Orders are verified to belong to the logged-in customer
- **Public Product Info**: Product catalog is accessible without authentication

## Files

- `shopping_cart_agent_db.py` - Main agent implementation with database support
- `init_database.py` - Database initialization script
- `test_agent_db.py` - Test suite demonstrating functionality
- `shopping_cart.db` - SQLite database file (created by init_database.py)
- `database_dump.sql` - MySQL-compatible SQL dump (25MB)

## Performance

- Database: ~15MB SQLite file
- Query Response: < 100ms for most queries
- Indexed fields for optimal performance

## Differences from JSON Version

| Feature | JSON Version | Database Version |
|---------|-------------|------------------|
| Data Storage | JSON files | SQLite database |
| Records | 5 users, 6 orders | 1000 users, 100k orders |
| Authentication | Not implemented | Customer ID based |
| Access Control | None | Order-level verification |
| Performance | Fast for small data | Optimized for large data |
| Queries | In-memory search | SQL queries with indexes |

## Future Enhancements

- Session management with tokens
- Order placement functionality
- Shopping cart management
- Payment processing integration
- Email notifications
- Advanced search and filtering
- Analytics and reporting
- Multi-language support
