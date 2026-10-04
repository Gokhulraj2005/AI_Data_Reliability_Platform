import os
import pandas as pd


INPUT_FILE = "data/corrupted/orders_corrupted.csv"
OUTPUT_FILE = "data/processed/orders_after_duplicate_cleanup.csv"


def remove_duplicates(input_file, output_file):
    """Remove duplicate records from the dataset."""

    print("\n" + "=" * 60)
    print("RECOVERY SKILL: DUPLICATE CLEANUP")
    print("=" * 60)

    # Load data
    df = pd.read_csv(input_file)

    original_count = len(df)

    print(f"\nOriginal records: {original_count}")

    # Detect duplicates
    duplicate_count = int(df.duplicated().sum())

    print(f"Duplicate records detected: {duplicate_count}")

    if duplicate_count == 0:

        print("No duplicates found.")

        return {
            "status": "NO_ACTION",
            "original_records": original_count,
            "duplicates_removed": 0,
            "final_records": original_count
        }

    # Remove duplicates
    cleaned_df = df.drop_duplicates()

    final_count = len(cleaned_df)

    removed_count = original_count - final_count

    # Create output directory
    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    # Save repaired data
    cleaned_df.to_csv(
        output_file,
        index=False
    )

    print(f"Duplicates removed: {removed_count}")
    print(f"Final records: {final_count}")

    print(f"\nRepaired file:")
    print(output_file)

    print("\n" + "=" * 60)
    print("DUPLICATE CLEANUP COMPLETED")
    print("=" * 60)

    return {
        "status": "SUCCESS",
        "original_records": original_count,
        "duplicates_removed": removed_count,
        "final_records": final_count
    }


if __name__ == "__main__":

    result = remove_duplicates(
        INPUT_FILE,
        OUTPUT_FILE
    )

    print("\nRecovery Result:")
    print(result)