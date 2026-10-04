from datetime import datetime
import json
import os


INCIDENT_FILE = "data/incidents.json"


def load_incidents():
    """Load existing incidents."""

    if not os.path.exists(INCIDENT_FILE):
        return []

    with open(INCIDENT_FILE, "r") as file:
        return json.load(file)


def save_incidents(incidents):
    """Save incidents to JSON."""

    os.makedirs("data", exist_ok=True)

    with open(INCIDENT_FILE, "w") as file:
        json.dump(
            incidents,
            file,
            indent=4
        )


def determine_severity(report):
    """Determine incident severity."""

    issue_count = 0

    if not report["schema"]["schema_valid"]:
        issue_count += 2

    if report["missing_values"]:
        issue_count += 1

    if report["duplicates"] > 0:
        issue_count += 1

    if report["invalid_values"]:
        issue_count += 2

    if report["anomalies"] > 0:
        issue_count += 1

    if issue_count >= 5:
        return "CRITICAL"

    if issue_count >= 3:
        return "HIGH"

    if issue_count >= 1:
        return "MEDIUM"

    return "LOW"


def create_incident(report):
    """Create an incident from a quality report."""

    incidents = load_incidents()

    incident_number = len(incidents) + 1

    incident_id = f"INC-{incident_number:04d}"

    severity = determine_severity(report)

    issues = []

    if not report["schema"]["schema_valid"]:
        issues.append("Schema Drift")

    if report["missing_values"]:
        issues.append("Missing Values")

    if report["duplicates"] > 0:
        issues.append("Duplicate Records")

    if report["invalid_values"]:
        issues.append("Invalid Values")

    if report["anomalies"] > 0:
        issues.append("Data Anomaly")

    incident = {
        "incident_id": incident_id,
        "created_at": datetime.now().isoformat(),
        "type": "DATA_QUALITY",
        "severity": severity,
        "status": "OPEN",
        "quality_score": report["quality_score"],
        "issues": issues
    }

    incidents.append(incident)

    save_incidents(incidents)

    return incident


def print_incident(incident):
    """Display incident information."""

    print("\n" + "=" * 60)
    print("DATA RELIABILITY INCIDENT")
    print("=" * 60)

    print(f"Incident ID : {incident['incident_id']}")
    print(f"Type        : {incident['type']}")
    print(f"Severity    : {incident['severity']}")
    print(f"Status      : {incident['status']}")
    print(f"Quality     : {incident['quality_score']}/100")

    print("\nDetected Issues:")

    for issue in incident["issues"]:
        print(f"  ❌ {issue}")

    print("=" * 60)


if __name__ == "__main__":

    # Import the quality engine
    from app.quality.quality_engine import run_quality_checks

    file_path = "data/corrupted/orders_corrupted.csv"

    # Run quality checks
    report = run_quality_checks(file_path)

    # Create incident
    incident = create_incident(report)

    # Display incident
    print_incident(incident)