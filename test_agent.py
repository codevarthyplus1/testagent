#!/usr/bin/env python3
"""
Test script for the Shopping Cart Customer Service Agent
"""

from shopping_cart_agent import ShoppingCartAgent


def test_agent():
    """Test various agent functionalities."""
    print("=" * 60)
    print("Testing Shopping Cart Customer Service Agent")
    print("=" * 60)
    print()

    agent = ShoppingCartAgent()

    # Test queries
    test_queries = [
        "What products are available?",
        "Tell me about the wireless headphones",
        "What electronics do you have?",
        "What's the status of order ORD001?",
        "How much does the coffee maker cost?",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 60)
        response = agent.answer_question(query)
        print(response)
        print()

    # Test direct API methods
    print("\n" + "=" * 60)
    print("Testing Direct API Methods")
    print("=" * 60)
    print()

    print("1. Finding product by name:")
    products = agent.find_product(name="headphones")
    print(f"   Found {len(products)} product(s)")

    print("\n2. Finding orders by user:")
    orders = agent.find_orders(user_id="U001")
    print(f"   User U001 has {len(orders)} order(s)")

    print("\n3. Getting order details:")
    order_details = agent.get_order_details("ORD001")
    if order_details:
        print(f"   Order ORD001 - Status: {order_details['status']}")
        print(f"   Customer: {order_details['customer_name']}")
        print(f"   Total: ${order_details['total']:.2f}")

    print("\n" + "=" * 60)
    print("All tests completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    test_agent()
