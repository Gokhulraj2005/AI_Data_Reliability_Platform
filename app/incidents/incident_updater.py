import json
import os
from datetime import datetime


INCIDENT_FILE = "data/incidents.json"


def update_incident_status(
    validation_result,
    decision=None,
    recovery_result=None
):

    if not os.path.exists(INCIDENT_FILE):
        raise FileNotFoundError(
            "Incident file not found."
        )

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    if not incidents:
        raise ValueError(
            "No incidents available."
        )

    incident = incidents[-1]

    # ---------------------------------------------------------
    # Update incident status
    # ---------------------------------------------------------

    if validation_result["status"] == "PASS":

        incident["status"] = "RESOLVED"

        incident["resolution"] = (
            "Data recovery completed successfully "
            "and post-recovery validation passed."
        )

    else:

        incident["status"] = "ESCALATED"

        incident["resolution"] = (
            "Post-recovery validation failed. "
            "Manual investigation required."
        )

    # ---------------------------------------------------------
    # Store timestamp
    # ---------------------------------------------------------

    incident["updated_at"] = (
        datetime.now().isoformat()
    )

    # ---------------------------------------------------------
    # Store validation result
    # ---------------------------------------------------------

    incident["validation_result"] = (
        validation_result
    )

    # ---------------------------------------------------------
    # Store AI decision
    # ---------------------------------------------------------

    if decision:

        incident["ai_decision"] = {
            "investigation": decision.get(
                "investigation"
            ),
            "llm_analysis": decision.get(
                "llm_analysis"
            ),
            "selected_skills": decision.get(
                "skills",
                []
            )
        }

    # ---------------------------------------------------------
    # Store recovery audit
    # ---------------------------------------------------------

    if recovery_result:

        incident["recovery_audit"] = {
            "status": recovery_result.get(
                "status"
            ),
            "executed_skills": recovery_result.get(
                "executed_skills",
                []
            ),
            "recovered_file": recovery_result.get(
                "file"
            )
        }

    # ---------------------------------------------------------
    # Save incident
    # ---------------------------------------------------------

    with open(INCIDENT_FILE, "w") as file:

        json.dump(
            incidents,
            file,
            indent=4
        )

    # ---------------------------------------------------------
    # Display result
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("INCIDENT STATUS UPDATED")
    print("=" * 70)

    print(
        f"Incident ID : "
        f"{incident['incident_id']}"
    )

    print(
        f"New Status  : "
        f"{incident['status']}"
    )

    print(
        f"Resolution  : "
        f"{incident['resolution']}"
    )

    if decision:

        print(
            "\nAI decision stored: YES"
        )

    if recovery_result:

        print(
            "Recovery audit stored: YES"
        )

    print("=" * 70)

    return incident


def update_incident_rejection(
    incident_id,
    rejected_skill
):

    if not os.path.exists(INCIDENT_FILE):
        raise FileNotFoundError(
            "Incident file not found."
        )

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    if not incidents:
        raise ValueError(
            "No incidents available."
        )

    incident = incidents[-1]

    incident["status"] = "ESCALATED"

    incident["resolution"] = (
        "Recovery action was rejected by "
        "human approval. Manual investigation "
        "is required."
    )

    incident["rejected_skill"] = (
        rejected_skill
    )

    incident["updated_at"] = (
        datetime.now().isoformat()
    )

    # Store rejection audit
    incident["recovery_audit"] = {
        "status": "REJECTED",
        "rejected_skill": rejected_skill
    }

    with open(INCIDENT_FILE, "w") as file:

        json.dump(
            incidents,
            file,
            indent=4
        )

    print("\n" + "=" * 70)
    print("INCIDENT ESCALATED")
    print("=" * 70)

    print(
        f"Incident ID : {incident_id}"
    )

    print(
        "Status      : ESCALATED"
    )

    print(
        f"Rejected Skill : {rejected_skill}"
    )

    print(
        "Reason      : Human approval rejected recovery."
    )

    print("=" * 70)

    return incident