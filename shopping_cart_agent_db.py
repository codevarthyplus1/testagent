#!/usr/bin/env python3
"""
Shopping Cart Customer Service Agent - Database Version

This agent helps customers with questions about:
- Products (availability, pricing, details)
- Orders (status, tracking, items)
- User account information

Works with SQL database instead of JSON files.
"""

import sqlite3
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class ShoppingCartAgentDB:
    """Customer service agent for shopping cart system using SQL database."""

    def __init__(self, db_path: str = "shopping_cart.db", customer_id: Optional[str] = None):
        """
        Initialize the agent with database connection.

        Args:
            db_path: Path to SQLite database file
            customer_id: Current customer ID for personalized queries
        """
        self.db_path = db_path
        self.customer_id = customer_id
        self.conn = None
        self._connect()

    def _connect(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable column access by name
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def _execute_query(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """Execute a SELECT query and return results."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Query error: {e}")
            return []

    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Convert sqlite3.Row to dictionary."""
        return dict(zip(row.keys(), row))

    def set_customer(self, customer_id: str) -> bool:
        """
        Set the current customer ID for personalized queries.

        Returns:
            True if customer exists, False otherwise
        """
        user = self.find_user(user_id=customer_id)
        if user:
            self.customer_id = customer_id
            return True
        return False

    def get_customer_info(self) -> Optional[Dict]:
        """Get current customer's information."""
        if not self.customer_id:
            return None
        return self.find_user(user_id=self.customer_id)

    def find_product(self, product_id: Optional[str] = None,
                    name: Optional[str] = None,
                    category: Optional[str] = None) -> List[Dict]:
        """Find products by ID, name, or category."""
        if product_id:
            query = "SELECT * FROM products WHERE id = ?"
            rows = self._execute_query(query, (product_id,))
        elif name:
            query = "SELECT * FROM products WHERE name LIKE ?"
            rows = self._execute_query(query, (f"%{name}%",))
        elif category:
            query = "SELECT * FROM products WHERE category LIKE ?"
            rows = self._execute_query(query, (f"%{category}%",))
        else:
            query = "SELECT * FROM products ORDER BY category, name"
            rows = self._execute_query(query)

        return [self._row_to_dict(row) for row in rows]

    def find_user(self, user_id: Optional[str] = None,
                  email: Optional[str] = None,
                  name: Optional[str] = None) -> Optional[Dict]:
        """Find user by ID, email, or name."""
        if user_id:
            query = "SELECT * FROM users WHERE id = ?"
            params = (user_id,)
        elif email:
            query = "SELECT * FROM users WHERE email = ?"
            params = (email,)
        elif name:
            query = "SELECT * FROM users WHERE name LIKE ?"
            params = (f"%{name}%",)
        else:
            return None

        rows = self._execute_query(query, params)
        if rows:
            user = self._row_to_dict(rows[0])
            # Combine address fields into nested dict
            user['address'] = {
                'street': user.pop('street'),
                'city': user.pop('city'),
                'state': user.pop('state'),
                'zip': user.pop('zip')
            }
            return user
        return None

    def find_orders(self, user_id: Optional[str] = None,
                   order_id: Optional[str] = None,
                   status: Optional[str] = None) -> List[Dict]:
        """Find orders by user ID, order ID, or status."""
        if order_id:
            query = "SELECT * FROM orders WHERE id = ?"
            params = (order_id,)
        elif user_id and status:
            query = "SELECT * FROM orders WHERE user_id = ? AND status = ? ORDER BY order_date DESC"
            params = (user_id, status)
        elif user_id:
            query = "SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC"
            params = (user_id,)
        elif status:
            query = "SELECT * FROM orders WHERE status = ? ORDER BY order_date DESC"
            params = (status,)
        else:
            query = "SELECT * FROM orders ORDER BY order_date DESC LIMIT 100"
            params = ()

        rows = self._execute_query(query, params)
        orders = []
        for row in rows:
            order = self._row_to_dict(row)
            # Combine shipping address fields
            order['shipping_address'] = {
                'street': order.pop('shipping_street'),
                'city': order.pop('shipping_city'),
                'state': order.pop('shipping_state'),
                'zip': order.pop('shipping_zip')
            }
            # Get order items
            order['items'] = self._get_order_items(order['id'])
            orders.append(order)

        return orders

    def _get_order_items(self, order_id: str) -> List[Dict]:
        """Get items for a specific order."""
        query = """
            SELECT oi.product_id, oi.quantity, oi.price, p.name as product_name, p.brand as product_brand
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        """
        rows = self._execute_query(query, (order_id,))
        return [self._row_to_dict(row) for row in rows]

    def get_order_details(self, order_id: str, verify_customer: bool = True) -> Optional[Dict]:
        """
        Get detailed information about an order including product names.

        Args:
            order_id: Order ID to retrieve
            verify_customer: If True, verify order belongs to current customer
        """
        orders = self.find_orders(order_id=order_id)
        if not orders:
            return None

        order = orders[0]

        # Verify this order belongs to the current customer if customer_id is set
        if verify_customer and self.customer_id and order['user_id'] != self.customer_id:
            return None

        user = self.find_user(user_id=order["user_id"])

        return {
            **order,
            "customer_name": user["name"] if user else "Unknown",
            "customer_email": user["email"] if user else "Unknown",
            "enriched_items": order['items']  # Already enriched from _get_order_items
        }

    def get_customer_orders(self, status: Optional[str] = None) -> List[Dict]:
        """Get orders for the current customer."""
        if not self.customer_id:
            return []
        return self.find_orders(user_id=self.customer_id, status=status)

    def get_order_summary(self) -> Dict:
        """Get summary of current customer's orders."""
        if not self.customer_id:
            return {}

        query = """
            SELECT
                COUNT(*) as total_orders,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing,
                SUM(CASE WHEN status = 'shipped' THEN 1 ELSE 0 END) as shipped,
                SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) as delivered,
                SUM(total) as total_spent
            FROM orders
            WHERE user_id = ?
        """
        rows = self._execute_query(query, (self.customer_id,))
        if rows:
            return self._row_to_dict(rows[0])
        return {}

    def answer_question(self, question: str) -> str:
        """Process natural language questions and provide answers."""
        question_lower = question.lower()

        # Check if customer is authenticated for personal queries
        if not self.customer_id:
            if "login" in question_lower or "customer id" in question_lower:
                return "Please provide your customer ID to access your account. Use: agent.set_customer('U000001')"
            # Allow product queries without authentication
            # Require authentication for personal queries (my, account, order, spent)
            personal_keywords = ["my account", "my profile", "my info", "my order", "my purchase", "how much", "spent"]
            if any(keyword in question_lower for keyword in personal_keywords):
                return "Please set your customer ID first to access your personal information. You can ask about products without logging in."

        # My account / profile queries
        if "my account" in question_lower or "my profile" in question_lower or "my info" in question_lower:
            if not self.customer_id:
                return "Please set your customer ID first to view your account information."
            customer = self.get_customer_info()
            if customer:
                return self._format_customer_info(customer)
            return "Could not find your account information."

        # Order summary queries
        if "how many orders" in question_lower or "order summary" in question_lower or "my orders" in question_lower and "status" not in question_lower:
            if not self.customer_id:
                return "Please set your customer ID first to view your orders."

            summary = self.get_order_summary()
            if summary and summary.get('total_orders', 0) > 0:
                return self._format_order_summary(summary)
            return "You don't have any orders yet."

        # Specific order status queries
        if "order" in question_lower and ("status" in question_lower or "track" in question_lower):
            # Try to extract order ID
            match = re.search(r'ORD\d+', question.upper())
            if match:
                order_id = match.group(0)
                order_details = self.get_order_details(order_id, verify_customer=True)
                if order_details:
                    return self._format_order_details(order_details)
                elif self.customer_id:
                    return f"Order {order_id} not found or doesn't belong to your account."
                else:
                    return f"Order {order_id} not found."
            return "Please provide an order ID (e.g., ORD000001) to check the status."

        # Pending orders
        if "pending" in question_lower and "order" in question_lower:
            if not self.customer_id:
                return "Please set your customer ID first."
            orders = self.get_customer_orders(status="pending")
            if orders:
                return self._format_orders_list(orders, "Pending Orders")
            return "You don't have any pending orders."

        # Shipped orders
        if "shipped" in question_lower and "order" in question_lower:
            if not self.customer_id:
                return "Please set your customer ID first."
            orders = self.get_customer_orders(status="shipped")
            if orders:
                return self._format_orders_list(orders, "Shipped Orders")
            return "You don't have any shipped orders."

        # Delivered orders
        if "delivered" in question_lower and "order" in question_lower:
            if not self.customer_id:
                return "Please set your customer ID first."
            orders = self.get_customer_orders(status="delivered")
            if orders:
                return self._format_orders_list(orders, "Delivered Orders")
            return "You don't have any delivered orders."

        # Product queries (available to everyone)
        if "product" in question_lower or "available" in question_lower or "catalog" in question_lower:
            # Specific product queries
            if "headphone" in question_lower:
                products = self.find_product(name="headphone")
            elif "coffee" in question_lower:
                products = self.find_product(name="coffee")
            elif "yoga" in question_lower or "mat" in question_lower:
                products = self.find_product(name="yoga")
            elif "water bottle" in question_lower or "bottle" in question_lower:
                products = self.find_product(name="bottle")
            elif "laptop" in question_lower:
                products = self.find_product(name="laptop")
            elif "lamp" in question_lower:
                products = self.find_product(name="lamp")
            elif "shirt" in question_lower or "t-shirt" in question_lower:
                products = self.find_product(name="shirt")
            elif "shoes" in question_lower or "running" in question_lower:
                products = self.find_product(name="shoes")
            # Category queries
            elif "electronics" in question_lower:
                products = self.find_product(category="electronics")
            elif "clothing" in question_lower:
                products = self.find_product(category="clothing")
            elif "kitchen" in question_lower or "home" in question_lower:
                products = self.find_product(category="kitchen")
            elif "fitness" in question_lower or "sports" in question_lower:
                products = self.find_product(category="sports")
            else:
                products = self.find_product()

            if products:
                return self._format_products(products)
            return "No products found."

        # Price queries
        if "price" in question_lower or "cost" in question_lower:
            if "headphone" in question_lower:
                products = self.find_product(name="headphone")
            elif "coffee" in question_lower:
                products = self.find_product(name="coffee")
            else:
                return "Which product would you like to know the price for?"

            if products:
                return self._format_products(products)

        # Stock queries
        if "stock" in question_lower or "in stock" in question_lower:
            products = self.find_product()
            in_stock = [p for p in products if p.get("stock", 0) > 0]
            return self._format_products(in_stock)

        # Total spent
        if "how much" in question_lower and ("spent" in question_lower or "purchased" in question_lower):
            if not self.customer_id:
                return "Please set your customer ID first."
            summary = self.get_order_summary()
            if summary.get('total_spent'):
                return f"You have spent ${summary['total_spent']:.2f} in total across {summary['total_orders']} orders."
            return "You haven't made any purchases yet."

        # General help
        return self._help_message()

    def _format_customer_info(self, customer: Dict) -> str:
        """Format customer information for display."""
        result = f"Account Information:\n\n"
        result += f"Customer ID: {customer['id']}\n"
        result += f"Name: {customer['name']}\n"
        result += f"Email: {customer['email']}\n"
        result += f"Phone: {customer['phone']}\n"
        result += f"Member Since: {customer['member_since']}\n\n"
        result += f"Address:\n"
        result += f"  {customer['address']['street']}\n"
        result += f"  {customer['address']['city']}, {customer['address']['state']} {customer['address']['zip']}\n"
        return result

    def _format_order_summary(self, summary: Dict) -> str:
        """Format order summary for display."""
        result = f"Order Summary:\n\n"
        result += f"Total Orders: {summary.get('total_orders', 0)}\n"
        result += f"  - Pending: {summary.get('pending', 0)}\n"
        result += f"  - Processing: {summary.get('processing', 0)}\n"
        result += f"  - Shipped: {summary.get('shipped', 0)}\n"
        result += f"  - Delivered: {summary.get('delivered', 0)}\n\n"
        if summary.get('total_spent'):
            result += f"Total Spent: ${summary['total_spent']:.2f}\n"
        return result

    def _format_orders_list(self, orders: List[Dict], title: str) -> str:
        """Format a list of orders for display."""
        result = f"{title} ({len(orders)}):\n\n"
        for order in orders[:10]:  # Show first 10
            result += f"Order {order['id']} - {order['order_date']}\n"
            result += f"  Status: {order['status'].upper()}\n"
            result += f"  Total: ${order['total']:.2f}\n"
            result += f"  Items: {len(order['items'])}\n"
            if order.get('tracking_number'):
                result += f"  Tracking: {order['tracking_number']}\n"
            result += "\n"

        if len(orders) > 10:
            result += f"... and {len(orders) - 10} more orders\n"

        return result

    def _format_products(self, products: List[Dict]) -> str:
        """Format product information for display."""
        if not products:
            return "No products found."

        result = f"Found {len(products)} product(s):\n\n"
        for product in products[:20]:  # Show first 20
            stock_status = "In Stock" if product.get("stock", 0) > 0 else "Out of Stock"
            result += f"Product: {product['name']}\n"
            result += f"  ID: {product['id']}\n"
            result += f"  Brand: {product.get('brand', 'N/A')}\n"
            result += f"  Category: {product.get('category', 'N/A')}\n"
            result += f"  Price: ${product['price']}\n"
            result += f"  Stock: {product.get('stock', 0)} ({stock_status})\n"
            if product.get('rating'):
                result += f"  Rating: {product['rating']}/5.0\n"
            if product.get('description'):
                result += f"  Description: {product['description']}\n"
            result += "\n"

        if len(products) > 20:
            result += f"... and {len(products) - 20} more products\n"

        return result

    def _format_order_details(self, order: Dict) -> str:
        """Format order details for display."""
        result = f"Order Details for {order['id']}:\n\n"
        result += f"Customer: {order['customer_name']} ({order['customer_email']})\n"
        result += f"Order Date: {order['order_date']}\n"
        result += f"Status: {order['status'].upper()}\n\n"

        result += "Items:\n"
        for item in order['enriched_items']:
            item_total = item['quantity'] * item['price']
            result += f"  - {item['product_name']} by {item['product_brand']}\n"
            result += f"    Quantity: {item['quantity']} x ${item['price']} = ${item_total:.2f}\n"

        result += f"\nSubtotal: ${order['subtotal']:.2f}\n"
        result += f"Tax: ${order['tax']:.2f}\n"
        result += f"Shipping: ${order['shipping']:.2f}\n"
        result += f"Total: ${order['total']:.2f}\n\n"

        result += f"Shipping Address:\n"
        addr = order['shipping_address']
        result += f"  {addr['street']}\n"
        result += f"  {addr['city']}, {addr['state']} {addr['zip']}\n"

        if order.get('tracking_number'):
            result += f"\nTracking Number: {order['tracking_number']}\n"

        if order['status'] == 'shipped' and order.get('shipped_date'):
            result += f"Shipped Date: {order['shipped_date']}\n"
        elif order['status'] == 'delivered' and order.get('delivered_date'):
            result += f"Delivered Date: {order['delivered_date']}\n"

        return result

    def _help_message(self) -> str:
        """Return help message with available commands."""
        customer_status = f"Logged in as: {self.customer_id}" if self.customer_id else "Not logged in"

        return f"""
Shopping Cart Customer Service Agent (Database Version)
{customer_status}

I can help you with:

1. Account Information:
   - "Show my account information"
   - "What's my profile?"

2. Order Queries:
   - "Show my orders"
   - "What's my order summary?"
   - "Show my pending orders"
   - "Show my delivered orders"
   - "What's the status of order ORD000001?"
   - "Track order ORD000001"
   - "How much have I spent?"

3. Product Information (available without login):
   - "What products are available?"
   - "Tell me about the wireless headphones"
   - "What electronics do you have?"
   - "How much does the coffee maker cost?"

4. Authentication:
   - Use: agent.set_customer('U000001') to login

How can I help you today?
"""

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Ensure database connection is closed."""
        self.close()


def main():
    """Run the customer service agent in interactive mode."""
    import sys

    print("=" * 70)
    print("Shopping Cart Customer Service Agent - Database Version")
    print("=" * 70)
    print()

    # Check if database exists
    db_path = "shopping_cart.db"
    try:
        agent = ShoppingCartAgentDB(db_path=db_path)
    except Exception as e:
        print(f"Error: Could not connect to database '{db_path}'")
        print(f"Please ensure the database exists and is properly initialized.")
        print(f"Error details: {e}")
        sys.exit(1)

    print("Welcome! I'm here to help you with product information and order tracking.")
    print()
    print("To access your personal information, please provide your customer ID:")
    print("Example: login U000001")
    print()
    print("Type 'help' for available commands or 'quit' to exit.")
    print()

    while True:
        try:
            question = input("You: ").strip()

            if not question:
                continue

            if question.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using our service. Have a great day!")
                break

            # Handle login command
            if question.lower().startswith('login'):
                parts = question.split()
                if len(parts) >= 2:
                    customer_id = parts[1].upper()
                    if agent.set_customer(customer_id):
                        customer = agent.get_customer_info()
                        print(f"\nWelcome back, {customer['name']}!")
                        print(f"Logged in as: {customer_id}\n")
                    else:
                        print(f"\nCustomer ID '{customer_id}' not found. Please check and try again.\n")
                else:
                    print("\nUsage: login <customer_id>")
                    print("Example: login U000001\n")
                continue

            # Handle logout command
            if question.lower() == 'logout':
                agent.customer_id = None
                print("\nYou have been logged out.\n")
                continue

            if question.lower() == 'help':
                print(agent._help_message())
                continue

            response = agent.answer_question(question)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            print("\n\nThank you for using our service. Have a great day!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")

    agent.close()


if __name__ == "__main__":
    main()
