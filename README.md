# AI Data Reliability Platform

An **Agentic AI platform for data pipeline reliability, automated incident investigation, human-approved recovery, and post-recovery validation**.

The platform detects data-quality problems such as schema drift, missing values, duplicate records, invalid values, and statistical anomalies. It creates incidents, retrieves relevant recovery runbooks using RAG, routes recovery skills, requests human approval for potentially risky actions, executes recovery, validates the repaired dataset, and updates the incident lifecycle.

## Key Capabilities

- Automated data-quality monitoring
- Schema drift detection
- Missing-value detection and repair
- Duplicate-record detection and cleanup
- Invalid-value detection and quarantine
- Statistical anomaly investigation
- AI-based incident investigation
- RAG-based runbook retrieval
- Recovery skill routing
- Human-in-the-loop approval
- Automated recovery execution
- Post-recovery validation
- Incident audit trail
- FastAPI REST API
- Streamlit dashboard
- Docker containerization
- Automated Pytest test suite

## Architecture

```text
                 ┌─────────────────────┐
                 │    Data Sources     │
                 │     CSV / APIs      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Data Ingestion    │
                 │   & Transformation  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Data Quality Engine│
                 │ Schema / Missing /  │
                 │ Duplicate / Invalid │
                 │ Anomaly Detection   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Incident Manager   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ AI Investigation    │
                 │      Agent          │
                 └──────────┬──────────┘
                            │
                 ┌──────────▼──────────┐
                 │    RAG Runbooks     │
                 │ Investigation &     │
                 │ Recovery Guidance   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Skill Router      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Human Approval      │
                 │    Gateway          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Recovery Skills     │
                 │ Schema / Missing /   │
                 │ Duplicate / Invalid │
                 │ Anomaly Investigation│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Post-Recovery       │
                 │    Validation       │
                 └──────────┬──────────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
                 PASS            FAIL
                    │               │
                    ▼               ▼
                RESOLVED        ESCALATED
```

## Incident Lifecycle

```text
DATA QUALITY ISSUE
        │
        ▼
INCIDENT CREATED
        │
        ▼
AI INVESTIGATION
        │
        ▼
RAG RUNBOOK RETRIEVAL
        │
        ▼
RECOVERY SKILL ROUTING
        │
        ▼
HUMAN APPROVAL
        │
        ├── REJECTED ──────► ESCALATED
        │
        ▼
RECOVERY EXECUTION
        │
        ▼
POST-RECOVERY VALIDATION
        │
        ├── PASS ──────────► RESOLVED
        │
        └── FAIL ──────────► ESCALATED
```

## Data Quality Checks

The platform currently detects:

### 1. Schema Drift

Detects:

- Missing expected columns
- Unexpected columns
- Renamed columns

Example:

```text
Expected: customer_id
Detected: cust_id
```

The schema recovery skill maps known renamed fields back to the expected schema.

### 2. Missing Values

Detects missing values in important fields such as:

- `quantity`
- `discount`

The recovery skill applies conservative default values and recalculates dependent fields.

### 3. Duplicate Records

Detects duplicate rows and removes duplicates after human approval.

### 4. Invalid Values

Detects invalid business values such as:

- Quantity <= 0
- Discount < 0
- Discount > 100
- Price <= 0

Invalid records can be quarantined rather than silently deleted.

### 5. Statistical Anomalies

Uses the **Interquartile Range (IQR)** method to identify unusual numerical values.

Anomalous values are **not automatically modified** because an unusual value may represent a legitimate business event.

## AI Investigation

The incident investigation layer combines:

- Incident findings
- Detected issue types
- Recovery skills
- Local recovery runbooks
- LLM-based incident analysis

The platform supports both:

### Mock LLM Mode

Used for local development and testing without API costs.

Configure:

```text
MOCK_LLM=true
```

### LLM Mode

The platform can use an OpenAI-compatible client for LLM-based investigation.

Configure the API key through environment variables:

```text
OPENAI_API_KEY=your_api_key_here
MOCK_LLM=false
```

Never commit `.env` or API keys to GitHub.

## RAG Runbooks

The platform includes local recovery documentation for:

```text
knowledge/runbooks/
├── schema_drift.md
├── missing_values.md
├── duplicate_records.md
├── invalid_values.md
└── data_anomaly.md
```

The retriever selects relevant runbooks based on the detected incident issues.

## Recovery Skills

Current recovery skills include:

```text
schema_repair
missing_value_repair
duplicate_cleanup
data_validation_repair
anomaly_investigation
```

Each skill is independently implemented and can be routed by the skill router.

## Human-in-the-Loop Safety

Recovery actions require explicit human approval.

The approval gateway records:

- Incident ID
- Recovery skill
- Issue type
- Risk level
- Human decision
- Approval status
- Timestamp

Example:

```text
Recovery action detected
        ↓
Risk assessment
        ↓
Human approval
   ↙          ↘
APPROVE      REJECT
   ↓            ↓
Execute      Escalate
```

This prevents potentially unsafe automatic modifications to production-like data.

## Post-Recovery Validation

After recovery, the platform validates:

- Schema
- Missing values
- Duplicate records
- Invalid values

If validation passes:

```text
Incident → RESOLVED
```

If validation fails:

```text
Incident → ESCALATED
```

The validation result and recovery audit are stored with the incident.

## FastAPI

The platform exposes REST endpoints through FastAPI.

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "AI Data Reliability Platform"
}
```

### All Incidents

```text
GET /incidents
```

### Latest Incident

```text
GET /incidents/latest
```

### Workflow

```text
POST /workflow/run
```

The workflow endpoint is available for orchestration, while interactive human approval is currently handled through the CLI approval gateway.

### API Documentation

After starting the API:

```text
http://localhost:8000/docs
```

## Streamlit Dashboard

The project includes a Streamlit dashboard for viewing incident information and platform status.

Start it with:

```powershell
streamlit run dashboard/app.py
```

## Project Structure

```text
AI_Data_Reliability_Platform/
│
├── app/
│   ├── agents/
│   │   ├── investigation_agent.py
│   │   ├── incident_agent.py
│   │   ├── llm_investigation_agent.py
│   │   ├── recovery_agent.py
│   │   └── workflow_controller.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── incidents/
│   │   ├── incident_manager.py
│   │   ├── incident_store.py
│   │   └── incident_updater.py
│   │
│   ├── pipeline/
│   │   ├── ingestion.py
│   │   ├── transformation.py
│   │   └── validation.py
│   │
│   ├── quality/
│   │   ├── anomaly_detector.py
│   │   ├── quality_engine.py
│   │   ├── rules.py
│   │   └── schema_checker.py
│   │
│   ├── rag/
│   │   ├── knowledge_base.py
│   │   └── retriever.py
│   │
│   └── skills/
│       ├── anomaly_investigation.py
│       ├── approval_gateway.py
│       ├── data_validation_repair.py
│       ├── duplicate_cleanup.py
│       ├── missing_value_repair.py
│       ├── schema_repair.py
│       └── skill_router.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   ├── corrupted/
│   ├── processed/
│   ├── sample/
│   ├── incidents.json
│   └── approval_log.json
│
├── knowledge/
│   ├── documentation/
│   └── runbooks/
│
├── tests/
│   ├── test_anomaly_investigation.py
│   ├── test_quality_engine.py
│   └── test_recovery_skills.py
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### Clone the Repository

```powershell
git clone <your-repository-url>
cd AI_Data_Reliability_Platform
```

### Create Virtual Environment

```powershell
py -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Local Development

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Start Streamlit in another terminal:

```powershell
streamlit run dashboard/app.py
```

## Running Tests

Run:

```powershell
pytest -v
```

Current automated test coverage includes:

- Quality engine
- Schema repair
- Missing-value repair
- Duplicate cleanup
- Invalid-value repair
- Anomaly investigation

The current test suite contains **6 tests**, all passing.

## Docker

Build the image:

```powershell
docker build -t ai-data-reliability-platform .
```

Run the container:

```powershell
docker run -d `
  --name ai-data-reliability-container `
  -p 8000:8000 `
  ai-data-reliability-platform
```

Check the running container:

```powershell
docker ps
```

View logs:

```powershell
docker logs ai-data-reliability-container
```

Test the API:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

Swagger:

```text
http://localhost:8000/docs
```

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| API | FastAPI, Uvicorn |
| AI | LLM, structured investigation |
| RAG | Local runbooks and retrieval |
| Database Support | SQLAlchemy, PostgreSQL |
| Dashboard | Streamlit |
| Testing | Pytest |
| Containerization | Docker |
| Configuration | python-dotenv |
| Version Control | Git / GitHub |

## Safety Design

The platform follows a conservative recovery strategy:

- Recovery actions require human approval.
- Anomalous values are investigated rather than automatically changed.
- Invalid records can be quarantined.
- Recovery operations generate audit information.
- Post-recovery validation determines whether an incident is resolved.
- Failed validation results in escalation.
- Credentials are excluded from Docker and Git through `.env` and `.dockerignore`.

## Future Improvements

Planned enhancements include:

- Apache Airflow pipeline orchestration
- PostgreSQL incident storage
- Vector database for scalable RAG
- Cloud deployment on AWS
- S3-based data ingestion
- AWS Glue integration
- Lambda-based recovery actions
- Advanced anomaly detection
- Production authentication and authorization
- Richer Streamlit incident dashboards
- Asynchronous approval workflows
- Container orchestration with Kubernetes

## Project Status

**Current status: Functional local prototype**

Implemented:

- Data quality detection
- Incident creation
- AI investigation
- RAG runbook retrieval
- Recovery skill routing
- Human approval
- Recovery execution
- Anomaly investigation
- Post-recovery validation
- Incident status management
- FastAPI API
- Streamlit dashboard
- Automated tests
- Docker containerization

The project is designed as a portfolio-grade prototype demonstrating **data engineering, AI agents, RAG, reliability engineering, automation, API development, and responsible recovery workflows**.