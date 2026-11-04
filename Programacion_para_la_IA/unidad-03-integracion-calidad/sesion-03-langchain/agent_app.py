import os
from getpass import getpass
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.chat_models import init_chat_model
from catalog_tools import count_pages, find_documents
from agent_hooks import show_message_count
from input_guardrails import check_user_input


PROVIDERS = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google_genai": "GOOGLE_API_KEY",
}


def build_agent(provider: str, model_name: str):
    load_dotenv(Path(__file__).with_name(".env"))
    if provider not in PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}")
    key_name = PROVIDERS[provider]
    if not os.environ.get(key_name):
        os.environ[key_name] = getpass(f"{key_name}: ")
    model = init_chat_model(model_name, model_provider=provider)
    return create_agent(
        model=model,
        tools=[find_documents, count_pages],
        system_prompt=(
            "Answer using the document catalog tools. "
            "Do not invent documents. State when no matches exist."
        ),
        middleware=[
            check_user_input,
            show_message_count,
            ModelCallLimitMiddleware(run_limit=3, exit_behavior="end"),
        ],
    )
