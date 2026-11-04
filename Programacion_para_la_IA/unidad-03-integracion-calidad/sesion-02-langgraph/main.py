from workflow import build_workflow


def main() -> None:
    workflow = build_workflow()
    for topic in (" Retrieval ", "unknown"):
        result = workflow.invoke({"topic": topic})
        print(result["message"])


if __name__ == "__main__":
    main()
