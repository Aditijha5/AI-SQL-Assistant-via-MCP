"""
Database Initialization Script
Creates SQLite database with realistic business data.

Schema:
- customers: Business clients with geographic distribution
- products: Product catalog with pricing
- orders: Transaction history linking customers to products
"""

import sqlite3
from datetime import datetime, timedelta
import random

def create_database():
    """Initialize SQLite database with schema and seed data."""
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    # Drop existing tables to ensure clean state
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS customers')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    
    # Create orders table with foreign keys
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Seed customers - realistic business client names
    customers = [
        ('Acme Corporation', 'USA'),
        ('TechVision Inc', 'USA'),
        ('Global Traders Ltd', 'UK'),
        ('Nordic Solutions AB', 'Sweden'),
        ('Pacific Imports', 'Australia'),
        ('Euro Dynamics GmbH', 'Germany'),
        ('Nexus Enterprises', 'Canada'),
        ('Apex Industries', 'USA'),
        ('Quantum Systems', 'UK'),
        ('Fusion Partners', 'France'),
        ('Summit Trading Co', 'Japan'),
        ('Velocity Group', 'USA'),
        ('Horizon Ventures', 'Singapore'),
        ('Zenith Corporation', 'USA'),
        ('Atlas Commerce', 'Netherlands')
    ]
    
    cursor.executemany('INSERT INTO customers (name, country) VALUES (?, ?)', customers)
    
    # Seed products - B2B product catalog
    products = [
        ('Enterprise Software License', 2499.99),
        ('Cloud Storage (1TB/year)', 599.99),
        ('Consulting Package (20h)', 3999.99),
        ('Hardware Server Unit', 8999.99),
        ('Security Audit Service', 1499.99),
        ('Training Workshop', 899.99),
        ('API Integration Bundle', 1999.99),
        ('Premium Support Plan', 4999.99),
        ('Data Analytics Platform', 6499.99),
        ('Mobile App Development', 12999.99)
    ]
    
    cursor.executemany('INSERT INTO products (name, price) VALUES (?, ?)', products)
    
    # Seed orders - realistic transaction patterns over 12 months
    # Create varying purchase patterns: some customers are heavy buyers, others occasional
    base_date = datetime.now() - timedelta(days=365)
    orders = []
    
    # High-value customers (frequent, large orders)
    heavy_customers = [1, 2, 7, 12, 14]  # Customer IDs
    for customer_id in heavy_customers:
        for month in range(12):
            num_orders = random.randint(3, 6)  # 3-6 orders per month
            for _ in range(num_orders):
                days_offset = month * 30 + random.randint(0, 28)
                order_date = base_date + timedelta(days=days_offset)
                product_id = random.randint(1, 10)
                quantity = random.randint(1, 5)
                orders.append((customer_id, product_id, quantity, order_date.strftime('%Y-%m-%d')))
    
    # Medium-value customers (regular orders)
    medium_customers = [3, 5, 8, 10, 13]
    for customer_id in medium_customers:
        for month in range(12):
            if random.random() < 0.7:  # 70% chance of order each month
                num_orders = random.randint(1, 3)
                for _ in range(num_orders):
                    days_offset = month * 30 + random.randint(0, 28)
                    order_date = base_date + timedelta(days=days_offset)
                    product_id = random.randint(1, 10)
                    quantity = random.randint(1, 3)
                    orders.append((customer_id, product_id, quantity, order_date.strftime('%Y-%m-%d')))
    
    # Low-value customers (occasional orders)
    low_customers = [4, 6, 9, 11, 15]
    for customer_id in low_customers:
        num_orders = random.randint(2, 8)  # Few orders total
        for _ in range(num_orders):
            days_offset = random.randint(0, 365)
            order_date = base_date + timedelta(days=days_offset)
            product_id = random.randint(1, 10)
            quantity = random.randint(1, 2)
            orders.append((customer_id, product_id, quantity, order_date.strftime('%Y-%m-%d')))
    
    # Add declining customer pattern (high activity first 6 months, then drops)
    declining_customer = 7
    for month in range(6):
        num_orders = random.randint(4, 6)
        for _ in range(num_orders):
            days_offset = month * 30 + random.randint(0, 28)
            order_date = base_date + timedelta(days=days_offset)
            product_id = random.randint(1, 10)
            quantity = random.randint(2, 5)
            orders.append((declining_customer, product_id, quantity, order_date.strftime('%Y-%m-%d')))
    
    # Insert all orders
    cursor.executemany(
        'INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)',
        orders
    )
    
    conn.commit()
    
    # Print summary statistics
    cursor.execute('SELECT COUNT(*) FROM customers')
    print(f"✓ Created {cursor.fetchone()[0]} customers")
    
    cursor.execute('SELECT COUNT(*) FROM products')
    print(f"✓ Created {cursor.fetchone()[0]} products")
    
    cursor.execute('SELECT COUNT(*) FROM orders')
    print(f"✓ Created {cursor.fetchone()[0]} orders")
    
    conn.close()
    print("\n✓ Database initialized successfully: db.sqlite")

if __name__ == '__main__':
    create_database()
