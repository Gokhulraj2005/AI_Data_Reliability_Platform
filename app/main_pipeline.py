from app.agents.recovery_agent import run_recovery
from app.pipeline.validation import validate_recovered_data
from app.incidents.incident_updater import (
    update_incident_status,
    update_incident_rejection
)


def run_pipeline():

    print("\n")
    print("=" * 70)
    print("AI DATA RELIABILITY PLATFORM")
    print("=" * 70)

    print("\nSTEP 1: DATA RECOVERY")

    recovery_result = run_recovery()

    # Handle rejected recovery
    if recovery_result["status"] == "REJECTED":

        print("\n" + "=" * 70)
        print("PIPELINE STOPPED")
        print("=" * 70)

        import json

        with open(
            "data/incidents.json",
            "r"
        ) as file:
            incidents = json.load(file)

        incident = incidents[-1]

        update_incident_rejection(
            incident["incident_id"],
            recovery_result["rejected_skill"]
        )

        print(
            "\nIncident has been escalated "
            "for manual investigation."
        )

        print("=" * 70)

        return

    # Recovery successful
    recovered_file = recovery_result["file"]

    print("\nSTEP 2: POST-RECOVERY VALIDATION")

    validation_result = validate_recovered_data(
        recovered_file
    )

    print("\nSTEP 3: INCIDENT STATUS UPDATE")

    incident = update_incident_status(
        validation_result
    )

    print("\n" + "=" * 70)
    print("PIPELINE FINAL RESULT")
    print("=" * 70)

    print(
        f"Incident : {incident['incident_id']}"
    )

    print(
        f"Status   : {incident['status']}"
    )

    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()