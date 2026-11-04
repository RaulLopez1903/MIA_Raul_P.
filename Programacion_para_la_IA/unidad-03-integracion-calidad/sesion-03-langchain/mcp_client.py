import argparse
import asyncio
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from input_guardrails import check_user_input


async def demonstrate_mcp(model=None, url: str = "http://127.0.0.1:8000/mcp") -> None:
    from langchain.mcp import MCPAdapter

    async with MCPAdapter(url) as adapter:
        tools = await adapter.list_tools()
        print("Available tools:", [tool.name for tool in tools])
        search = next(tool for tool in tools if tool.name == "search_products")
        result = await search.ainvoke({
            "query": "A portable waterproof Bluetooth speaker",
            "top_k": 3,
        })
        print(result)
        if model is not None:
            agent = create_agent(
                model=model,
                tools=tools,
                system_prompt="Use the Amazon catalog tools. Do not invent products or ratings.",
                middleware=[check_user_input, ModelCallLimitMiddleware(run_limit=3, exit_behavior="end")],
            )
            result = await agent.ainvoke({"messages": [{
                "role": "user", "content": "Find three portable waterproof Bluetooth speakers in the catalog."
            }]})
            for message in result["messages"]:
                print(message.type, message.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect and call the project MCP tools without a model")
    parser.add_argument("--url", default="http://127.0.0.1:8000/mcp")
    args = parser.parse_args()
    asyncio.run(demonstrate_mcp(url=args.url))
