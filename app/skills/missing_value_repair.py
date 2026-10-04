import os
import pandas as pd


INPUT_FILE = "data/corrupted/orders_corrupted.csv"
OUTPUT_FILE = "data/processed/orders_after_missing_value_repair.csv"


def repair_missing_values(input_file, output_file):
    """Repair missing values using predefined rules."""

    print("\n" + "=" * 60)
    print("RECOVERY SKILL: MISSING VALUE REPAIR")
    print("=" * 60)

    # Load data
    df = pd.read_csv(input_file)

    print(f"\nRecords loaded: {len(df)}")

    # --------------------------------------------
    # Check missing values
    # --------------------------------------------

    quantity_missing = int(
        df["quantity"].isna().sum()
    )

    discount_missing = int(
        df["discount"].isna().sum()
    )

    print(
        f"Missing quantity values : {quantity_missing}"
    )

    print(
        f"Missing discount values : {discount_missing}"
    )

    # --------------------------------------------
    # Repair quantity
    # --------------------------------------------

    if quantity_missing > 0:

        df["quantity"] = df["quantity"].fillna(1)

        print(
            "✓ Missing quantity values replaced with 1"
        )

    # --------------------------------------------
    # Repair discount
    # --------------------------------------------

    if discount_missing > 0:

        df["discount"] = df["discount"].fillna(0)

        print(
            "✓ Missing discount values replaced with 0"
        )

    # --------------------------------------------
    # Recalculate total amount
    # --------------------------------------------

    df["total_amount"] = (
        df["quantity"]
        * df["price"]
        * (1 - df["discount"] / 100)
    )

    print(
        "✓ Total amount recalculated"
    )

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

    # --------------------------------------------
    # Verify
    # --------------------------------------------

    remaining_missing = int(
        df[["quantity", "discount"]].isna().sum().sum()
    )

    print(
        f"\nRemaining missing values: {remaining_missing}"
    )

    print(f"Repaired file: {output_file}")

    print("\n" + "=" * 60)
    print("MISSING VALUE REPAIR COMPLETED")
    print("=" * 60)

    return {
        "status": "SUCCESS",
        "quantity_repaired": quantity_missing,
        "discount_repaired": discount_missing,
        "remaining_missing": remaining_missing
    }


if __name__ == "__main__":

    result = repair_missing_values(
        INPUT_FILE,
        OUTPUT_FILE
    )

    print("\nRecovery Result:")
    print(result)