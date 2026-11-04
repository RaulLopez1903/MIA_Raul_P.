from langchain.tools import tool
from sample_data import DOCUMENTS


@tool
def find_documents(topic: str) -> list[dict[str, str | int]]:
    """Find catalog documents by topic: python, retrieval, integration, or data."""
    normalized_topic = topic.strip().lower()
    return [dict(document) for document in DOCUMENTS if document["topic"] == normalized_topic]


@tool
def count_pages(topic: str) -> int:
    """Return the total pages of catalog documents for a topic."""
    normalized_topic = topic.strip().lower()
    return sum(document["pages"] for document in DOCUMENTS if document["topic"] == normalized_topic)
