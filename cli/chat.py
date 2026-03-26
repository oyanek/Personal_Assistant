import sys
from core import AgentRouter, ToolRegistry, LLMClient, MemoryStore
from agents import AGENTS
from core.agent import Agent
from tools.default_tools import get_transactions, analyze_stock, summarize_text, add_transaction, list_transactions


def main():
    memory = MemoryStore()
    agents = {name: Agent(config) for name, config in AGENTS.items()}
    router = AgentRouter(agents)
    tool_registry = ToolRegistry()

    tool_registry.register_tool("get_transactions", "Return sample transaction data", get_transactions)
    tool_registry.register_tool("analyze_stock", "Analyze a stock ticker", analyze_stock)
    tool_registry.register_tool("summarize_text", "Summarize text input", summarize_text)
    tool_registry.register_tool("add_transaction", "Add transaction record", add_transaction)
    tool_registry.register_tool("list_transactions", "List sample transactions", list_transactions)

    llm = LLMClient()

    print("AI OS CLI chat (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in {"exit", "quit"}:
            print("Exiting...")
            sys.exit(0)

        agent = router.route(user_input)
        memory.add_message("user", user_input)

        # simple tool lookup (no complex execution path)
        prompt = f"{agent.system_prompt}\nUser: {user_input}"
        if llm.api_key:
            response = llm.call(agent.system_prompt, user_message=user_input)
        else:
            response = llm.echo(prompt)

        memory.add_message("assistant", response["text"])
        memory.add_agent_log(agent.name, "chat", response["text"])

        print(f"{agent.name}: {response['text']}\n")


if __name__ == "__main__":
    main()
