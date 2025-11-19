#!/usr/bin/env python3
"""
Test script for Shopping Cart Agent with Database

Demonstrates customer-specific queries using different customer IDs.
"""

from shopping_cart_agent_db import ShoppingCartAgentDB


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def test_customer_queries(agent, customer_id):
    """Test various queries for a specific customer."""
    print_section(f"Testing Customer: {customer_id}")

    # Login as customer
    if agent.set_customer(customer_id):
        print(f"✓ Successfully logged in as {customer_id}\n")
    else:
        print(f"✗ Customer {customer_id} not found\n")
        return

    # Test queries
    queries = [
        "Show my account information",
        "What's my order summary?",
        "Show my pending orders",
        "Show my delivered orders",
        "How much have I spent?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 70)
        response = agent.answer_question(query)
        print(response)


def test_order_tracking(agent):
    """Test order tracking for specific orders."""
    print_section("Testing Order Tracking")

    # Get some orders from database
    orders = agent.find_orders()[:5]  # Get first 5 orders

    for order in orders:
        print(f"\nTracking order {order['id']} for customer {order['user_id']}")
        print("-" * 70)

        # Login as the order's customer
        agent.set_customer(order['user_id'])

        # Track the order
        query = f"What's the status of order {order['id']}?"
        response = agent.answer_question(query)
        print(response)


def test_product_queries(agent):
    """Test product queries (no login required)."""
    print_section("Testing Product Queries (No Login Required)")

    # Clear customer ID to test without login
    agent.customer_id = None

    queries = [
        "What products are available?",
        "Tell me about wireless headphones",
        "What electronics do you have?",
        "How much does the coffee maker cost?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 70)
        response = agent.answer_question(query)
        print(response[:500])  # Limit output for readability
        if len(response) > 500:
            print("... (truncated)")


def test_unauthorized_access(agent):
    """Test that customers can't access other customers' orders."""
    print_section("Testing Order Access Control")

    # Get two different customers
    users = agent._execute_query("SELECT id FROM users LIMIT 2")
    if len(users) < 2:
        print("Not enough users for this test")
        return

    customer1 = users[0]['id']
    customer2 = users[1]['id']

    # Get an order from customer1
    agent.set_customer(customer1)
    orders1 = agent.get_customer_orders()
    if not orders1:
        print(f"Customer {customer1} has no orders")
        return

    order_id = orders1[0]['id']

    print(f"\nCustomer {customer1} accessing their own order {order_id}:")
    print("-" * 70)
    order_details = agent.get_order_details(order_id, verify_customer=True)
    if order_details:
        print(f"✓ Access granted: Order {order_id} found")
    else:
        print(f"✗ Access denied unexpectedly")

    # Now try to access that order as customer2
    agent.set_customer(customer2)
    print(f"\nCustomer {customer2} trying to access {customer1}'s order {order_id}:")
    print("-" * 70)
    order_details = agent.get_order_details(order_id, verify_customer=True)
    if order_details:
        print(f"✗ SECURITY ISSUE: Customer {customer2} accessed another customer's order!")
    else:
        print(f"✓ Access correctly denied: Order not found or doesn't belong to customer")


def main():
    """Run all tests."""
    print("=" * 70)
    print("Shopping Cart Agent Database - Test Suite")
    print("=" * 70)

    # Initialize agent
    agent = ShoppingCartAgentDB(db_path="shopping_cart.db")

    # Test different customer IDs
    test_customers = ["U000001", "U000010", "U000100"]

    for customer_id in test_customers:
        test_customer_queries(agent, customer_id)

    # Test order tracking
    test_order_tracking(agent)

    # Test product queries
    test_product_queries(agent)

    # Test access control
    test_unauthorized_access(agent)

    # Close connection
    agent.close()

    print("\n" + "=" * 70)
    print("All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
