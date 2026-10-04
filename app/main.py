
from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="AI Data Reliability Platform",
    description=(
        "Agentic AI platform for data pipeline reliability, "
        "incident investigation, human approval, and autonomous recovery."
    ),
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "AI Data Reliability Platform API",
        "status": "running"
    }
