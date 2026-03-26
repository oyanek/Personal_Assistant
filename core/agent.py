from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class AgentConfig:
    name: str
    description: str
    system_prompt: str
    tools: List[str] = field(default_factory=list)
    tone: str = "neutral"

class Agent:
    """Base Agent class for modular AI OS agents."""

    def __init__(self, config: AgentConfig):
        self.config = config

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def description(self) -> str:
        return self.config.description

    @property
    def system_prompt(self) -> str:
        return self.config.system_prompt

    @property
    def tools(self) -> List[str]:
        return self.config.tools

    @property
    def tone(self) -> str:
        return self.config.tone

    def handle(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request and return structured output."""
        # Agents can be extended for custom workflows.
        return {
            "agent": self.name,
            "request": user_input,
            "context": context,
        }
