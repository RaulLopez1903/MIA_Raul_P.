from typing import Any
from langchain.agents.middleware import AgentState, before_model
from langgraph.runtime import Runtime


@before_model
def show_message_count(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"Messages before model call: {len(state['messages'])}")
    return None
