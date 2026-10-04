import os
import pandas as pd

from app.skills.schema_repair import repair_schema
from app.skills.missing_value_repair import repair_missing_values
from app.skills.duplicate_cleanup import remove_duplicates
from app.skills.data_validation_repair import validate_and_repair


INPUT_FILE = "data/corrupted/orders_corrupted.csv"


def test_schema_repair():

    output_file = "data/processed/test_schema.csv"

    repair_schema(
        INPUT_FILE,
        output_file
    )

    assert os.path.exists(output_file)

    df = pd.read_csv(output_file)

    assert "customer_id" in df.columns

    os.remove(output_file)


def test_missing_value_repair():

    output_file = "data/processed/test_missing.csv"

    repair_missing_values(
        INPUT_FILE,
        output_file
    )

    assert os.path.exists(output_file)

    df = pd.read_csv(output_file)

    assert df["quantity"].isna().sum() == 0
    assert df["discount"].isna().sum() == 0

    os.remove(output_file)


def test_duplicate_cleanup():

    output_file = "data/processed/test_duplicates.csv"

    remove_duplicates(
        INPUT_FILE,
        output_file
    )

    assert os.path.exists(output_file)

    df = pd.read_csv(output_file)

    assert df.duplicated().sum() == 0

    os.remove(output_file)


def test_data_validation_repair():

    validate_and_repair(
        INPUT_FILE
    )

    output_file = (
        "data/processed/"
        "orders_after_validation_repair.csv"
    )

    assert os.path.exists(output_file)

    df = pd.read_csv(output_file)

    assert (
        (df["quantity"] <= 0).sum()
        == 0
    )

    assert (
        (df["discount"] < 0).sum()
        == 0
    )

    assert (
        (df["discount"] > 100).sum()
        == 0
    )