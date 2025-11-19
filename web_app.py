#!/usr/bin/env python3
"""
Web-based Shopping Cart Customer Service Agent

Flask web application providing a customer service interface
for the shopping cart system.
"""

from flask import Flask, render_template, request, jsonify, session
from shopping_cart_agent_db import ShoppingCartAgentDB
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Database path
DB_PATH = "shopping_cart.db"


def get_agent():
    """Get or create agent instance for current session."""
    customer_id = session.get('customer_id')
    agent = ShoppingCartAgentDB(db_path=DB_PATH, customer_id=customer_id)
    return agent


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    """Login with customer ID."""
    data = request.json
    customer_id = data.get('customer_id', '').upper().strip()

    if not customer_id:
        return jsonify({'success': False, 'error': 'Customer ID is required'})

    agent = ShoppingCartAgentDB(db_path=DB_PATH)
    if agent.set_customer(customer_id):
        customer = agent.get_customer_info()
        session['customer_id'] = customer_id
        agent.close()
        return jsonify({
            'success': True,
            'customer': {
                'id': customer['id'],
                'name': customer['name'],
                'email': customer['email']
            }
        })
    else:
        agent.close()
        return jsonify({'success': False, 'error': 'Customer ID not found'})


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout current customer."""
    session.pop('customer_id', None)
    return jsonify({'success': True})


@app.route('/api/customer', methods=['GET'])
def get_customer():
    """Get current customer info."""
    if 'customer_id' not in session:
        return jsonify({'logged_in': False})

    agent = get_agent()
    customer = agent.get_customer_info()
    agent.close()

    if customer:
        return jsonify({
            'logged_in': True,
            'customer': {
                'id': customer['id'],
                'name': customer['name'],
                'email': customer['email'],
                'phone': customer['phone'],
                'address': customer['address'],
                'member_since': customer['member_since']
            }
        })
    else:
        return jsonify({'logged_in': False})


@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Process a question from the user."""
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({'success': False, 'error': 'Question is required'})

    agent = get_agent()
    answer = agent.answer_question(question)
    agent.close()

    return jsonify({'success': True, 'answer': answer})


@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get customer orders."""
    if 'customer_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})

    status = request.args.get('status')

    agent = get_agent()
    if status:
        orders = agent.get_customer_orders(status=status)
    else:
        orders = agent.get_customer_orders()
    agent.close()

    return jsonify({'success': True, 'orders': orders})


@app.route('/api/order/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details."""
    if 'customer_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})

    agent = get_agent()
    order = agent.get_order_details(order_id, verify_customer=True)
    agent.close()

    if order:
        return jsonify({'success': True, 'order': order})
    else:
        return jsonify({'success': False, 'error': 'Order not found or access denied'})


@app.route('/api/order-summary', methods=['GET'])
def get_order_summary():
    """Get customer order summary."""
    if 'customer_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})

    agent = get_agent()
    summary = agent.get_order_summary()
    agent.close()

    return jsonify({'success': True, 'summary': summary})


@app.route('/api/products', methods=['GET'])
def get_products():
    """Get products (filtered by category or search)."""
    category = request.args.get('category')
    search = request.args.get('search')

    agent = get_agent()

    if category:
        products = agent.find_product(category=category)
    elif search:
        products = agent.find_product(name=search)
    else:
        products = agent.find_product()

    agent.close()

    return jsonify({'success': True, 'products': products})


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all product categories."""
    agent = get_agent()

    # Get unique categories from database
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    agent.close()

    return jsonify({'success': True, 'categories': categories})


if __name__ == '__main__':
    print("=" * 70)
    print("Shopping Cart Customer Service Agent - Web Interface")
    print("=" * 70)
    print()
    print("Starting web server...")
    print("Open your browser to: http://localhost:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)
