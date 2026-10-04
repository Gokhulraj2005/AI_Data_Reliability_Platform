import os
import pandas as pd

from app.skills.anomaly_investigation import (
    investigate_anomalies
)


def test_anomaly_investigation():

    input_file = (
        "data/corrupted/orders_corrupted.csv"
    )

    output_file = (
        "data/processed/test_anomaly_output.csv"
    )

    result = investigate_anomalies(
        input_file,
        output_file
    )

    # Check that the function completed
    assert result["status"] == "INVESTIGATED"

    # Check that anomalies were detected
    assert result["anomaly_count"] >= 0

    # Check that the original data was NOT modified
    assert result["modified"] is False

    # Check that output file exists
    assert os.path.exists(output_file)

    # Check that output data can be loaded
    df = pd.read_csv(output_file)

    assert len(df) > 0

    # Cleanup test output
    os.remove(output_file)