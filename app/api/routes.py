from fastapi import APIRouter, HTTPException
import json

from app.agents.workflow_controller import run_ai_workflow


router = APIRouter()

INCIDENT_FILE = "data/incidents.json"


@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Data Reliability Platform"
    }


@router.get("/incidents")
def get_incidents():

    try:
        with open(INCIDENT_FILE, "r") as file:
            incidents = json.load(file)

        return {
            "count": len(incidents),
            "incidents": incidents
        }

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Incident file not found."
        )


@router.get("/incidents/latest")
def get_latest_incident():

    try:
        with open(INCIDENT_FILE, "r") as file:
            incidents = json.load(file)

        if not incidents:
            raise HTTPException(
                status_code=404,
                detail="No incidents found."
            )

        return incidents[-1]

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Incident file not found."
        )


@router.post("/workflow/run")
def run_workflow():

    try:
        run_ai_workflow()

        return {
            "status": "completed",
            "message": "AI reliability workflow executed successfully."
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )