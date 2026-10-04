"""Append-only JSON Lines incident store."""

import json
from pathlib import Path

from config.settings import INCIDENTS_FILE


def save_incident(incident: dict[str, object], path: Path = INCIDENTS_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as destination:
        destination.write(json.dumps(incident, default=str) + "\n")


def list_incidents(path: Path = INCIDENTS_FILE) -> list[dict[str, object]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]
