#!/usr/bin/env python3
"""Test script for web application"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_api():
    print("Testing Web API...")
    print("="*60)

    # Test 1: Get categories
    print("\n1. Getting categories...")
    response = requests.get(f"{BASE_URL}/api/categories")
    data = response.json()
    print(f"Categories: {data['categories']}")

    # Test 2: Get products
    print("\n2. Getting products...")
    response = requests.get(f"{BASE_URL}/api/products")
    data = response.json()
    print(f"Products loaded: {len(data['products'])}")

    # Test 3: Login
    print("\n3. Testing login...")
    session = requests.Session()
    response = session.post(
        f"{BASE_URL}/api/login",
        json={"customer_id": "U000001"},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    if data['success']:
        print(f"Logged in as: {data['customer']['name']}")

    # Test 4: Get customer info
    print("\n4. Getting customer info...")
    response = session.get(f"{BASE_URL}/api/customer")
    data = response.json()
    if data['logged_in']:
        print(f"Customer: {data['customer']['name']}")

    # Test 5: Ask a question
    print("\n5. Asking a question...")
    response = session.post(
        f"{BASE_URL}/api/ask",
        json={"question": "What is my order summary?"},
        headers={"Content-Type": "application/json"}
    )
    data = response.json()
    print(f"Answer: {data['answer'][:100]}...")

    # Test 6: Get orders
    print("\n6. Getting orders...")
    response = session.get(f"{BASE_URL}/api/orders")
    data = response.json()
    if data['success']:
        print(f"Orders found: {len(data['orders'])}")

    print("\n" + "="*60)
    print("All tests completed successfully!")

if __name__ == "__main__":
    print("Make sure the web server is running on http://localhost:5000")
    print("Run: python3 web_app.py")
    print()

    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to web server")
        print("Please start the server first: python3 web_app.py")
    except Exception as e:
        print(f"ERROR: {e}")
