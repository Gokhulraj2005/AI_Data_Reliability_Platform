import json
import os
from datetime import datetime


APPROVAL_FILE = "data/approval_log.json"


def request_approval(
    incident_id,
    skill_name,
    issue,
    risk
):
    print("\n" + "=" * 60)
    print("HUMAN APPROVAL REQUIRED")
    print("=" * 60)

    print(f"Incident ID : {incident_id}")
    print(f"Issue       : {issue}")
    print(f"Recovery    : {skill_name}")
    print(f"Risk Level  : {risk}")

    print("\nThis recovery action requires human approval.")

    while True:

        decision = input(
            "\nApprove this recovery action? [Y/N]: "
        ).strip().upper()

        if decision in ["Y", "N"]:
            break

        print("Please enter Y or N.")

    approved = decision == "Y"

    approval_record = {
        "incident_id": incident_id,
        "skill_name": skill_name,
        "issue": issue,
        "risk": risk,
        "decision": "APPROVED" if approved else "REJECTED",
        "approved": bool(approved),
        "timestamp": datetime.now().isoformat()
    }

    os.makedirs("data", exist_ok=True)

    approvals = []

    if os.path.exists(APPROVAL_FILE):

        try:
            with open(
                APPROVAL_FILE,
                "r"
            ) as file:
                approvals = json.load(file)

        except json.JSONDecodeError:
            approvals = []

    approvals.append(approval_record)

    with open(
        APPROVAL_FILE,
        "w"
    ) as file:

        json.dump(
            approvals,
            file,
            indent=4
        )

    print("\n" + "-" * 60)

    if approved:
        print("APPROVAL RESULT: APPROVED")
    else:
        print("APPROVAL RESULT: REJECTED")

    print("-" * 60)

    return approved


if __name__ == "__main__":

    result = request_approval(
        "INC-0001",
        "schema_repair",
        "Schema Drift",
        "HIGH"
    )

    print(f"\nReturned value: {result}")