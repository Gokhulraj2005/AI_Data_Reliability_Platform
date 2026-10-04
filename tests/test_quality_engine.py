import json
import os

from app.quality.quality_engine import run_quality_check


INCIDENT_FILE = "data/incidents.json"


def test_quality_engine():

    run_quality_check()

    assert os.path.exists(INCIDENT_FILE)

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    assert len(incidents) > 0

    latest_incident = incidents[-1]

    assert "incident_id" in latest_incident
    assert "severity" in latest_incident
    assert "status" in latest_incident
    assert "quality_score" in latest_incident
    assert "issues" in latest_incident

    assert latest_incident["quality_score"] < 100

    expected_issues = [
        "Schema Drift",
        "Missing Values",
        "Duplicate Records",
        "Invalid Values",
        "Data Anomaly"
    ]

    for issue in expected_issues:
        assert issue in latest_incident["issues"]