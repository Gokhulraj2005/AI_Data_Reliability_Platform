import json

from app.agents.incident_agent import run_incident_orchestrator
from app.agents.recovery_agent import run_recovery
from app.pipeline.validation import validate_recovered_data
from app.incidents.incident_updater import (
    update_incident_status,
    update_incident_rejection
)


INCIDENT_FILE = "data/incidents.json"


def get_latest_incident():

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    if not incidents:
        return None

    return incidents[-1]


def run_ai_workflow():

    print("\n" + "=" * 70)
    print("AUTONOMOUS DATA RELIABILITY WORKFLOW")
    print("=" * 70)

    # ---------------------------------------------------------
    # Get latest incident
    # ---------------------------------------------------------

    incident = get_latest_incident()

    if incident is None:

        print("\nNo incident available.")

        return

    print(
        f"\nLatest Incident : "
        f"{incident['incident_id']}"
    )

    print(
        f"Current Status  : "
        f"{incident['status']}"
    )

    # ---------------------------------------------------------
    # Prevent processing resolved incidents
    # ---------------------------------------------------------

    if incident["status"] == "RESOLVED":

        print("\n" + "=" * 70)
        print("WORKFLOW NOT STARTED")
        print("=" * 70)

        print(
            f"\nIncident {incident['incident_id']} "
            "is already RESOLVED."
        )

        print(
            "\nNo additional recovery action is required."
        )

        print("=" * 70)

        return

    # ---------------------------------------------------------
    # STEP 1: AI Incident Decision
    # ---------------------------------------------------------

    print("\nSTEP 1: AI INCIDENT DECISION")

    decision = run_incident_orchestrator()

    if decision is None:

        print("\nNo incident decision available.")

        return

    # ---------------------------------------------------------
    # Display AI-selected recovery skills
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("AI SELECTED RECOVERY SKILLS")
    print("-" * 70)

    selected_skills = decision.get(
        "skills",
        []
    )

    for skill in selected_skills:

        print(f"  - {skill}")

    # ---------------------------------------------------------
    # STEP 2: AI Recovery
    # ---------------------------------------------------------

    print("\nSTEP 2: AI RECOVERY")

    recovery_result = run_recovery(
        decision
    )

    # ---------------------------------------------------------
    # Handle rejected recovery
    # ---------------------------------------------------------

    if recovery_result["status"] == "REJECTED":

        rejected_skill = (
            recovery_result["rejected_skill"]
        )

        update_incident_rejection(
            incident["incident_id"],
            rejected_skill
        )

        print("\n" + "=" * 70)
        print("WORKFLOW STOPPED")
        print("=" * 70)

        print(
            "\nHuman approval rejected "
            "the recovery action."
        )

        print(
            "\nIncident has been escalated "
            "for manual investigation."
        )

        print("=" * 70)

        return

    # ---------------------------------------------------------
    # STEP 3: Post-Recovery Validation
    # ---------------------------------------------------------

    print("\nSTEP 3: POST-RECOVERY VALIDATION")

    recovered_file = recovery_result["file"]

    validation_result = validate_recovered_data(
        recovered_file
    )

    # ---------------------------------------------------------
    # STEP 4: Incident Status Update
    # ---------------------------------------------------------

    print("\nSTEP 4: INCIDENT STATUS UPDATE")

    updated_incident = update_incident_status(
        validation_result,
        decision,
        recovery_result
    )

    # ---------------------------------------------------------
    # Final Workflow Result
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("AI WORKFLOW COMPLETED")
    print("=" * 70)

    print(
        f"\nIncident : "
        f"{updated_incident['incident_id']}"
    )

    print(
        f"Status   : "
        f"{updated_incident['status']}"
    )

    print(
        f"Quality  : "
        f"{updated_incident['quality_score']}/100"
    )

    print("\nExecuted Recovery Skills:")

    for skill in recovery_result.get(
        "executed_skills",
        []
    ):

        print(f"  - {skill}")

    print(
        "\nAI decision stored: YES"
    )

    print(
        "Recovery audit stored: YES"
    )

    print("=" * 70)


if __name__ == "__main__":

    run_ai_workflow()