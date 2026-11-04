from typing import TypedDict


class Document(TypedDict):
    title: str
    topic: str
    pages: int


DOCUMENTS: list[Document] = [
    {"title": "Python fundamentals", "topic": "python", "pages": 28},
    {"title": "Text embeddings", "topic": "retrieval", "pages": 12},
    {"title": "MCP tools", "topic": "integration", "pages": 8},
    {"title": "Graph search", "topic": "retrieval", "pages": 16},
    {"title": "NumPy arrays", "topic": "data", "pages": 20},
    {"title": "Pandas tables", "topic": "data", "pages": 24},
]
