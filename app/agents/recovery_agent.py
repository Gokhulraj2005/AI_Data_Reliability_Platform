import os
import shutil
import json

from app.skills.schema_repair import repair_schema
from app.skills.missing_value_repair import repair_missing_values
from app.skills.duplicate_cleanup import remove_duplicates
from app.skills.data_validation_repair import validate_and_repair
from app.skills.anomaly_investigation import investigate_anomalies
from app.skills.approval_gateway import request_approval


INPUT_FILE = "data/corrupted/orders_corrupted.csv"
RECOVERY_DIR = "data/processed"
FINAL_FILE = "data/processed/orders_recovered.csv"
INCIDENT_FILE = "data/incidents.json"


def run_recovery(decision=None):

    print("\n" + "=" * 70)
    print("AI RECOVERY AGENT")
    print("=" * 70)

    os.makedirs(
        RECOVERY_DIR,
        exist_ok=True
    )

    current_file = INPUT_FILE

    # ---------------------------------------------------------
    # Load latest incident
    # ---------------------------------------------------------

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    if not incidents:

        print("\nNo incidents available.")

        return {
            "status": "FAILED"
        }

    incident = incidents[-1]

    incident_id = incident["incident_id"]

    print(
        f"\nIncident ID: {incident_id}"
    )

    print(
        f"Severity: {incident['severity']}"
    )

    # ---------------------------------------------------------
    # Get AI-selected skills
    # ---------------------------------------------------------

    if decision and decision.get("skills"):

        selected_skills = decision["skills"]

        print(
            "\nSkills selected by AI decision:"
        )

        for skill in selected_skills:

            print(
                f"  - {skill}"
            )

    else:

        print(
            "\nNo AI-selected skills available."
        )

        print(
            "Using detected incident issues."
        )

        selected_skills = []

        if "Schema Drift" in incident["issues"]:
            selected_skills.append(
                "schema_repair"
            )

        if "Missing Values" in incident["issues"]:
            selected_skills.append(
                "missing_value_repair"
            )

        if "Duplicate Records" in incident["issues"]:
            selected_skills.append(
                "duplicate_cleanup"
            )

        if "Invalid Values" in incident["issues"]:
            selected_skills.append(
                "data_validation_repair"
            )

        if "Data Anomaly" in incident["issues"]:
            selected_skills.append(
                "anomaly_investigation"
            )

    # ---------------------------------------------------------
    # Track ONLY skills actually executed
    # ---------------------------------------------------------

    executed_skills = []

    print(
        "\nHuman approval will be required "
        "before recovery actions."
    )

    # ---------------------------------------------------------
    # 1. Schema Repair
    # ---------------------------------------------------------

    if "schema_repair" in selected_skills:

        print("\n[1] Schema Repair")

        approved = request_approval(
            incident_id,
            "schema_repair",
            "Schema Drift",
            "HIGH"
        )

        if approved:

            schema_output = (
                "data/processed/"
                "recovery_step1_schema.csv"
            )

            repair_schema(
                current_file,
                schema_output
            )

            current_file = schema_output

            executed_skills.append(
                "schema_repair"
            )

        else:

            print(
                "\nSchema repair rejected."
            )

            print(
                "Recovery process stopped."
            )

            return {
                "status": "REJECTED",
                "rejected_skill": "schema_repair"
            }

    # ---------------------------------------------------------
    # 2. Missing Value Repair
    # ---------------------------------------------------------

    if "missing_value_repair" in selected_skills:

        print("\n[2] Missing Value Repair")

        approved = request_approval(
            incident_id,
            "missing_value_repair",
            "Missing Values",
            "MEDIUM"
        )

        if approved:

            missing_output = (
                "data/processed/"
                "recovery_step2_missing.csv"
            )

            repair_missing_values(
                current_file,
                missing_output
            )

            current_file = missing_output

            executed_skills.append(
                "missing_value_repair"
            )

        else:

            print(
                "\nMissing value repair rejected."
            )

            print(
                "Recovery process stopped."
            )

            return {
                "status": "REJECTED",
                "rejected_skill":
                    "missing_value_repair"
            }

    # ---------------------------------------------------------
    # 3. Duplicate Cleanup
    # ---------------------------------------------------------

    if "duplicate_cleanup" in selected_skills:

        print("\n[3] Duplicate Cleanup")

        approved = request_approval(
            incident_id,
            "duplicate_cleanup",
            "Duplicate Records",
            "MEDIUM"
        )

        if approved:

            duplicate_output = (
                "data/processed/"
                "recovery_step3_duplicates.csv"
            )

            remove_duplicates(
                current_file,
                duplicate_output
            )

            current_file = duplicate_output

            executed_skills.append(
                "duplicate_cleanup"
            )

        else:

            print(
                "\nDuplicate cleanup rejected."
            )

            print(
                "Recovery process stopped."
            )

            return {
                "status": "REJECTED",
                "rejected_skill":
                    "duplicate_cleanup"
            }

    # ---------------------------------------------------------
    # 4. Data Validation Repair
    # ---------------------------------------------------------

    if "data_validation_repair" in selected_skills:

        print("\n[4] Data Validation Repair")

        approved = request_approval(
            incident_id,
            "data_validation_repair",
            "Invalid Values",
            "HIGH"
        )

        if approved:

            validate_and_repair(
                current_file
            )

            current_file = (
                "data/processed/"
                "orders_after_validation_repair.csv"
            )

            executed_skills.append(
                "data_validation_repair"
            )

        else:

            print(
                "\nData validation repair rejected."
            )

            print(
                "Recovery process stopped."
            )

            return {
                "status": "REJECTED",
                "rejected_skill":
                    "data_validation_repair"
            }

    # ---------------------------------------------------------
    # 5. Data Anomaly Investigation
    # ---------------------------------------------------------

    if "anomaly_investigation" in selected_skills:

        print(
            "\n[5] Data Anomaly Investigation"
        )

        approved = request_approval(
            incident_id,
            "anomaly_investigation",
            "Data Anomaly",
            "HIGH"
        )

        if approved:

            anomaly_output = (
                "data/processed/"
                "orders_after_anomaly_investigation.csv"
            )

            investigate_anomalies(
                current_file,
                anomaly_output
            )

            current_file = anomaly_output

            executed_skills.append(
                "anomaly_investigation"
            )

        else:

            print(
                "\nAnomaly investigation rejected."
            )

            print(
                "Recovery process stopped."
            )

            return {
                "status": "REJECTED",
                "rejected_skill":
                    "anomaly_investigation"
            }

    # ---------------------------------------------------------
    # Create final recovered file
    # ---------------------------------------------------------

    shutil.copy(
        current_file,
        FINAL_FILE
    )

    print("\n" + "=" * 70)
    print("RECOVERY COMPLETED")
    print("=" * 70)

    print(
        "\nFinal recovered file:"
    )

    print(
        FINAL_FILE
    )

    print(
        "\nActually executed skills:"
    )

    for skill in executed_skills:

        print(
            f"  - {skill}"
        )

    print("=" * 70)

    return {
        "status": "SUCCESS",
        "file": FINAL_FILE,
        "executed_skills": executed_skills
    }


if __name__ == "__main__":

    result = run_recovery()

    print(
        "\nRecovery Result:"
    )

    print(
        result
    )