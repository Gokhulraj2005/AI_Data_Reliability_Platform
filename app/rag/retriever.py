import os


RUNBOOK_DIR = "knowledge/runbooks"


RUNBOOK_MAPPING = {
    "Schema Drift": "schema_drift.md",
    "Missing Values": "missing_values.md",
    "Duplicate Records": "duplicate_records.md",
    "Invalid Values": "invalid_values.md",
    "Data Anomaly": "data_anomaly.md"
}


def retrieve_runbooks(incident):

    print("\n" + "-" * 70)
    print("RAG KNOWLEDGE RETRIEVAL")
    print("-" * 70)

    retrieved = []

    issues = incident.get(
        "issues",
        []
    )

    for issue in issues:

        filename = RUNBOOK_MAPPING.get(
            issue
        )

        if filename is None:
            continue

        file_path = os.path.join(
            RUNBOOK_DIR,
            filename
        )

        if not os.path.exists(file_path):
            print(
                f"\nRunbook not found: {filename}"
            )
            continue

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            content = file.read()

        retrieved.append({
            "issue": issue,
            "file": filename,
            "content": content
        })

        print(
            f"\nRetrieved: {filename}"
        )

    print(
        f"\nTotal runbooks retrieved: "
        f"{len(retrieved)}"
    )

    return retrieved


if __name__ == "__main__":

    import json

    with open(
        "data/incidents.json",
        "r"
    ) as file:
        incidents = json.load(file)

    incident = incidents[-1]

    results = retrieve_runbooks(
        incident
    )

    print(
        f"\nRetrieved runbooks: {len(results)}"
    )