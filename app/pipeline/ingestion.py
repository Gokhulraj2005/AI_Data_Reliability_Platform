"""CSV ingestion helpers."""

import csv
from pathlib import Path


def read_csv(path: str | Path) -> list[dict[str, str]]:
    """Load a CSV file as dictionaries, preserving source values as text."""
    with Path(path).open("r", newline="", encoding="utf-8-sig") as source:
        return list(csv.DictReader(source))
