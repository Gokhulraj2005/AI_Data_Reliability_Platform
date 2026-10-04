
import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 200
NUM_ORDERS = 50000

OUTPUT_DIR = "data/raw"

# Make results reproducible
random.seed(42)
np.random.seed(42)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 1. GENERATE CUSTOMERS
# ============================================================

print("Generating customers...")

first_names = [
    "Arun", "Priya", "Rahul", "Karthik", "Ananya",
    "Vijay", "Divya", "Rohit", "Sneha", "Aakash",
    "Meena", "Sanjay", "Nithya", "Hari", "Keerthi",
    "Aditya", "Pooja", "Vishal", "Swetha", "Manoj"
]

cities = [
    "Chennai",
    "Bangalore",
    "Mumbai",
    "Delhi",
    "Hyderabad",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Coimbatore",
    "Jaipur"
]

customer_rows = []

start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 9, 30)

for i in range(1, NUM_CUSTOMERS + 1):

    customer_id = f"C{i:05d}"

    name = random.choice(first_names)

    age = random.randint(18, 65)

    city = random.choice(cities)

    signup_days = (end_date - start_date).days

    signup_date = start_date + timedelta(
        days=random.randint(0, signup_days)
    )

    customer_rows.append({
        "customer_id": customer_id,
        "name": name,
        "age": age,
        "city": city,
        "signup_date": signup_date.strftime("%Y-%m-%d")
    })


customers_df = pd.DataFrame(customer_rows)

customers_path = os.path.join(
    OUTPUT_DIR,
    "customers.csv"
)

customers_df.to_csv(
    customers_path,
    index=False
)


# ============================================================
# 2. GENERATE PRODUCTS
# ============================================================

print("Generating products...")

categories = {
    "Electronics": [
        "Laptop",
        "Smartphone",
        "Tablet",
        "Headphones",
        "Keyboard",
        "Mouse",
        "Monitor",
        "Smartwatch"
    ],

    "Fashion": [
        "T-Shirt",
        "Jeans",
        "Shoes",
        "Jacket",
        "Backpack",
        "Sunglasses"
    ],

    "Home": [
        "Chair",
        "Table",
        "Lamp",
        "Pillow",
        "Bedsheet",
        "Curtains"
    ],

    "Beauty": [
        "Face Wash",
        "Shampoo",
        "Perfume",
        "Moisturizer",
        "Hair Oil"
    ],

    "Sports": [
        "Cricket Bat",
        "Football",
        "Tennis Racket",
        "Running Shoes",
        "Yoga Mat"
    ]
}

product_rows = []

product_id = 1

for category, product_names in categories.items():

    for product_name in product_names:

        # Create multiple variants of each product
        variants = random.randint(5, 10)

        for variant in range(variants):

            if product_id > NUM_PRODUCTS:
                break

            pid = f"P{product_id:04d}"

            price = round(
                random.uniform(500, 100000),
                2
            )

            stock = random.randint(10, 500)

            product_rows.append({
                "product_id": pid,
                "product_name": f"{product_name} {variant + 1}",
                "category": category,
                "price": price,
                "stock": stock
            })

            product_id += 1

        if product_id > NUM_PRODUCTS:
            break

    if product_id > NUM_PRODUCTS:
        break


products_df = pd.DataFrame(product_rows)

products_path = os.path.join(
    OUTPUT_DIR,
    "products.csv"
)

products_df.to_csv(
    products_path,
    index=False
)


# ============================================================
# 3. GENERATE ORDERS
# ============================================================

print("Generating 50,000 orders...")

order_rows = []

order_start_date = datetime(2025, 1, 1)
order_end_date = datetime(2026, 9, 30)

customer_ids = customers_df["customer_id"].tolist()

product_ids = products_df["product_id"].tolist()

# Create product price lookup
product_price_lookup = dict(
    zip(
        products_df["product_id"],
        products_df["price"]
    )
)

date_range_days = (
    order_end_date - order_start_date
).days


for i in range(1, NUM_ORDERS + 1):

    order_id = f"O{i:06d}"

    customer_id = random.choice(
        customer_ids
    )

    product_id = random.choice(
        product_ids
    )

    order_date = (
        order_start_date
        + timedelta(
            days=random.randint(
                0,
                date_range_days
            )
        )
    )

    quantity = random.randint(1, 5)

    price = product_price_lookup[product_id]

    discount = random.choice([
        0,
        0,
        0,
        5,
        10,
        15,
        20
    ])

    subtotal = quantity * price

    total_amount = subtotal * (
        1 - discount / 100
    )

    order_rows.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "product_id": product_id,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "quantity": quantity,
        "price": round(price, 2),
        "discount": discount,
        "total_amount": round(total_amount, 2)
    })


orders_df = pd.DataFrame(order_rows)

orders_path = os.path.join(
    OUTPUT_DIR,
    "orders.csv"
)

orders_df.to_csv(
    orders_path,
    index=False
)


# ============================================================
# 4. PRINT SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATA GENERATION COMPLETED")
print("=" * 60)

print(f"\nCustomers : {len(customers_df):,}")
print(f"Products  : {len(products_df):,}")
print(f"Orders    : {len(orders_df):,}")

print("\nFiles created:")

print(f"✓ {customers_path}")
print(f"✓ {products_path}")
print(f"✓ {orders_path}")

print("\nCustomer columns:")
print(list(customers_df.columns))

print("\nProduct columns:")
print(list(products_df.columns))

print("\nOrder columns:")
print(list(orders_df.columns))

print("\nFirst 5 orders:")
print(orders_df.head())

print("\nTotal revenue:")
print(
    f"₹{orders_df['total_amount'].sum():,.2f}"
)

print("\n" + "=" * 60)
print("Ready for the Data Reliability Pipeline!")
print("=" * 60)