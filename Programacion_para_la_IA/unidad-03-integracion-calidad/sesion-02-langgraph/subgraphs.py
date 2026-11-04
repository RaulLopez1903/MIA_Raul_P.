from langgraph.graph import END, START, StateGraph
from workflow import (
    WorkflowState, normalize_topic, report_empty, route_documents,
    select_documents, summarize_documents,
)


def validate_request(state: WorkflowState) -> WorkflowState:
    topic = state.get("topic")
    if not isinstance(topic, str):
        raise TypeError("topic must be a string")
    if not topic.strip():
        raise ValueError("topic must not be blank")
    return {}


def build_analysis_subgraph():
    builder = StateGraph(WorkflowState)
    builder.add_node("select", select_documents)
    builder.add_node("summarize", summarize_documents)
    builder.add_node("empty", report_empty)
    builder.add_edge(START, "select")
    builder.add_conditional_edges(
        "select", route_documents,
        {"found": "summarize", "empty": "empty"},
    )
    builder.add_edge("summarize", END)
    builder.add_edge("empty", END)
    return builder.compile()


def build_modular_workflow():
    analysis = build_analysis_subgraph()
    builder = StateGraph(WorkflowState)
    builder.add_node("validate", validate_request)
    builder.add_node("normalize", normalize_topic)
    builder.add_node("analysis", analysis)
    builder.add_edge(START, "validate")
    builder.add_edge("validate", "normalize")
    builder.add_edge("normalize", "analysis")
    builder.add_edge("analysis", END)
    return builder.compile()
