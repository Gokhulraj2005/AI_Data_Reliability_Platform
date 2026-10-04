import json

from app.agents.investigation_agent import investigate_incident
from app.agents.llm_investigation_agent import analyze_incident_with_llm
from app.rag.retriever import retrieve_runbooks
from app.skills.skill_router import route_skills


INCIDENT_FILE = "data/incidents.json"


def run_incident_orchestrator():

    print("\n" + "=" * 70)
    print("AI INCIDENT ORCHESTRATOR")
    print("=" * 70)

    # --------------------------------------------------
    # Load latest incident
    # --------------------------------------------------

    with open(INCIDENT_FILE, "r") as file:
        incidents = json.load(file)

    if not incidents:
        print("\nNo incidents found.")
        return None

    incident = incidents[-1]

    print(f"\nIncident ID : {incident['incident_id']}")
    print(f"Severity    : {incident['severity']}")
    print(f"Status      : {incident['status']}")

    # --------------------------------------------------
    # STEP 1: Rule-Based AI Investigation
    # --------------------------------------------------

    print("\n[1] AI Investigation")

    investigation = investigate_incident(incident)

    print("\nInvestigation completed.")

    # --------------------------------------------------
    # STEP 2: RAG Runbook Retrieval
    # --------------------------------------------------

    print("\n[2] RAG Runbook Retrieval")

    runbooks = retrieve_runbooks(incident)

    print(f"Runbooks retrieved: {len(runbooks)}")

    # --------------------------------------------------
    # STEP 3: Recovery Skill Routing
    # --------------------------------------------------

    print("\n[3] Recovery Skill Routing")

    skills = route_skills(incident)

    print(f"Recovery skills identified: {len(skills)}")

    # --------------------------------------------------
    # STEP 4: LLM Investigation
    # --------------------------------------------------

    print("\n[4] LLM Investigation")

    llm_analysis = analyze_incident_with_llm(
        incident,
        runbooks,
        skills
    )

    print("\n===== LLM ANALYSIS =====")
    print(llm_analysis)

    # --------------------------------------------------
    # STEP 5: AI Decision Summary
    # --------------------------------------------------

    print("\n[5] AI Decision Summary")

    print(f"\nIncident: {incident['incident_id']}")
    print(f"Severity: {incident['severity']}")

    print("\nIssues detected:")

    for issue in incident.get("issues", []):
        print(f"  - {issue}")

    print("\nRecovery skills:")

    for skill in skills:
        print(f"  - {skill}")

    print("\nRAG runbooks:")

    for runbook in runbooks:
        print(f"  - {runbook['file']}")

    print("\n" + "=" * 70)
    print("AI INCIDENT DECISION COMPLETED")
    print("=" * 70)

    # --------------------------------------------------
    # Convert recovery skills into skill names
    # --------------------------------------------------

    skill_names = [
        skill["skill_name"]
        for skill in skills
    ]

    # --------------------------------------------------
    # Return complete AI decision
    # --------------------------------------------------

    return {
        "incident": incident,
        "investigation": investigation,
        "llm_analysis": llm_analysis,
        "runbooks": runbooks,
        "skills": skill_names
    }


if __name__ == "__main__":
    run_incident_orchestrator()