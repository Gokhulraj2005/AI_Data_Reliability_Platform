"""Schema and required-value checks."""


def check_schema(
    records: list[dict[str, object]], required_columns: tuple[str, ...]
) -> list[str]:
    if not records:
        return ["Dataset is empty"]
    available = set().union(*(record.keys() for record in records))
    return [f"Missing required column: {column}"
            for column in required_columns if column not in available]


def find_missing_values(
    records: list[dict[str, object]], required_columns: tuple[str, ...]
) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    for index, record in enumerate(records):
        for column in required_columns:
            if record.get(column) is None or record.get(column) == "":
                issues.append({"row": index + 1, "column": column})
    return issues
