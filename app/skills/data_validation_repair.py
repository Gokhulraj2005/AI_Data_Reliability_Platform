import os
import pandas as pd


INPUT_FILE = "data/corrupted/orders_corrupted.csv"

CLEAN_OUTPUT = (
    "data/processed/orders_after_validation_repair.csv"
)

QUARANTINE_OUTPUT = (
    "data/processed/orders_quarantine.csv"
)


def validate_and_repair(input_file):
    """Detect invalid business values and quarantine them."""

    print("\n" + "=" * 60)
    print("RECOVERY SKILL: DATA VALIDATION REPAIR")
    print("=" * 60)

    # --------------------------------------------
    # Load data
    # --------------------------------------------

    df = pd.read_csv(input_file)

    print(f"\nRecords loaded: {len(df)}")

    # --------------------------------------------
    # Business validation rules
    # --------------------------------------------

    invalid_quantity = (
        df["quantity"].notna()
        & (df["quantity"] <= 0)
    )

    invalid_discount = (
        df["discount"].notna()
        & (
            (df["discount"] < 0)
            | (df["discount"] > 100)
        )
    )

    invalid_price = (
        df["price"].notna()
        & (df["price"] <= 0)
    )

    # --------------------------------------------
    # Combine invalid conditions
    # --------------------------------------------

    invalid_records = (
        invalid_quantity
        | invalid_discount
        | invalid_price
    )

    quarantine_df = df[
        invalid_records
    ].copy()

    clean_df = df[
        ~invalid_records
    ].copy()

    # --------------------------------------------
    # Report
    # --------------------------------------------

    print(
        f"\nInvalid quantity records : "
        f"{invalid_quantity.sum()}"
    )

    print(
        f"Invalid discount records: "
        f"{invalid_discount.sum()}"
    )

    print(
        f"Invalid price records   : "
        f"{invalid_price.sum()}"
    )

    print(
        f"\nTotal records quarantined: "
        f"{len(quarantine_df)}"
    )

    print(
        f"Valid records remaining: "
        f"{len(clean_df)}"
    )

    # --------------------------------------------
    # Create directories
    # --------------------------------------------

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    # --------------------------------------------
    # Save clean data
    # --------------------------------------------

    clean_df.to_csv(
        CLEAN_OUTPUT,
        index=False
    )

    # --------------------------------------------
    # Save quarantine data
    # --------------------------------------------

    quarantine_df.to_csv(
        QUARANTINE_OUTPUT,
        index=False
    )

    # --------------------------------------------
    # Verify clean data
    # --------------------------------------------

    remaining_invalid_quantity = int(
        (
            clean_df["quantity"].notna()
            & (clean_df["quantity"] <= 0)
        ).sum()
    )

    remaining_invalid_discount = int(
        (
            clean_df["discount"].notna()
            & (
                (clean_df["discount"] < 0)
                | (clean_df["discount"] > 100)
            )
        ).sum()
    )

    remaining_invalid_price = int(
        (
            clean_df["price"].notna()
            & (clean_df["price"] <= 0)
        ).sum()
    )

    total_remaining_invalid = (
        remaining_invalid_quantity
        + remaining_invalid_discount
        + remaining_invalid_price
    )

    print(
        f"\nRemaining invalid records: "
        f"{total_remaining_invalid}"
    )

    print(
        f"\nClean output:"
    )

    print(CLEAN_OUTPUT)

    print(
        f"\nQuarantine output:"
    )

    print(QUARANTINE_OUTPUT)

    # --------------------------------------------
    # Final status
    # --------------------------------------------

    if total_remaining_invalid == 0:

        status = "SUCCESS"

    else:

        status = "FAILED"

    print("\n" + "=" * 60)
    print(
        f"DATA VALIDATION REPAIR {status}"
    )
    print("=" * 60)

    return {
        "status": status,
        "invalid_records": len(quarantine_df),
        "clean_records": len(clean_df),
        "quarantine_file": QUARANTINE_OUTPUT
    }


if __name__ == "__main__":

    result = validate_and_repair(
        INPUT_FILE
    )

    print("\nRecovery Result:")
    print(result)