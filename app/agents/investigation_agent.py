import json
import os


INCIDENT_FILE = "data/incidents.json"


def load_latest_incident():
    """Load the latest incident."""

    if not os.path.exists(INCIDENT_FILE):
        raise FileNotFoundError(
            "No incident file found. Run the Incident Manager first."
        )

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    if not incidents:
        raise ValueError("No incidents found.")

    return incidents[-1]


def investigate_incident(incident):
    """Investigate the detected data-quality problems."""

    issues = incident["issues"]

    findings = []
    recommendations = []

    # --------------------------------------------
    # Schema Drift
    # --------------------------------------------

    if "Schema Drift" in issues:

        findings.append(
            "The incoming dataset schema differs from the expected schema."
        )

        recommendations.append(
            "Compare the incoming columns with the expected schema "
            "and restore renamed or missing columns."
        )

    # --------------------------------------------
    # Missing Values
    # --------------------------------------------

    if "Missing Values" in issues:

        findings.append(
            "Required fields contain missing values."
        )

        recommendations.append(
            "Identify affected columns and apply an appropriate "
            "missing-value handling strategy."
        )

    # --------------------------------------------
    # Duplicate Records
    # --------------------------------------------

    if "Duplicate Records" in issues:

        findings.append(
            "Duplicate records were detected in the dataset."
        )

        recommendations.append(
            "Identify duplicate records using the order identifier "
            "and remove duplicate entries."
        )

    # --------------------------------------------
    # Invalid Values
    # --------------------------------------------

    if "Invalid Values" in issues:

        findings.append(
            "One or more fields contain values that violate "
            "business validation rules."
        )

        recommendations.append(
            "Validate quantity, discount, and price values "
            "against predefined business rules."
        )

    # --------------------------------------------
    # Data Anomaly
    # --------------------------------------------

    if "Data Anomaly" in issues:

        findings.append(
            "Extreme values were detected in the dataset."
        )

        recommendations.append(
            "Investigate anomalous values and compare them "
            "with historical or expected ranges."
        )

    # --------------------------------------------
    # Determine action
    # --------------------------------------------

    if incident["severity"] == "CRITICAL":

        action = "REQUIRES_HUMAN_APPROVAL"

    elif incident["severity"] == "HIGH":

        action = "AUTOMATED_REMEDIATION_RECOMMENDED"

    else:

        action = "MONITOR"

    investigation = {
        "incident_id": incident["incident_id"],
        "severity": incident["severity"],
        "root_cause_categories": issues,
        "findings": findings,
        "recommendations": recommendations,
        "recommended_action": action
    }

    return investigation


def print_investigation(result):
    """Display investigation results."""

    print("\n" + "=" * 60)
    print("AI INVESTIGATION AGENT")
    print("=" * 60)

    print(f"Incident ID : {result['incident_id']}")
    print(f"Severity    : {result['severity']}")

    print("\nRoot Cause Categories:")

    for category in result["root_cause_categories"]:
        print(f"  • {category}")

    print("\nInvestigation Findings:")

    for finding in result["findings"]:
        print(f"  → {finding}")

    print("\nRecommended Actions:")

    for recommendation in result["recommendations"]:
        print(f"  → {recommendation}")

    print("\nRecommended Decision:")
    print(f"  {result['recommended_action']}")

    print("=" * 60)


if __name__ == "__main__":

    incident = load_latest_incident()

    investigation = investigate_incident(
        incident
    )

    print_investigation(
        investigation
    )