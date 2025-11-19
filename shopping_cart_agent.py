#!/usr/bin/env python3
"""
Shopping Cart Customer Service Agent

This agent helps customers with questions about:
- Products (availability, pricing, details)
- Orders (status, tracking, items)
- User account information
"""

import json
import re
from typing import List, Dict, Optional
from datetime import datetime


class ShoppingCartAgent:
    """Customer service agent for shopping cart system."""

    def __init__(self, data_dir: str = "data"):
        """Initialize the agent with data from JSON files."""
        self.data_dir = data_dir
        self.products = self._load_json(f"{data_dir}/products.json")
        self.users = self._load_json(f"{data_dir}/users.json")
        self.orders = self._load_json(f"{data_dir}/orders.json")

    def _load_json(self, filepath: str) -> List[Dict]:
        """Load JSON data from file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Could not find {filepath}")
            return []

    def find_product(self, product_id: Optional[str] = None,
                    name: Optional[str] = None,
                    category: Optional[str] = None) -> List[Dict]:
        """Find products by ID, name, or category."""
        results = []

        for product in self.products:
            if product_id and product["id"] == product_id:
                return [product]

            if name and name.lower() in product["name"].lower():
                results.append(product)
            elif category and category.lower() in product["category"].lower():
                results.append(product)

        return results if results else self.products if not (product_id or name or category) else []

    def find_user(self, user_id: Optional[str] = None,
                  email: Optional[str] = None,
                  name: Optional[str] = None) -> Optional[Dict]:
        """Find user by ID, email, or name."""
        for user in self.users:
            if user_id and user["id"] == user_id:
                return user
            if email and user["email"].lower() == email.lower():
                return user
            if name and name.lower() in user["name"].lower():
                return user
        return None

    def find_orders(self, user_id: Optional[str] = None,
                   order_id: Optional[str] = None,
                   status: Optional[str] = None) -> List[Dict]:
        """Find orders by user ID, order ID, or status."""
        results = []

        for order in self.orders:
            if order_id and order["id"] == order_id:
                return [order]

            if user_id and order["user_id"] == user_id:
                if status:
                    if order["status"].lower() == status.lower():
                        results.append(order)
                else:
                    results.append(order)
            elif status and not user_id:
                if order["status"].lower() == status.lower():
                    results.append(order)

        return results

    def get_order_details(self, order_id: str) -> Optional[Dict]:
        """Get detailed information about an order including product names."""
        orders = self.find_orders(order_id=order_id)
        if not orders:
            return None

        order = orders[0]
        user = self.find_user(user_id=order["user_id"])

        # Enrich order items with product details
        enriched_items = []
        for item in order["items"]:
            product = self.find_product(product_id=item["product_id"])
            if product:
                enriched_items.append({
                    **item,
                    "product_name": product[0]["name"],
                    "product_brand": product[0]["brand"]
                })

        return {
            **order,
            "customer_name": user["name"] if user else "Unknown",
            "customer_email": user["email"] if user else "Unknown",
            "enriched_items": enriched_items
        }

    def answer_question(self, question: str) -> str:
        """Process natural language questions and provide answers."""
        question_lower = question.lower()

        # Order status queries (check this first to avoid conflicts)
        if "order" in question_lower and ("status" in question_lower or "track" in question_lower):
            # Try to extract order ID
            match = re.search(r'ORD\d+', question.upper())
            if match:
                order_id = match.group(0)
                order_details = self.get_order_details(order_id)
                if order_details:
                    return self._format_order_details(order_details)
            return "Please provide an order ID (e.g., ORD001) to check the status."

        # Specific product queries (before general product queries)
        if "headphone" in question_lower:
            products = self.find_product(name="headphone")
            if products:
                return self._format_products(products)
        elif "coffee" in question_lower:
            products = self.find_product(name="coffee")
            if products:
                return self._format_products(products)
        elif "yoga" in question_lower or ("mat" in question_lower and "yoga" not in question_lower):
            products = self.find_product(name="yoga")
            if products:
                return self._format_products(products)
        elif "water bottle" in question_lower or "bottle" in question_lower:
            products = self.find_product(name="bottle")
            if products:
                return self._format_products(products)
        elif "laptop" in question_lower and "stand" in question_lower:
            products = self.find_product(name="laptop")
            if products:
                return self._format_products(products)
        elif "lamp" in question_lower:
            products = self.find_product(name="lamp")
            if products:
                return self._format_products(products)
        elif "shirt" in question_lower or "t-shirt" in question_lower:
            products = self.find_product(name="shirt")
            if products:
                return self._format_products(products)
        elif "shoes" in question_lower or "running" in question_lower:
            products = self.find_product(name="shoes")
            if products:
                return self._format_products(products)

        # Category queries
        if "electronics" in question_lower:
            products = self.find_product(category="electronics")
            if products:
                return self._format_products(products)
        elif "clothing" in question_lower:
            products = self.find_product(category="clothing")
            if products:
                return self._format_products(products)
        elif "kitchen" in question_lower or "home" in question_lower:
            products = self.find_product(category="kitchen")
            if products:
                return self._format_products(products)
        elif "fitness" in question_lower or "sports" in question_lower:
            products = self.find_product(category="sports")
            if products:
                return self._format_products(products)

        # General product catalog query
        if "product" in question_lower or "item" in question_lower or "available" in question_lower or "catalog" in question_lower:
            return self._format_product_catalog()

        # User order history
        elif "my order" in question_lower or "my purchase" in question_lower:
            # In a real system, we'd have authenticated user context
            return "Please provide your email address or order ID to look up your orders."

        # Price queries
        elif "price" in question_lower or "cost" in question_lower:
            if "headphone" in question_lower:
                products = self.find_product(name="headphone")
            elif "coffee" in question_lower:
                products = self.find_product(name="coffee")
            else:
                return "Which product would you like to know the price for?"

            if products:
                return self._format_products(products)

        # Stock queries
        elif "stock" in question_lower or "in stock" in question_lower:
            products = self.products
            in_stock = [p for p in products if p["stock"] > 0]
            return self._format_products(in_stock)

        # General help
        else:
            return self._help_message()

    def _format_products(self, products: List[Dict]) -> str:
        """Format product information for display."""
        if not products:
            return "No products found."

        result = f"Found {len(products)} product(s):\n\n"
        for product in products:
            stock_status = "In Stock" if product["stock"] > 0 else "Out of Stock"
            result += f"Product: {product['name']}\n"
            result += f"  ID: {product['id']}\n"
            result += f"  Brand: {product['brand']}\n"
            result += f"  Category: {product['category']}\n"
            result += f"  Price: ${product['price']}\n"
            result += f"  Stock: {product['stock']} ({stock_status})\n"
            result += f"  Rating: {product['rating']}/5.0\n"
            result += f"  Description: {product['description']}\n\n"

        return result

    def _format_product_catalog(self) -> str:
        """Format entire product catalog."""
        categories = {}
        for product in self.products:
            cat = product['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(product)

        result = "Product Catalog:\n\n"
        for category, products in categories.items():
            result += f"{category}:\n"
            for product in products:
                result += f"  - {product['name']} (${product['price']}) - {product['stock']} in stock\n"
            result += "\n"

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

        if 'tracking_number' in order:
            result += f"\nTracking Number: {order['tracking_number']}\n"

        if order['status'] == 'shipped' and 'shipped_date' in order:
            result += f"Shipped Date: {order['shipped_date']}\n"
        elif order['status'] == 'delivered' and 'delivered_date' in order:
            result += f"Delivered Date: {order['delivered_date']}\n"

        return result

    def _help_message(self) -> str:
        """Return help message with available commands."""
        return """
I'm your Shopping Cart Customer Service Agent! I can help you with:

1. Product Information:
   - "What products are available?"
   - "Tell me about the wireless headphones"
   - "What electronics do you have?"
   - "Is the yoga mat in stock?"
   - "How much does the coffee maker cost?"

2. Order Tracking:
   - "What's the status of order ORD001?"
   - "Track my order ORD002"

3. Product Categories:
   - Electronics
   - Clothing
   - Home & Kitchen
   - Sports & Fitness

How can I help you today?
"""


def main():
    """Run the customer service agent in interactive mode."""
    print("=" * 60)
    print("Shopping Cart Customer Service Agent")
    print("=" * 60)
    print()

    agent = ShoppingCartAgent()

    print("Welcome! I'm here to help you with product information and order tracking.")
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


if __name__ == "__main__":
    main()
