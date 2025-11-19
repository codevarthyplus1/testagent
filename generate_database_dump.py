#!/usr/bin/env python3
"""
Generate a database dump with 1000+ users and 100k+ orders
Creates both JSON files and SQL dump file
"""

import json
import random
from datetime import datetime, timedelta


# Sample data for generation
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
    "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Frank", "Rachel", "Alexander", "Catherine", "Patrick", "Carolyn", "Raymond", "Janet",
    "Jack", "Ruth", "Dennis", "Maria", "Jerry", "Heather", "Tyler", "Diane",
    "Aaron", "Virginia", "Jose", "Julie", "Adam", "Joyce", "Henry", "Victoria",
    "Nathan", "Olivia", "Douglas", "Kelly", "Zachary", "Christina", "Peter", "Lauren",
    "Kyle", "Joan", "Walter", "Evelyn", "Ethan", "Judith", "Jeremy", "Megan",
    "Harold", "Cheryl", "Keith", "Andrea", "Christian", "Hannah", "Roger", "Martha",
    "Noah", "Jacqueline", "Gerald", "Frances", "Carl", "Gloria", "Terry", "Ann",
    "Sean", "Teresa", "Austin", "Kathryn", "Arthur", "Sara", "Lawrence", "Janice",
    "Jesse", "Jean", "Dylan", "Alice", "Bryan", "Madison", "Joe", "Doris",
    "Jordan", "Abigail", "Billy", "Julia", "Bruce", "Judy", "Albert", "Grace",
    "Willie", "Denise", "Gabriel", "Amber", "Logan", "Marilyn", "Alan", "Beverly",
    "Juan", "Danielle", "Wayne", "Theresa", "Roy", "Sophia", "Ralph", "Marie",
    "Randy", "Diana", "Eugene", "Brittany", "Vincent", "Natalie", "Russell", "Isabella",
    "Louis", "Charlotte", "Philip", "Rose", "Bobby", "Alexis", "Johnny", "Kayla"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell",
    "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher",
    "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham",
    "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant",
    "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray",
    "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "McDonald", "Woods",
    "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb",
    "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter",
    "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz",
    "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd",
    "Rose", "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice",
    "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens", "Soto", "Weaver",
    "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins"
]

CITIES = [
    ("New York", "NY", "10001"), ("Los Angeles", "CA", "90001"), ("Chicago", "IL", "60601"),
    ("Houston", "TX", "77001"), ("Phoenix", "AZ", "85001"), ("Philadelphia", "PA", "19101"),
    ("San Antonio", "TX", "78201"), ("San Diego", "CA", "92101"), ("Dallas", "TX", "75201"),
    ("San Jose", "CA", "95101"), ("Austin", "TX", "78701"), ("Jacksonville", "FL", "32099"),
    ("Fort Worth", "TX", "76101"), ("Columbus", "OH", "43004"), ("San Francisco", "CA", "94101"),
    ("Charlotte", "NC", "28201"), ("Indianapolis", "IN", "46201"), ("Seattle", "WA", "98101"),
    ("Denver", "CO", "80201"), ("Washington", "DC", "20001"), ("Boston", "MA", "02101"),
    ("Nashville", "TN", "37201"), ("Oklahoma City", "OK", "73101"), ("Las Vegas", "NV", "89101"),
    ("Portland", "OR", "97201"), ("Detroit", "MI", "48201"), ("Memphis", "TN", "38101"),
    ("Louisville", "KY", "40201"), ("Baltimore", "MD", "21201"), ("Milwaukee", "WI", "53201"),
    ("Albuquerque", "NM", "87101"), ("Tucson", "AZ", "85701"), ("Fresno", "CA", "93650"),
    ("Sacramento", "CA", "94203"), ("Kansas City", "MO", "64101"), ("Mesa", "AZ", "85201"),
    ("Atlanta", "GA", "30301"), ("Omaha", "NE", "68101"), ("Colorado Springs", "CO", "80901"),
    ("Raleigh", "NC", "27601"), ("Miami", "FL", "33101"), ("Virginia Beach", "VA", "23450"),
    ("Oakland", "CA", "94601"), ("Minneapolis", "MN", "55401"), ("Tulsa", "OK", "74101"),
    ("Tampa", "FL", "33601"), ("Arlington", "TX", "76010"), ("New Orleans", "LA", "70112"),
    ("Wichita", "KS", "67201"), ("Cleveland", "OH", "44101"), ("Bakersfield", "CA", "93301")
]

STREET_NAMES = [
    "Main St", "Oak Ave", "Maple St", "Cedar Ln", "Pine Rd", "Elm St", "Washington Ave",
    "Lake St", "Hill Rd", "Park Ave", "Sunset Blvd", "Broadway", "First St", "Second Ave",
    "Third St", "Church St", "Spring St", "River Rd", "Valley Dr", "Forest Ave",
    "Meadow Ln", "Highland Ave", "Franklin St", "Jefferson Ave", "Madison St", "Monroe Dr",
    "Adams St", "Lincoln Ave", "Wilson Rd", "Jackson St", "Grant Ave", "College St",
    "Market St", "Water St", "Mill Rd", "Bridge St", "Bay St", "School St", "Walnut St",
    "Chestnut St", "Cherry St", "Dogwood Dr", "Willow Ln", "Birch St", "Sycamore Ave"
]

ORDER_STATUSES = ["pending", "processing", "shipped", "delivered"]

PRODUCTS = [
    {"id": "P001", "price": 79.99},
    {"id": "P002", "price": 24.99},
    {"id": "P003", "price": 19.99},
    {"id": "P004", "price": 49.99},
    {"id": "P005", "price": 34.99},
    {"id": "P006", "price": 89.99},
    {"id": "P007", "price": 94.99},
    {"id": "P008", "price": 39.99}
]


def generate_email(first_name, last_name, user_id):
    """Generate a unique email address."""
    domains = ["email.com", "mail.com", "example.com", "webmail.com", "inbox.com"]
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name[0].lower()}{last_name.lower()}",
        f"{first_name.lower()}{last_name[0].lower()}",
        f"{first_name.lower()}.{last_name[0].lower()}",
        f"{first_name.lower()}{user_id}"
    ]
    pattern = random.choice(patterns)
    domain = random.choice(domains)
    return f"{pattern}@{domain}"


def generate_phone():
    """Generate a phone number."""
    return f"555-{random.randint(1000, 9999)}"


def generate_street_address():
    """Generate a street address."""
    number = random.randint(100, 9999)
    street = random.choice(STREET_NAMES)
    return f"{number} {street}"


def generate_member_since():
    """Generate a random member_since date in the past 3 years."""
    days_ago = random.randint(0, 1095)  # 3 years
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y-%m-%d")


def generate_users(count):
    """Generate specified number of users."""
    print(f"Generating {count} users...")
    users = []

    for i in range(1, count + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        city, state, base_zip = random.choice(CITIES)

        # Add variation to zip codes
        zip_code = str(int(base_zip) + random.randint(0, 99))

        user = {
            "id": f"U{i:06d}",
            "name": f"{first_name} {last_name}",
            "email": generate_email(first_name, last_name, i),
            "phone": generate_phone(),
            "address": {
                "street": generate_street_address(),
                "city": city,
                "state": state,
                "zip": zip_code
            },
            "member_since": generate_member_since()
        }
        users.append(user)

        if i % 10000 == 0:
            print(f"  Generated {i} users...")

    return users


def generate_order_date(user_member_since):
    """Generate order date after user joined."""
    member_date = datetime.strptime(user_member_since, "%Y-%m-%d")
    today = datetime.now()

    # Order must be after member date
    days_range = (today - member_date).days
    if days_range < 1:
        days_range = 1

    days_ago = random.randint(0, min(days_range, 365))  # Within last year or since joining
    order_date = today - timedelta(days=days_ago)
    return order_date.strftime("%Y-%m-%d")


def calculate_order_totals(items):
    """Calculate subtotal, tax, shipping, and total."""
    subtotal = sum(item["quantity"] * item["price"] for item in items)
    tax = round(subtotal * 0.08, 2)  # 8% tax

    # Shipping based on subtotal
    if subtotal > 100:
        shipping = 0.0
    elif subtotal > 50:
        shipping = 5.99
    else:
        shipping = 7.99

    total = round(subtotal + tax + shipping, 2)

    return {
        "subtotal": round(subtotal, 2),
        "tax": tax,
        "shipping": shipping,
        "total": total
    }


def generate_orders(count, users):
    """Generate specified number of orders."""
    print(f"Generating {count} orders...")
    orders = []

    for i in range(1, count + 1):
        # Pick a random user
        user = random.choice(users)

        # Generate order items (1-5 items per order)
        num_items = random.randint(1, 5)
        items = []
        for _ in range(num_items):
            product = random.choice(PRODUCTS)
            quantity = random.randint(1, 3)
            items.append({
                "product_id": product["id"],
                "quantity": quantity,
                "price": product["price"]
            })

        # Calculate totals
        totals = calculate_order_totals(items)

        order_date = generate_order_date(user["member_since"])
        status = random.choice(ORDER_STATUSES)

        order = {
            "id": f"ORD{i:06d}",
            "user_id": user["id"],
            "order_date": order_date,
            "status": status,
            "items": items,
            "subtotal": totals["subtotal"],
            "tax": totals["tax"],
            "shipping": totals["shipping"],
            "total": totals["total"],
            "shipping_address": user["address"].copy()
        }

        # Add tracking number for shipped/delivered orders
        if status in ["shipped", "delivered"]:
            order["tracking_number"] = f"TRK{random.randint(100000000, 999999999)}"

            order_dt = datetime.strptime(order_date, "%Y-%m-%d")
            shipped_date = order_dt + timedelta(days=random.randint(1, 3))
            order["shipped_date"] = shipped_date.strftime("%Y-%m-%d")

            if status == "delivered":
                delivered_date = shipped_date + timedelta(days=random.randint(2, 7))
                order["delivered_date"] = delivered_date.strftime("%Y-%m-%d")

        orders.append(order)

        if i % 10000 == 0:
            print(f"  Generated {i} orders...")

    return orders


def create_sql_dump(users, orders, products, output_file):
    """Create SQL dump file."""
    print(f"Creating SQL dump file: {output_file}")

    with open(output_file, 'w') as f:
        # Header
        f.write("-- Shopping Cart Database Dump\n")
        f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- Users: {len(users)}\n")
        f.write(f"-- Orders: {len(orders)}\n")
        f.write("--\n\n")

        # Create tables
        f.write("-- Create tables\n\n")

        f.write("CREATE TABLE IF NOT EXISTS users (\n")
        f.write("  id VARCHAR(10) PRIMARY KEY,\n")
        f.write("  name VARCHAR(100) NOT NULL,\n")
        f.write("  email VARCHAR(100) UNIQUE NOT NULL,\n")
        f.write("  phone VARCHAR(20),\n")
        f.write("  street VARCHAR(200),\n")
        f.write("  city VARCHAR(100),\n")
        f.write("  state VARCHAR(2),\n")
        f.write("  zip VARCHAR(10),\n")
        f.write("  member_since DATE\n")
        f.write(");\n\n")

        f.write("CREATE TABLE IF NOT EXISTS products (\n")
        f.write("  id VARCHAR(10) PRIMARY KEY,\n")
        f.write("  name VARCHAR(200) NOT NULL,\n")
        f.write("  category VARCHAR(50),\n")
        f.write("  price DECIMAL(10, 2) NOT NULL,\n")
        f.write("  stock INTEGER DEFAULT 0,\n")
        f.write("  description TEXT,\n")
        f.write("  brand VARCHAR(100),\n")
        f.write("  rating DECIMAL(3, 2)\n")
        f.write(");\n\n")

        f.write("CREATE TABLE IF NOT EXISTS orders (\n")
        f.write("  id VARCHAR(10) PRIMARY KEY,\n")
        f.write("  user_id VARCHAR(10) NOT NULL,\n")
        f.write("  order_date DATE NOT NULL,\n")
        f.write("  status VARCHAR(20) NOT NULL,\n")
        f.write("  subtotal DECIMAL(10, 2) NOT NULL,\n")
        f.write("  tax DECIMAL(10, 2) NOT NULL,\n")
        f.write("  shipping DECIMAL(10, 2) NOT NULL,\n")
        f.write("  total DECIMAL(10, 2) NOT NULL,\n")
        f.write("  shipping_street VARCHAR(200),\n")
        f.write("  shipping_city VARCHAR(100),\n")
        f.write("  shipping_state VARCHAR(2),\n")
        f.write("  shipping_zip VARCHAR(10),\n")
        f.write("  tracking_number VARCHAR(50),\n")
        f.write("  shipped_date DATE,\n")
        f.write("  delivered_date DATE,\n")
        f.write("  FOREIGN KEY (user_id) REFERENCES users(id)\n")
        f.write(");\n\n")

        f.write("CREATE TABLE IF NOT EXISTS order_items (\n")
        f.write("  id INTEGER PRIMARY KEY AUTO_INCREMENT,\n")
        f.write("  order_id VARCHAR(10) NOT NULL,\n")
        f.write("  product_id VARCHAR(10) NOT NULL,\n")
        f.write("  quantity INTEGER NOT NULL,\n")
        f.write("  price DECIMAL(10, 2) NOT NULL,\n")
        f.write("  FOREIGN KEY (order_id) REFERENCES orders(id),\n")
        f.write("  FOREIGN KEY (product_id) REFERENCES products(id)\n")
        f.write(");\n\n")

        # Insert products
        f.write("-- Insert products\n\n")
        f.write("INSERT INTO products (id, name, category, price, stock, description, brand, rating) VALUES\n")

        product_values = []
        for product in products:
            values = f"('{product['id']}', '{product['name']}', '{product['category']}', {product['price']}, {product['stock']}, '{product['description']}', '{product['brand']}', {product['rating']})"
            product_values.append(values)

        f.write(",\n".join(product_values))
        f.write(";\n\n")

        # Insert users in batches
        f.write("-- Insert users\n\n")
        batch_size = 1000
        for i in range(0, len(users), batch_size):
            batch = users[i:i + batch_size]
            f.write("INSERT INTO users (id, name, email, phone, street, city, state, zip, member_since) VALUES\n")

            user_values = []
            for user in batch:
                name = user['name'].replace("'", "''")
                email = user['email'].replace("'", "''")
                values = f"('{user['id']}', '{name}', '{email}', '{user['phone']}', '{user['address']['street']}', '{user['address']['city']}', '{user['address']['state']}', '{user['address']['zip']}', '{user['member_since']}')"
                user_values.append(values)

            f.write(",\n".join(user_values))
            f.write(";\n\n")

            if (i + batch_size) % 10000 == 0:
                print(f"  Written {i + batch_size} users to SQL...")

        # Insert orders in batches
        f.write("-- Insert orders\n\n")
        order_item_id = 1

        for i in range(0, len(orders), batch_size):
            batch = orders[i:i + batch_size]
            f.write("INSERT INTO orders (id, user_id, order_date, status, subtotal, tax, shipping, total, shipping_street, shipping_city, shipping_state, shipping_zip, tracking_number, shipped_date, delivered_date) VALUES\n")

            order_values = []
            for order in batch:
                tracking = order.get('tracking_number', 'NULL')
                if tracking != 'NULL':
                    tracking = f"'{tracking}'"

                shipped = order.get('shipped_date', 'NULL')
                if shipped != 'NULL':
                    shipped = f"'{shipped}'"

                delivered = order.get('delivered_date', 'NULL')
                if delivered != 'NULL':
                    delivered = f"'{delivered}'"

                values = f"('{order['id']}', '{order['user_id']}', '{order['order_date']}', '{order['status']}', {order['subtotal']}, {order['tax']}, {order['shipping']}, {order['total']}, '{order['shipping_address']['street']}', '{order['shipping_address']['city']}', '{order['shipping_address']['state']}', '{order['shipping_address']['zip']}', {tracking}, {shipped}, {delivered})"
                order_values.append(values)

            f.write(",\n".join(order_values))
            f.write(";\n\n")

            # Insert order items for this batch
            f.write("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES\n")

            item_values = []
            for order in batch:
                for item in order['items']:
                    values = f"('{order['id']}', '{item['product_id']}', {item['quantity']}, {item['price']})"
                    item_values.append(values)

            f.write(",\n".join(item_values))
            f.write(";\n\n")

            if (i + batch_size) % 10000 == 0:
                print(f"  Written {i + batch_size} orders to SQL...")

        # Create indexes for better performance
        f.write("-- Create indexes\n\n")
        f.write("CREATE INDEX idx_users_email ON users(email);\n")
        f.write("CREATE INDEX idx_orders_user_id ON orders(user_id);\n")
        f.write("CREATE INDEX idx_orders_status ON orders(status);\n")
        f.write("CREATE INDEX idx_orders_date ON orders(order_date);\n")
        f.write("CREATE INDEX idx_order_items_order_id ON order_items(order_id);\n")
        f.write("CREATE INDEX idx_order_items_product_id ON order_items(product_id);\n")

        f.write("\n-- End of dump\n")


def main():
    print("=" * 70)
    print("Shopping Cart Database Dump Generator")
    print("=" * 70)
    print()

    # Configuration
    NUM_USERS = 1000
    NUM_ORDERS = 100000

    # Load existing products
    print("Loading existing products...")
    with open('data/products.json', 'r') as f:
        products = json.load(f)

    # Generate data
    users = generate_users(NUM_USERS)
    orders = generate_orders(NUM_ORDERS, users)

    print()
    print("Creating output files...")

    # Create SQL dump
    create_sql_dump(users, orders, products, 'database_dump.sql')

    # Also save as JSON for reference
    print("Saving JSON files for reference...")
    with open('data/users_large.json', 'w') as f:
        json.dump(users[:100], f, indent=2)  # Save first 100 for reference

    with open('data/orders_large.json', 'w') as f:
        json.dump(orders[:100], f, indent=2)  # Save first 100 for reference

    print()
    print("=" * 70)
    print("Generation Complete!")
    print("=" * 70)
    print(f"Users generated: {len(users)}")
    print(f"Orders generated: {len(orders)}")
    print(f"Total order items: {sum(len(order['items']) for order in orders)}")
    print()
    print("Output files:")
    print("  - database_dump.sql (Full SQL database dump)")
    print("  - data/users_large.json (First 100 users for reference)")
    print("  - data/orders_large.json (First 100 orders for reference)")
    print()


if __name__ == "__main__":
    main()
