import os
import pandas as pd


INPUT_FILE = "data/corrupted/orders_corrupted.csv"
OUTPUT_FILE = "data/processed/orders_after_schema_repair.csv"


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


COLUMN_MAPPING = {
    "cust_id": "customer_id"
}


def repair_schema(input_file, output_file):
    """Repair known schema changes."""

    print("\n" + "=" * 60)
    print("RECOVERY SKILL: SCHEMA REPAIR")
    print("=" * 60)

    # --------------------------------------------
    # Load data
    # --------------------------------------------

    df = pd.read_csv(input_file)

    print(f"\nRecords loaded: {len(df)}")

    print("\nIncoming columns:")
    print(list(df.columns))

    # --------------------------------------------
    # Detect known renamed columns
    # --------------------------------------------

    renamed_columns = []

    for old_name, new_name in COLUMN_MAPPING.items():

        if old_name in df.columns and new_name not in df.columns:

            df.rename(
                columns={
                    old_name: new_name
                },
                inplace=True
            )

            renamed_columns.append(
                f"{old_name} -> {new_name}"
            )

    # --------------------------------------------
    # Report changes
    # --------------------------------------------

    if renamed_columns:

        print("\nKnown schema changes repaired:")

        for change in renamed_columns:
            print(f"✓ {change}")

    else:

        print("\nNo known renamed columns detected.")

    # --------------------------------------------
    # Detect unexpected columns
    # --------------------------------------------

    unexpected_columns = [
        column
        for column in df.columns
        if column not in EXPECTED_COLUMNS
    ]

    if unexpected_columns:

        print("\nUnexpected columns detected:")

        for column in unexpected_columns:
            print(f"⚠ {column}")

        print(
            "\nUnexpected columns are being preserved "
            "for audit purposes."
        )

    # --------------------------------------------
    # Verify required columns
    # --------------------------------------------

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]

    print("\nSchema verification:")

    if missing_columns:

        print("❌ Required columns still missing:")

        for column in missing_columns:
            print(f"  - {column}")

        status = "FAILED"

    else:

        print("✓ All expected columns are present.")

        status = "SUCCESS"

    # --------------------------------------------
    # Save repaired data
    # --------------------------------------------

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(f"\nRepaired file:")
    print(output_file)

    print("\nFinal columns:")
    print(list(df.columns))

    print("\n" + "=" * 60)
    print(f"SCHEMA REPAIR {status}")
    print("=" * 60)

    return {
        "status": status,
        "renamed_columns": renamed_columns,
        "unexpected_columns": unexpected_columns,
        "missing_columns": missing_columns
    }


if __name__ == "__main__":

    result = repair_schema(
        INPUT_FILE,
        OUTPUT_FILE
    )

    print("\nRecovery Result:")
    print(result)