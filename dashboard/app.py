
import json

import streamlit as st


INCIDENT_FILE = "data/incidents.json"


st.set_page_config(
    page_title="AI Data Reliability Platform",
    page_icon="🤖",
    layout="wide"
)


def load_incidents():

    try:
        with open(INCIDENT_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


# --------------------------------------------------
# Load data
# --------------------------------------------------

incidents = load_incidents()


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🤖 AI Data Reliability Platform")

st.write(
    "Agentic AI platform for data pipeline reliability, "
    "incident investigation, human approval, and recovery."
)


if not incidents:

    st.warning("No incidents found.")
    st.stop()


latest = incidents[-1]


# --------------------------------------------------
# Metrics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Incidents",
        len(incidents)
    )


with col2:
    st.metric(
        "Latest Incident",
        latest["incident_id"]
    )


with col3:
    st.metric(
        "Quality Score",
        f"{latest['quality_score']}/100"
    )


with col4:
    st.metric(
        "Status",
        latest["status"]
    )


st.divider()


# --------------------------------------------------
# Latest Incident
# --------------------------------------------------

st.header("Latest Incident")


col1, col2 = st.columns(2)


with col1:

    st.subheader("Incident Information")

    st.write(
        f"**Incident ID:** {latest['incident_id']}"
    )

    st.write(
        f"**Type:** {latest['type']}"
    )

    st.write(
        f"**Severity:** {latest['severity']}"
    )

    st.write(
        f"**Status:** {latest['status']}"
    )

    st.write(
        f"**Created:** {latest['created_at']}"
    )


with col2:

    st.subheader("Detected Issues")

    for issue in latest.get("issues", []):
        st.write(f"🔴 {issue}")


# --------------------------------------------------
# Validation Results
# --------------------------------------------------

st.divider()

st.header("Post-Recovery Validation")


validation = latest.get("validation_result")


if validation:

    checks = validation.get("checks", {})

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Schema",
            "PASS" if checks.get("schema") else "FAIL"
        )

    with col2:
        st.metric(
            "Missing Values",
            "PASS" if checks.get("missing_values") else "FAIL"
        )

    with col3:
        st.metric(
            "Duplicates",
            "PASS" if checks.get("duplicates") else "FAIL"
        )

    with col4:
        st.metric(
            "Invalid Values",
            "PASS" if checks.get("invalid_values") else "FAIL"
        )

    st.write(
        f"**Rows after recovery:** "
        f"{validation.get('rows', 0)}"
    )

    st.write(
        f"**Duplicate records:** "
        f"{validation.get('duplicate_count', 0)}"
    )

    st.write(
        f"**Missing values:** "
        f"{validation.get('missing_values', 0)}"
    )

else:

    st.info(
        "Post-recovery validation has not been recorded."
    )


# --------------------------------------------------
# Resolution
# --------------------------------------------------

st.divider()

st.header("Incident Resolution")


if latest.get("resolution"):

    st.success(
        latest["resolution"]
    )

else:

    st.info(
        "Incident has not been resolved yet."
    )


# --------------------------------------------------
# Incident History
# --------------------------------------------------

st.divider()

st.header("Incident History")


for incident in reversed(incidents):

    with st.expander(
        f"{incident['incident_id']} — "
        f"{incident['severity']} — "
        f"{incident['status']}"
    ):

        st.write(
            f"**Quality Score:** "
            f"{incident['quality_score']}/100"
        )

        st.write(
            "**Issues:**"
        )

        for issue in incident.get("issues", []):
            st.write(f"- {issue}")
