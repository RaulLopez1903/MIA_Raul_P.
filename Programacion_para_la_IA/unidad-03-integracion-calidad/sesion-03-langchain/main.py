import argparse
from agent_app import build_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the optional document agent")
    parser.add_argument("--provider", required=True, choices=["openai", "anthropic", "google_genai"])
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    agent = build_agent(args.provider, args.model)
    result = agent.invoke({"messages": [{"role": "user", "content": "Which retrieval documents exist and how many pages do they total?"}]})
    for message in result["messages"]:
        print(message.type, message.content)
        if getattr(message, "tool_calls", None):
            print(message.tool_calls)


if __name__ == "__main__":
    main()
