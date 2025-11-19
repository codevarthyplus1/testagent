#!/usr/bin/env python3
"""
Initialize SQLite database from the generated SQL dump.

This script creates a SQLite database and loads the data from database_dump.sql.
SQLite syntax is slightly different from MySQL, so we'll regenerate the data directly.
"""

import sqlite3
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


def generate_products(count=300):
    """Generate a diverse list of products."""

    # Product categories with items
    product_data = {
        "Electronics": {
            "items": [
                "Wireless Headphones", "Bluetooth Earbuds", "Noise Cancelling Headphones",
                "LED Desk Lamp", "Smart Bulb", "Ring Light", "Table Lamp",
                "Laptop Stand", "Monitor Stand", "Phone Stand", "Tablet Stand",
                "USB Hub", "Card Reader", "External SSD", "USB Flash Drive",
                "Wireless Mouse", "Mechanical Keyboard", "Gaming Mouse", "Ergonomic Keyboard",
                "Webcam", "Microphone", "USB Cable", "HDMI Cable", "Power Bank",
                "Wireless Charger", "Fast Charger", "Charging Cable", "Wall Adapter",
                "Smart Watch", "Fitness Tracker", "Phone Case", "Screen Protector",
                "Bluetooth Speaker", "Portable Speaker", "Soundbar", "Smart Display",
                "Security Camera", "Doorbell Camera", "Smart Plug", "Smart Thermostat"
            ],
            "brands": ["TechPro", "AudioTech", "BrightSpace", "DeskPro", "SmartHome", "GadgetHub"]
        },
        "Clothing": {
            "items": [
                "Cotton T-Shirt", "V-Neck Shirt", "Polo Shirt", "Long Sleeve Shirt",
                "Hoodie", "Sweatshirt", "Jacket", "Winter Coat", "Rain Jacket",
                "Jeans", "Chinos", "Cargo Pants", "Joggers", "Shorts",
                "Dress", "Skirt", "Blouse", "Tank Top", "Cardigan",
                "Socks", "Underwear", "Bra", "Sports Bra", "Leggings",
                "Hat", "Beanie", "Cap", "Scarf", "Gloves",
                "Belt", "Tie", "Bow Tie", "Suspenders", "Wallet"
            ],
            "brands": ["EcoWear", "FashionHub", "StyleCo", "TrendyThreads", "UrbanStyle", "ClassicFit"]
        },
        "Home & Kitchen": {
            "items": [
                "Coffee Maker", "French Press", "Pour Over", "Espresso Machine",
                "Blender", "Food Processor", "Juicer", "Hand Mixer", "Stand Mixer",
                "Toaster", "Air Fryer", "Microwave", "Rice Cooker", "Slow Cooker",
                "Water Bottle", "Travel Mug", "Tea Infuser", "Wine Glasses", "Coffee Mugs",
                "Knife Set", "Cutting Board", "Mixing Bowls", "Measuring Cups", "Spatula Set",
                "Cookware Set", "Frying Pan", "Sauce Pan", "Dutch Oven", "Baking Sheet",
                "Bed Sheets", "Pillows", "Comforter", "Blanket", "Mattress Pad",
                "Towel Set", "Bath Mat", "Shower Curtain", "Storage Bins", "Hangers"
            ],
            "brands": ["BrewMaster", "HydroLife", "ChefPro", "HomeEssentials", "KitchenAid", "ComfortHome"]
        },
        "Sports & Fitness": {
            "items": [
                "Yoga Mat", "Exercise Mat", "Foam Roller", "Resistance Bands", "Dumbbells",
                "Running Shoes", "Training Shoes", "Basketball Shoes", "Soccer Cleats", "Hiking Boots",
                "Gym Bag", "Water Bottle", "Shaker Bottle", "Gym Towel", "Jump Rope",
                "Yoga Blocks", "Yoga Strap", "Balance Ball", "Kettlebell", "Medicine Ball",
                "Bike Helmet", "Cycling Gloves", "Sports Watch", "Heart Rate Monitor", "Pedometer",
                "Tennis Racket", "Badminton Set", "Basketball", "Soccer Ball", "Volleyball",
                "Swim Goggles", "Swim Cap", "Snorkel Set", "Camping Tent", "Sleeping Bag",
                "Backpack", "Hiking Poles", "Compression Shorts", "Sports Bra", "Athletic Socks"
            ],
            "brands": ["ZenFit", "SpeedRunner", "ActiveGear", "FitPro", "AthleteZone", "SportElite"]
        },
        "Beauty & Personal Care": {
            "items": [
                "Face Moisturizer", "Face Wash", "Toner", "Serum", "Eye Cream",
                "Sunscreen", "Body Lotion", "Hand Cream", "Lip Balm", "Face Mask",
                "Shampoo", "Conditioner", "Hair Mask", "Hair Oil", "Styling Gel",
                "Toothbrush", "Toothpaste", "Mouthwash", "Dental Floss", "Electric Toothbrush",
                "Makeup Remover", "Cleanser", "Exfoliator", "Night Cream", "BB Cream",
                "Perfume", "Cologne", "Deodorant", "Body Spray", "Body Wash",
                "Razor", "Shaving Cream", "Aftershave", "Nail Clipper", "Tweezers"
            ],
            "brands": ["BeautyNature", "GlowSkin", "PureEssence", "FreshCare", "LuxeBeauty", "NaturalGlow"]
        },
        "Books & Media": {
            "items": [
                "Fiction Novel", "Mystery Novel", "Romance Novel", "Sci-Fi Novel", "Fantasy Novel",
                "Biography", "Self-Help Book", "Cookbook", "Travel Guide", "History Book",
                "Children's Book", "Comic Book", "Graphic Novel", "Poetry Book", "Art Book",
                "Educational DVD", "Movie Collection", "Music Album", "Audiobook", "E-Reader",
                "Notebook", "Journal", "Planner", "Sketchbook", "Coloring Book",
                "Bookmark", "Book Light", "Reading Glasses", "Book Stand", "Bookends"
            ],
            "brands": ["ReadMore", "ClassicReads", "ModernMedia", "BookHub", "StoryWorld", "PageTurner"]
        },
        "Toys & Games": {
            "items": [
                "Board Game", "Card Game", "Puzzle", "Building Blocks", "Action Figures",
                "Doll", "Plush Toy", "Remote Control Car", "Drone", "Robot Toy",
                "Art Set", "Craft Kit", "Science Kit", "Magic Set", "Musical Instrument",
                "Basketball Hoop", "Soccer Goal", "Frisbee", "Kite", "Bubble Machine",
                "Educational Toy", "Baby Rattle", "Stacking Toys", "Shape Sorter", "Play Kitchen",
                "Video Game", "Gaming Console", "Controller", "Gaming Headset", "Game Card"
            ],
            "brands": ["PlayFun", "ToyWorld", "GameMaster", "KidJoy", "FunTime", "CreativePlay"]
        },
        "Office Supplies": {
            "items": [
                "Notebook", "Sticky Notes", "Index Cards", "Legal Pad", "Graph Paper",
                "Pen Set", "Pencil Set", "Markers", "Highlighters", "Crayons",
                "Stapler", "Paper Clips", "Binder Clips", "Rubber Bands", "Push Pins",
                "Tape Dispenser", "Scissors", "Paper Cutter", "Hole Punch", "Calculator",
                "File Folders", "Binders", "Sheet Protectors", "Dividers", "Labels",
                "Desk Organizer", "Drawer Organizer", "Pen Holder", "Paper Tray", "Calendar"
            ],
            "brands": ["OfficePro", "WorkSpace", "DeskMate", "Stationery+", "OfficeHub", "PaperWorks"]
        }
    }

    products = []
    product_id = 1

    for category, data in product_data.items():
        items = data["items"]
        brands = data["brands"]

        for item in items:
            if product_id > count:
                break

            # Generate realistic price based on category
            if category == "Electronics":
                base_price = random.uniform(19.99, 299.99)
            elif category == "Clothing":
                base_price = random.uniform(9.99, 89.99)
            elif category == "Home & Kitchen":
                base_price = random.uniform(14.99, 199.99)
            elif category == "Sports & Fitness":
                base_price = random.uniform(12.99, 149.99)
            elif category == "Beauty & Personal Care":
                base_price = random.uniform(7.99, 79.99)
            elif category == "Books & Media":
                base_price = random.uniform(9.99, 49.99)
            elif category == "Toys & Games":
                base_price = random.uniform(14.99, 99.99)
            else:  # Office Supplies
                base_price = random.uniform(4.99, 59.99)

            price = round(base_price, 2)
            stock = random.randint(0, 200)
            rating = round(random.uniform(3.5, 5.0), 1)
            brand = random.choice(brands)

            # Generate description
            quality_words = ["Premium", "High-quality", "Professional", "Deluxe", "Essential"]
            feature_words = ["durable", "comfortable", "efficient", "reliable", "versatile"]

            description = f"{random.choice(quality_words)} {item.lower()} - {random.choice(feature_words)} and perfect for daily use"

            product = {
                "id": f"P{product_id:06d}",
                "name": item,
                "category": category,
                "price": price,
                "stock": stock,
                "description": description,
                "brand": brand,
                "rating": rating
            }

            products.append(product)
            product_id += 1

        if product_id > count:
            break

    return products


def load_products(conn, count=300):
    """Generate and load products into database."""
    print(f"Generating and loading {count} products...")

    products = generate_products(count)

    cursor = conn.cursor()
    batch = []

    for product in products:
        batch.append((
            product['id'],
            product['name'],
            product['category'],
            product['price'],
            product['stock'],
            product['description'],
            product['brand'],
            product['rating']
        ))

    cursor.executemany("""
        INSERT OR REPLACE INTO products (id, name, category, price, stock, description, brand, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, batch)

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

    ORDER_STATUSES = ["pending", "processing", "shipped", "delivered"]

    # Get all users
    cursor = conn.cursor()
    cursor.execute("SELECT id, member_since FROM users")
    users = [(row[0], row[1]) for row in cursor.fetchall()]

    if not users:
        print("Error: No users found in database")
        return

    # Get all products from database
    cursor.execute("SELECT id, price FROM products")
    products = [{"id": row[0], "price": row[1]} for row in cursor.fetchall()]

    if not products:
        print("Error: No products found in database")
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
            product = random.choice(products)
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
        load_products(conn, count=300)
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
