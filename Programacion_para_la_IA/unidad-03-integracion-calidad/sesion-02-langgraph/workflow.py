from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from sample_data import DOCUMENTS, Document


class WorkflowState(TypedDict, total=False):
    topic: str
    original_topic: str
    documents: list[Document]
    count: int
    total_pages: int
    message: str


def normalize_topic(state: WorkflowState) -> WorkflowState:
    return {"original_topic": state["topic"], "topic": state["topic"].strip().lower()}


def select_documents(state: WorkflowState) -> WorkflowState:
    selected = []
    for document in DOCUMENTS:
        if document["topic"] == state["topic"]:
            selected.append(document)
    return {"documents": selected}


def route_documents(state: WorkflowState) -> Literal["found", "empty"]:
    if state["documents"]:
        return "found"
    return "empty"


def summarize_documents(state: WorkflowState) -> WorkflowState:
    count = len(state["documents"])
    total_pages = sum(document["pages"] for document in state["documents"])
    return {
        "count": count,
        "total_pages": total_pages,
        "message": f"Found {count} documents with {total_pages} pages.",
    }


def report_empty(state: WorkflowState) -> WorkflowState:
    return {
        "count": 0,
        "total_pages": 0,
        "message": f"No documents found for topic: {state['topic']}",
    }


def build_workflow():
    builder = StateGraph(WorkflowState)
    builder.add_node("normalize", normalize_topic)
    builder.add_node("select", select_documents)
    builder.add_node("summarize", summarize_documents)
    builder.add_node("empty", report_empty)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", "select")
    builder.add_conditional_edges(
        "select", route_documents,
        {"found": "summarize", "empty": "empty"},
    )
    builder.add_edge("summarize", END)
    builder.add_edge("empty", END)
    return builder.compile()
