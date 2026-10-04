"""Small, predictable transformations for ingested records."""


def normalize_records(records: list[dict[str, object]]) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []
    for record in records:
        row = {str(key).strip(): value.strip() if isinstance(value, str) else value
               for key, value in record.items()}
        if "value" in row and row["value"] not in (None, ""):
            try:
                row["value"] = float(row["value"])
            except (TypeError, ValueError):
                pass
        normalized.append(row)
    return normalized
