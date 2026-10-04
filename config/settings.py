"""Environment-backed paths and service settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

DATA_DIR = ROOT_DIR / "data"
KNOWLEDGE_DIR = ROOT_DIR / "knowledge"
INCIDENTS_FILE = Path(os.getenv("INCIDENTS_FILE", DATA_DIR / "processed" / "incidents.jsonl"))
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
