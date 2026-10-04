import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MOCK_LLM = os.getenv("MOCK_LLM", "true").lower() == "true"


def mock_analysis(incident, runbooks, skills):
    issues = incident.get("issues", [])

    return f"""
ROOT CAUSE:
The incident was caused by data quality issues detected in the
pipeline: {", ".join(issues)}.

EVIDENCE:
The incident manager detected the listed data quality problems
during pipeline validation.

RECOMMENDED RECOVERY ACTION:
Use the available recovery skills to repair the detected issues,
followed by post-recovery validation.

RISK LEVEL:
HIGH

HUMAN APPROVAL:
YES. Recovery actions should be approved before execution.
"""


def analyze_incident_with_llm(incident, runbooks, skills):

    if MOCK_LLM:
        print("\n[MOCK LLM MODE]")
        return mock_analysis(incident, runbooks, skills)

    runbook_text = "\n\n".join(
        [
            f"RUNBOOK: {item['file']}\n{item['content']}"
            for item in runbooks
        ]
    )

    skill_text = "\n".join(
        [str(skill) for skill in skills]
    )

    prompt = f"""
You are an AI Data Reliability Engineer.

Analyze the following data pipeline incident.

INCIDENT:
{json.dumps(incident, indent=2)}

AVAILABLE RUNBOOKS:
{runbook_text}

AVAILABLE RECOVERY SKILLS:
{skill_text}

Provide a concise investigation containing:

1. Root cause
2. Evidence
3. Recommended recovery action
4. Risk level
5. Whether human approval is required

Do not invent facts that are not present in the
incident, runbooks, or available skills.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=(
            "You are a careful data reliability "
            "incident investigation assistant."
        ),
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":
    print("LLM Investigation Agent is ready.")
    print(f"Mock LLM mode: {MOCK_LLM}")