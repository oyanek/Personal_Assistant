from __future__ import annotations
from typing import Dict, List, Optional

class AgentRouter:
    """Simple keyword-based agent router."""

    def __init__(self, agents: Dict[str, object], routing_rules: Optional[Dict[str, str]] = None):
        self.agents = agents
        self.routing_rules = routing_rules or {
            "finance": "finance_agent",
            "stock": "finance_agent",
            "investment": "finance_agent",
            "research": "research_agent",
            "summarize": "research_agent",
            "productivity": "productivity_agent",
            "todo": "productivity_agent",
            "reminder": "productivity_agent",
        }

    def route(self, user_input: str) -> object:
        text = user_input.lower()
        for keyword, agent_name in self.routing_rules.items():
            if keyword in text and agent_name in self.agents:
                return self.agents[agent_name]
        # fallback to default
        return self.agents.get("productivity_agent") or next(iter(self.agents.values()))
