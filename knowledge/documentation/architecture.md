# Architecture Notes

The starter flow is ingestion, normalization, quality evaluation, and incident review. Quality rules live in `app/quality/rules.py`; the API exposes evaluation and incident listing. Repair helpers are deterministic and intentionally require review before production use. Local runbooks are searched with simple keyword matching, not an external LLM or vector database.
