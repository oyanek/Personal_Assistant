from __future__ import annotations
from typing import Callable, Dict, Any

class Tool:
    def __init__(self, name: str, description: str, func: Callable[..., Any]):
        self.name = name
        self.description = description
        self.func = func

    def execute(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)


class ToolRegistry:
    """Registry of callable tools for the AI OS."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register_tool(self, name: str, description: str, func: Callable[..., Any]):
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered")
        self._tools[name] = Tool(name, description, func)

    def get_tool(self, name: str) -> Tool:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Tool '{name}' is not registered")
        return tool

    def list_tools(self) -> Dict[str, str]:
        return {name: tool.description for name, tool in self._tools.items()}

    def execute_tool(self, name: str, *args, **kwargs) -> Any:
        tool = self.get_tool(name)
        return tool.execute(*args, **kwargs)
