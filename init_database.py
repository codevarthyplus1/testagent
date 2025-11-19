#!/usr/bin/env python3
"""
Initialize SQLite database from the generated SQL dump.

This script creates a SQLite database and loads the data from database_dump.sql.
SQLite syntax is slightly different from MySQL, so we'll regenerate the data directly.
"""

import sqlite3
import json
import random
from datetime import datetime, timedelta


def create_tables(conn):
    """Create database tables."""
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            street TEXT,
            city TEXT,
            state TEXT,
            zip TEXT,
            member_since DATE
        )
    """)

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            description TEXT,
            brand TEXT,
            rating REAL
        )
    """)

    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            order_date DATE NOT NULL,
            status TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax REAL NOT NULL,
            shipping REAL NOT NULL,
            total REAL NOT NULL,
            shipping_street TEXT,
            shipping_city TEXT,
            shipping_state TEXT,
            shipping_zip TEXT,
            tracking_number TEXT,
            shipped_date DATE,
            delivered_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    conn.commit()
    print("Tables created successfully")


def create_indexes(conn):
    """Create indexes for better performance."""
    cursor = conn.cursor()

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)")

    conn.commit()
    print("Indexes created successfully")


def load_products(conn):
    """Load products from JSON file."""
    print("Loading products...")

    with open('data/products.json', 'r') as f:
        products = json.load(f)

    cursor = conn.cursor()
    for product in products:
        cursor.execute("""
            INSERT OR REPLACE INTO products (id, name, category, price, stock, description, brand, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product['id'],
            product['name'],
            product['category'],
            product['price'],
            product['stock'],
            product['description'],
            product['brand'],
            product['rating']
        ))

    conn.commit()
    print(f"Loaded {len(products)} products")


def generate_and_load_users(conn, count=1000):
    """Generate and load users into database."""
    print(f"Generating and loading {count} users...")

    from generate_database_dump import (
        FIRST_NAMES, LAST_NAMES, CITIES,
        generate_phone, generate_street_address, generate_member_since
    )

    cursor = conn.cursor()
    batch = []
    used_emails = set()

    def generate_unique_email(first_name, last_name, user_id):
        """Generate a unique email address."""
        domains = ["email.com", "mail.com", "example.com", "webmail.com", "inbox.com"]
        # Always use user_id to ensure uniqueness
        email = f"{first_name.lower()}.{last_name.lower()}.{user_id}@{random.choice(domains)}"
        return email

    for i in range(1, count + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        city, state, base_zip = random.choice(CITIES)
        zip_code = str(int(base_zip) + random.randint(0, 99))

        email = generate_unique_email(first_name, last_name, i)
        used_emails.add(email)

        user = (
            f"U{i:06d}",
            f"{first_name} {last_name}",
            email,
            generate_phone(),
            generate_street_address(),
            city,
            state,
            zip_code,
            generate_member_since()
        )
        batch.append(user)

        if len(batch) >= 1000:
            cursor.executemany("""
                INSERT INTO users (id, name, email, phone, street, city, state, zip, member_since)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch)
            conn.commit()
            print(f"  Loaded {i} users...")
            batch = []

    # Insert remaining
    if batch:
        cursor.executemany("""
            INSERT INTO users (id, name, email, phone, street, city, state, zip, member_since)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, batch)
        conn.commit()

    print(f"Loaded {count} users")


def generate_and_load_orders(conn, count=100000):
    """Generate and load orders into database."""
    print(f"Generating and loading {count} orders...")

    from generate_database_dump import PRODUCTS, ORDER_STATUSES

    # Get all users
    cursor = conn.cursor()
    cursor.execute("SELECT id, member_since FROM users")
    users = [(row[0], row[1]) for row in cursor.fetchall()]

    if not users:
        print("Error: No users found in database")
        return

    order_batch = []
    items_batch = []
    batch_size = 1000

    for i in range(1, count + 1):
        # Pick a random user
        user_id, member_since = random.choice(users)

        # Generate order items (1-5 items per order)
        num_items = random.randint(1, 5)
        items = []
        subtotal = 0

        for _ in range(num_items):
            product = random.choice(PRODUCTS)
            quantity = random.randint(1, 3)
            price = product["price"]
            subtotal += quantity * price

            items.append({
                "product_id": product["id"],
                "quantity": quantity,
                "price": price
            })

        # Calculate totals
        tax = round(subtotal * 0.08, 2)
        if subtotal > 100:
            shipping = 0.0
        elif subtotal > 50:
            shipping = 5.99
        else:
            shipping = 7.99
        total = round(subtotal + tax + shipping, 2)

        # Generate order date
        member_date = datetime.strptime(member_since, "%Y-%m-%d")
        today = datetime.now()
        days_range = (today - member_date).days
        if days_range < 1:
            days_range = 1
        days_ago = random.randint(0, min(days_range, 365))
        order_date = today - timedelta(days=days_ago)

        status = random.choice(ORDER_STATUSES)
        order_id = f"ORD{i:06d}"

        # Get shipping address from user
        cursor.execute("SELECT street, city, state, zip FROM users WHERE id = ?", (user_id,))
        addr = cursor.fetchone()

        tracking_number = None
        shipped_date = None
        delivered_date = None

        if status in ["shipped", "delivered"]:
            tracking_number = f"TRK{random.randint(100000000, 999999999)}"
            shipped_date = order_date + timedelta(days=random.randint(1, 3))
            shipped_date = shipped_date.strftime("%Y-%m-%d")

            if status == "delivered":
                delivered_date = datetime.strptime(shipped_date, "%Y-%m-%d") + timedelta(days=random.randint(2, 7))
                delivered_date = delivered_date.strftime("%Y-%m-%d")

        order = (
            order_id,
            user_id,
            order_date.strftime("%Y-%m-%d"),
            status,
            round(subtotal, 2),
            tax,
            shipping,
            total,
            addr[0],  # street
            addr[1],  # city
            addr[2],  # state
            addr[3],  # zip
            tracking_number,
            shipped_date,
            delivered_date
        )
        order_batch.append(order)

        # Add items for this order
        for item in items:
            items_batch.append((
                order_id,
                item["product_id"],
                item["quantity"],
                item["price"]
            ))

        # Batch insert
        if len(order_batch) >= batch_size:
            cursor.executemany("""
                INSERT INTO orders (id, user_id, order_date, status, subtotal, tax, shipping, total,
                                  shipping_street, shipping_city, shipping_state, shipping_zip,
                                  tracking_number, shipped_date, delivered_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, order_batch)

            cursor.executemany("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, items_batch)

            conn.commit()
            print(f"  Loaded {i} orders...")
            order_batch = []
            items_batch = []

    # Insert remaining
    if order_batch:
        cursor.executemany("""
            INSERT INTO orders (id, user_id, order_date, status, subtotal, tax, shipping, total,
                              shipping_street, shipping_city, shipping_state, shipping_zip,
                              tracking_number, shipped_date, delivered_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, order_batch)

        cursor.executemany("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, items_batch)

        conn.commit()

    print(f"Loaded {count} orders")


def get_database_stats(conn):
    """Print database statistics."""
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM order_items")
    item_count = cursor.fetchone()[0]

    print("\n" + "=" * 70)
    print("Database Statistics:")
    print("=" * 70)
    print(f"Users: {user_count}")
    print(f"Products: {product_count}")
    print(f"Orders: {order_count}")
    print(f"Order Items: {item_count}")
    print("=" * 70)


def main():
    """Main function to initialize the database."""
    import os

    db_path = "shopping_cart.db"

    print("=" * 70)
    print("Shopping Cart Database Initialization")
    print("=" * 70)
    print()

    # Remove existing database if it exists
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
        print()

    # Create new database
    print(f"Creating new database: {db_path}")
    conn = sqlite3.connect(db_path)

    try:
        # Create schema
        create_tables(conn)

        # Load data
        load_products(conn)
        generate_and_load_users(conn, count=1000)
        generate_and_load_orders(conn, count=100000)

        # Create indexes
        create_indexes(conn)

        # Show stats
        get_database_stats(conn)

        print("\nDatabase initialization complete!")
        print(f"Database file: {db_path}")
        print()

    except Exception as e:
        print(f"\nError during database initialization: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
