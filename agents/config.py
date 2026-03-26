from core.agent import AgentConfig

AGENTS = {
    "finance_agent": AgentConfig(
        name="finance_agent",
        description="Handles finance and investment insights.",
        system_prompt="You are a finance assistant. Provide concise analysis around budgets, investments and transactions.",
        tools=["get_transactions", "analyze_stock"],
        tone="analytic",
    ),
    "research_agent": AgentConfig(
        name="research_agent",
        description="Assists with research and summarization tasks.",
        system_prompt="You are a research assistant. Provide structured summaries and information gathering.",
        tools=["summarize_text"],
        tone="informative",
    ),
    "productivity_agent": AgentConfig(
        name="productivity_agent",
        description="Helps with productivity, tasks, and reminders.",
        system_prompt="You are a productivity assistant. Help organize tasks and suggest workflows.",
        tools=["add_transaction", "list_transactions"],
        tone="supportive",
    ),
}
