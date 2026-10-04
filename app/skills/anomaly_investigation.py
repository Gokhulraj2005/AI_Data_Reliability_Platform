import os
import pandas as pd


def investigate_anomalies(
    input_file,
    output_file
):
    """
    Investigate statistical anomalies in the dataset.

    The function detects price anomalies using the IQR method.
    It does NOT automatically change anomalous values.
    """

    print("\n" + "=" * 70)
    print("DATA ANOMALY INVESTIGATION")
    print("=" * 70)

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    df = pd.read_csv(input_file)

    if "price" not in df.columns:
        raise ValueError(
            "Required column 'price' not found."
        )

    # ---------------------------------------------------------
    # Calculate IQR boundaries
    # ---------------------------------------------------------

    q1 = df["price"].quantile(0.25)
    q3 = df["price"].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    # ---------------------------------------------------------
    # Detect anomalies
    # ---------------------------------------------------------

    anomaly_mask = (
        (df["price"] < lower_bound)
        |
        (df["price"] > upper_bound)
    )

    anomaly_count = int(
        anomaly_mask.sum()
    )

    # ---------------------------------------------------------
    # Display results
    # ---------------------------------------------------------

    print(f"\nTotal rows       : {len(df)}")
    print(f"Q1               : {q1:.2f}")
    print(f"Q3               : {q3:.2f}")
    print(f"IQR              : {iqr:.2f}")
    print(f"Lower boundary   : {lower_bound:.2f}")
    print(f"Upper boundary   : {upper_bound:.2f}")
    print(f"Anomalies found  : {anomaly_count}")

    # ---------------------------------------------------------
    # Safety rule
    # ---------------------------------------------------------

    print("\nSafety decision:")
    print(
        "Anomalous values will NOT be automatically modified."
    )

    print(
        "They require human/business validation."
    )

    # ---------------------------------------------------------
    # Preserve the dataset unchanged
    # ---------------------------------------------------------

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("\nAnomaly investigation completed.")

    print(
        f"Output file: {output_file}"
    )

    print("=" * 70)

    return {
        "status": "INVESTIGATED",
        "anomaly_count": anomaly_count,
        "lower_bound": float(lower_bound),
        "upper_bound": float(upper_bound),
        "output_file": output_file,
        "modified": False
    }


if __name__ == "__main__":

    result = investigate_anomalies(
        "data/corrupted/orders_corrupted.csv",
        "data/processed/orders_after_anomaly_investigation.csv"
    )

    print("\nInvestigation Result:")
    print(result)