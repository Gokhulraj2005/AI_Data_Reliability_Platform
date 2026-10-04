"""Load local runbooks and documentation as plain text."""

from pathlib import Path

from config.settings import KNOWLEDGE_DIR


def load_documents(root: Path = KNOWLEDGE_DIR) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    if not root.exists():
        return documents
    for path in sorted(root.rglob("*.md")):
        documents.append({"source": str(path.relative_to(root)), "text": path.read_text(encoding="utf-8")})
    return documents
