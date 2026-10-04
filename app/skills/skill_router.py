import json
import os


INCIDENT_FILE = "data/incidents.json"


# --------------------------------------------------
# SKILL DEFINITIONS
# --------------------------------------------------

SKILLS = {
    "Schema Drift": {
        "skill_name": "schema_repair",
        "description": "Compare and repair incoming dataset schema.",
        "risk": "HIGH",
        "requires_approval": True
    },

    "Missing Values": {
        "skill_name": "missing_value_repair",
        "description": "Detect and handle missing values.",
        "risk": "MEDIUM",
        "requires_approval": True
    },

    "Duplicate Records": {
        "skill_name": "duplicate_cleanup",
        "description": "Identify and remove duplicate records.",
        "risk": "MEDIUM",
        "requires_approval": True
    },

    "Invalid Values": {
        "skill_name": "data_validation_repair",
        "description": "Validate and repair business-rule violations.",
        "risk": "HIGH",
        "requires_approval": True
    },

    "Data Anomaly": {
        "skill_name": "anomaly_investigation",
        "description": "Investigate extreme or unusual data values.",
        "risk": "HIGH",
        "requires_approval": True
    }
}


def load_latest_incident():
    """Load the latest incident."""

    if not os.path.exists(INCIDENT_FILE):
        raise FileNotFoundError(
            "No incident file found."
        )

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    if not incidents:
        raise ValueError(
            "No incidents available."
        )

    return incidents[-1]


def route_skills(incident):
    """Route incident issues to appropriate skills."""

    routed_skills = []

    for issue in incident["issues"]:

        if issue in SKILLS:

            skill = SKILLS[issue]

            routed_skills.append({
                "issue": issue,
                "skill_name": skill["skill_name"],
                "description": skill["description"],
                "risk": skill["risk"],
                "requires_approval": skill["requires_approval"]
            })

    return routed_skills


def print_routing(routed_skills):

    print("\n" + "=" * 60)
    print("AGENT SKILL ROUTER")
    print("=" * 60)

    for item in routed_skills:

        print("\nIssue:")
        print(f"  {item['issue']}")

        print("Selected Skill:")
        print(f"  {item['skill_name']}")

        print("Risk:")
        print(f"  {item['risk']}")

        print("Human Approval:")
        print(
            f"  {'YES' if item['requires_approval'] else 'NO'}"
        )

        print("-" * 60)


if __name__ == "__main__":

    incident = load_latest_incident()

    routed_skills = route_skills(
        incident
    )

    print_routing(
        routed_skills
    )