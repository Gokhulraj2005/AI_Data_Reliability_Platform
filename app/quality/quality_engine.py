import os
import json
import pandas as pd
from datetime import datetime


INPUT_FILE = "data/corrupted/orders_corrupted.csv"
INCIDENT_FILE = "data/incidents.json"

EXPECTED_COLUMNS = [
    "order_id",
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "price",
    "discount",
    "total_amount"
]


def get_next_incident_id(incidents):

    if not incidents:
        return "INC-0001"

    last_id = incidents[-1]["incident_id"]

    number = int(last_id.split("-")[1])

    return f"INC-{number + 1:04d}"


def create_incident(quality_score, issues):

    if not issues:
        return None

    os.makedirs(
        os.path.dirname(INCIDENT_FILE),
        exist_ok=True
    )

    if os.path.exists(INCIDENT_FILE):

        with open(INCIDENT_FILE, "r") as file:
            incidents = json.load(file)

    else:
        incidents = []

    incident_id = get_next_incident_id(incidents)

    # Determine severity based on number of issue types
    if len(issues) >= 5:
        severity = "CRITICAL"
    elif len(issues) >= 3:
        severity = "HIGH"
    elif len(issues) >= 1:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    incident = {
        "incident_id": incident_id,
        "created_at": datetime.now().isoformat(),
        "type": "DATA_QUALITY",
        "severity": severity,
        "status": "OPEN",
        "quality_score": quality_score,
        "issues": issues
    }

    incidents.append(incident)

    with open(INCIDENT_FILE, "w") as file:
        json.dump(
            incidents,
            file,
            indent=4
        )

    print("\n" + "=" * 70)
    print("NEW INCIDENT CREATED")
    print("=" * 70)

    print(f"\nIncident ID : {incident_id}")
    print(f"Severity    : {severity}")
    print(f"Status      : OPEN")
    print(f"Quality     : {quality_score}/100")

    print("\nIssues:")

    for issue in issues:
        print(f"  - {issue}")

    print("=" * 70)

    return incident


def run_quality_check():

    print("\n" + "=" * 60)
    print("AI DATA RELIABILITY PLATFORM")
    print("DATA QUALITY ENGINE")
    print("=" * 60)

    print(f"\nLoading file: {INPUT_FILE}")

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    print("\n" + "-" * 60)
    print("DATA QUALITY REPORT")
    print("-" * 60)

    quality_score = 100
    issues = []

    # ---------------------------------------------------------
    # 1. Schema Check
    # ---------------------------------------------------------

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    unexpected_columns = [
        column
        for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    if missing_columns or unexpected_columns:

        print("❌ Schema: PROBLEM DETECTED")

        if missing_columns:
            print(
                f"   Missing columns: {missing_columns}"
            )

        if unexpected_columns:
            print(
                f"   Unexpected columns: {unexpected_columns}"
            )

        quality_score -= 20

        issues.append("Schema Drift")

    else:

        print("✅ Schema: PASS")

    # ---------------------------------------------------------
    # 2. Missing Values
    # ---------------------------------------------------------

    quantity_missing = int(
        df["quantity"].isna().sum()
    ) if "quantity" in df.columns else 0

    discount_missing = int(
        df["discount"].isna().sum()
    ) if "discount" in df.columns else 0

    if quantity_missing > 0 or discount_missing > 0:

        print("❌ Missing Values Detected")

        print(
            f"   quantity: {quantity_missing}"
        )

        print(
            f"   discount: {discount_missing}"
        )

        quality_score -= 20

        issues.append("Missing Values")

    else:

        print("✅ Missing Values: PASS")

    # ---------------------------------------------------------
    # 3. Duplicate Records
    # ---------------------------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        print(
            f"❌ Duplicate Records: {duplicate_count}"
        )

        quality_score -= 15

        issues.append("Duplicate Records")

    else:

        print("✅ Duplicate Records: PASS")

    # ---------------------------------------------------------
    # 4. Invalid Values
    # ---------------------------------------------------------

    invalid_quantity = 0
    invalid_discount = 0

    if "quantity" in df.columns:

        invalid_quantity = int(
            (df["quantity"] <= 0).sum()
        )

    if "discount" in df.columns:

        invalid_discount = int(
            (
                (df["discount"] < 0)
                |
                (df["discount"] > 100)
            ).sum()
        )

    if invalid_quantity > 0 or invalid_discount > 0:

        print("❌ Invalid Values Detected")

        print(
            f"   invalid_quantity: {invalid_quantity}"
        )

        print(
            f"   invalid_discount: {invalid_discount}"
        )

        quality_score -= 20

        issues.append("Invalid Values")

    else:

        print("✅ Invalid Values: PASS")

    # ---------------------------------------------------------
    # 5. Price Anomaly Detection
    # ---------------------------------------------------------

    price_anomalies = 0

    if "price" in df.columns:

        price_series = df["price"].dropna()

        if len(price_series) > 0:

            q1 = price_series.quantile(0.25)
            q3 = price_series.quantile(0.75)

            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            price_anomalies = int(
                (
                    (df["price"] < lower_bound)
                    |
                    (df["price"] > upper_bound)
                ).sum()
            )

    if price_anomalies > 0:

        print(
            f"⚠️ Price Anomalies Detected: "
            f"{price_anomalies}"
        )

        quality_score -= 15

        issues.append("Data Anomaly")

    else:

        print("✅ Price Anomalies: PASS")

    # ---------------------------------------------------------
    # Quality Score
    # ---------------------------------------------------------

    quality_score = max(
        quality_score,
        0
    )

    print("\n" + "-" * 60)

    print(
        f"DATA QUALITY SCORE: "
        f"{quality_score}/100"
    )

    print("-" * 60)

    # ---------------------------------------------------------
    # Create Incident
    # ---------------------------------------------------------

    if issues:

        create_incident(
            quality_score,
            issues
        )

    else:

        print("\n✅ DATA QUALITY CHECK PASSED")
        print("No incident created.")

    return {
        "quality_score": quality_score,
        "issues": issues
    }


if __name__ == "__main__":

    run_quality_check()