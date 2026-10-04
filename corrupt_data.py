import os
import random
import pandas as pd
import numpy as np

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

RAW_DIR = "data/raw"
CORRUPTED_DIR = "data/corrupted"

random.seed(42)
np.random.seed(42)

os.makedirs(CORRUPTED_DIR, exist_ok=True)


# --------------------------------------------------
# LOAD CLEAN DATA
# --------------------------------------------------

customers = pd.read_csv(f"{RAW_DIR}/customers.csv")
products = pd.read_csv(f"{RAW_DIR}/products.csv")
orders = pd.read_csv(f"{RAW_DIR}/orders.csv")

print("Clean data loaded successfully.")
print(f"Customers: {customers.shape}")
print(f"Products : {products.shape}")
print(f"Orders   : {orders.shape}")


# ==================================================
# 1. MISSING VALUES
# ==================================================

print("\n[1] Adding missing values...")

missing_indices = np.random.choice(
    orders.index,
    size=500,
    replace=False
)

orders.loc[missing_indices[:250], "quantity"] = np.nan
orders.loc[missing_indices[250:], "discount"] = np.nan

print("Added missing values to quantity and discount.")


# ==================================================
# 2. DUPLICATE ORDERS
# ==================================================

print("\n[2] Adding duplicate records...")

duplicate_rows = orders.sample(
    n=300,
    random_state=42
)

orders = pd.concat(
    [orders, duplicate_rows],
    ignore_index=True
)

print("Added 300 duplicate order records.")


# ==================================================
# 3. INVALID VALUES
# ==================================================

print("\n[3] Adding invalid values...")

# Negative quantities
negative_indices = np.random.choice(
    orders.index,
    size=100,
    replace=False
)

orders.loc[negative_indices, "quantity"] = -1

# Invalid discount values
discount_indices = np.random.choice(
    orders.index,
    size=100,
    replace=False
)

orders.loc[discount_indices, "discount"] = 150

print("Added negative quantities and invalid discounts.")


# ==================================================
# 4. EXTREME / ANOMALOUS VALUES
# ==================================================

print("\n[4] Adding anomalous values...")

anomaly_indices = np.random.choice(
    orders.index,
    size=50,
    replace=False
)

orders.loc[anomaly_indices, "price"] = 999999

orders.loc[anomaly_indices, "total_amount"] = (
    orders.loc[anomaly_indices, "quantity"].fillna(1)
    * 999999
)

print("Added extreme price anomalies.")


# ==================================================
# 5. SCHEMA DRIFT
# ==================================================

print("\n[5] Introducing schema drift...")

# Rename a column
orders.rename(
    columns={"customer_id": "cust_id"},
    inplace=True
)

# Add a new unexpected column
orders["order_source"] = np.random.choice(
    ["Website", "Mobile", "Store"],
    size=len(orders)
)

print("Renamed customer_id → cust_id")
print("Added unexpected column: order_source")


# ==================================================
# SAVE CORRUPTED DATA
# ==================================================

output_path = f"{CORRUPTED_DIR}/orders_corrupted.csv"

orders.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 50)
print("CORRUPTED DATA CREATED SUCCESSFULLY")
print("=" * 50)

print(f"File: {output_path}")
print(f"Rows: {len(orders)}")
print(f"Columns: {len(orders.columns)}")

print("\nMissing values:")
print(orders.isnull().sum())

print("\nColumns:")
print(list(orders.columns))

print("\nFirst 5 rows:")
print(orders.head())