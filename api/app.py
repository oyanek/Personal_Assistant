from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core import AgentRouter, ToolRegistry, LLMClient, MemoryStore
from agents import AGENTS
from core.agent import Agent
from tools.default_tools import get_transactions, analyze_stock, summarize_text, add_transaction, list_transactions

app = FastAPI(title="AI OS", version="0.1.0")

memory = MemoryStore()

# agent instances
AGENT_INSTANCES = {name: Agent(config) for name, config in AGENTS.items()}
router = AgentRouter(AGENT_INSTANCES)

# tool registry
tool_registry = ToolRegistry()
tool_registry.register_tool("get_transactions", "Return sample transaction data", get_transactions)
tool_registry.register_tool("analyze_stock", "Analyze a stock ticker", analyze_stock)
tool_registry.register_tool("summarize_text", "Summarize text input", summarize_text)
tool_registry.register_tool("add_transaction", "Add transaction record", add_transaction)
tool_registry.register_tool("list_transactions", "List sample transactions", list_transactions)

llm = LLMClient()  # uses env OPENAI_API_KEY when available

class ChatRequest(BaseModel):
    user_input: str

class ToolCallRequest(BaseModel):
    tool_name: str
    args: list = []
    kwargs: dict = {}

@app.get("/agents")
def get_agents():
    return [{"name": agent.name, "description": agent.description, "tools": agent.tools} for agent in AGENT_INSTANCES.values()]

@app.post("/chat")
def chat(request: ChatRequest):
    agent = router.route(request.user_input)

    memory.add_message("user", request.user_input)
    memory.add_agent_log(agent.name, "route", f"routed to {agent.name}")

    # Simple agent handling path, calls all registered tool helpers available to this agent
    tool_results = {}
    for tool_name in agent.tools:
        if tool_name in tool_registry.list_tools():
            try:
                tool_results[tool_name] = tool_registry.execute_tool(tool_name, "2026-01" if tool_name == "get_transactions" else "AAPL" if tool_name == "analyze_stock" else "Hello world" if tool_name == "summarize_text" else None)
            except Exception as exc:
                tool_results[tool_name] = str(exc)

    prompt = f"{agent.system_prompt}\nUser: {request.user_input}\nTools: {tool_results}"

    try:
        response = llm.echo(prompt) if not llm.api_key else llm.call(agent.system_prompt, user_message=request.user_input)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    memory.add_message("assistant", response["text"])
    memory.add_agent_log(agent.name, "respond", response["text"])

    return {
        "agent": agent.name,
        "response": response["text"],
        "tools": tool_results,
    }

@app.post("/tools/test")
def test_tool(request: ToolCallRequest):
    if request.tool_name not in tool_registry.list_tools():
        raise HTTPException(404, f"Tool {request.tool_name} not found")

    result = tool_registry.execute_tool(request.tool_name, *request.args, **request.kwargs)
    return {"tool": request.tool_name, "result": result}

@app.get("/memory/messages")
def get_messages(limit: int = 50):
    return memory.get_messages(limit)
