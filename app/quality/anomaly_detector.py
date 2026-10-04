"""Robust IQR-based numeric outlier detection."""


def detect_outliers(
    records: list[dict[str, object]], column: str, factor: float = 1.5
) -> list[dict[str, object]]:
    values: list[tuple[int, float]] = []
    for index, record in enumerate(records):
        try:
            value = float(record[column])
        except (KeyError, TypeError, ValueError):
            continue
        values.append((index + 1, value))
    if len(values) < 4:
        return []

    sorted_values = sorted(value for _, value in values)
    midpoint = len(sorted_values) // 2
    lower_half = sorted_values[:midpoint]
    upper_half = sorted_values[midpoint:] if len(sorted_values) % 2 == 0 else sorted_values[midpoint + 1:]
    q1 = _median(lower_half)
    q3 = _median(upper_half)
    spread = q3 - q1
    low, high = q1 - factor * spread, q3 + factor * spread
    return [{"row": row, "column": column, "value": value}
            for row, value in values if value < low or value > high]


def _median(values: list[float]) -> float:
    middle = len(values) // 2
    if len(values) % 2:
        return values[middle]
    return (values[middle - 1] + values[middle]) / 2
