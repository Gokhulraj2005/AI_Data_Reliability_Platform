
import os
import pandas as pd


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


def validate_recovered_data(file_path):

    print("\n" + "=" * 70)
    print("POST-RECOVERY VALIDATION")
    print("=" * 70)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Recovered file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print(f"\nFile: {file_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    results = {}

    # --------------------------------------------------
    # 1. Schema Validation
    # --------------------------------------------------

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    results["schema"] = bool(
        len(missing_columns) == 0
    )

    print("\n[1] Schema Validation")

    if results["schema"]:
        print(
            "PASS - All expected columns are present."
        )
    else:
        print(
            f"FAIL - Missing columns: {missing_columns}"
        )

    # --------------------------------------------------
    # 2. Missing Value Validation
    # --------------------------------------------------

    required_columns = [
        "quantity",
        "discount"
    ]

    missing_values = int(
        df[required_columns]
        .isnull()
        .sum()
        .sum()
    )

    results["missing_values"] = bool(
        missing_values == 0
    )

    print("\n[2] Missing Value Validation")

    if results["missing_values"]:
        print(
            "PASS - No missing quantity/discount values."
        )
    else:
        print(
            f"FAIL - Missing values found: {missing_values}"
        )

    # --------------------------------------------------
    # 3. Duplicate Validation
    # --------------------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    results["duplicates"] = bool(
        duplicate_count == 0
    )

    print("\n[3] Duplicate Validation")

    if results["duplicates"]:
        print(
            "PASS - No duplicate records found."
        )
    else:
        print(
            f"FAIL - Duplicate records found: "
            f"{duplicate_count}"
        )

    # --------------------------------------------------
    # 4. Invalid Value Validation
    # --------------------------------------------------

    invalid_quantity = int(
        (
            df["quantity"].notna()
            & (df["quantity"] <= 0)
        ).sum()
    )

    invalid_discount = int(
        (
            df["discount"].notna()
            & (
                (df["discount"] < 0)
                | (df["discount"] > 100)
            )
        ).sum()
    )

    results["invalid_values"] = bool(
        invalid_quantity == 0
        and invalid_discount == 0
    )

    print("\n[4] Invalid Value Validation")

    if results["invalid_values"]:
        print(
            "PASS - No invalid quantity/discount values."
        )
    else:
        print(
            f"FAIL - Invalid quantities: "
            f"{invalid_quantity}, "
            f"Invalid discounts: "
            f"{invalid_discount}"
        )

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    overall_pass = bool(
        all(results.values())
    )

    print("\n" + "-" * 70)

    if overall_pass:
        print("FINAL RESULT: PASS")
        print(
            "Recovered data is ready for "
            "the next pipeline stage."
        )
    else:
        print("FINAL RESULT: FAIL")
        print(
            "Recovered data still contains "
            "quality issues."
        )

    print("=" * 70)

    return {
        "status": "PASS" if overall_pass else "FAIL",
        "checks": results,
        "rows": int(len(df)),
        "duplicate_count": duplicate_count,
        "missing_values": missing_values,
        "invalid_quantity": invalid_quantity,
        "invalid_discount": invalid_discount
    }


if __name__ == "__main__":

    file_path = (
        "data/processed/"
        "orders_recovered.csv"
    )

    validate_recovered_data(file_path)
