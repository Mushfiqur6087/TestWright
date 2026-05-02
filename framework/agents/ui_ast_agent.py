"""UI-AST Agent: converts a module's functional description into a UI Abstract Syntax Tree."""

from importlib import resources
from typing import Any, Dict

from autospectest.framework.agents.base import BaseAgent

_PROMPT = resources.files("autospectest.prompts").joinpath("ui_ast.md").read_text(encoding="utf-8")


class UIASTAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "UI-AST Agent"

    @property
    def system_prompt(self) -> str:
        return _PROMPT

    def run(self, module: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Module: {module['title']}\n\n{module['description']}"
        return self.call_llm_json(prompt, temperature=0.2, max_tokens=8192)

    async def arun(self, module: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Module: {module['title']}\n\n{module['description']}"
        return await self.acall_llm_json(prompt, temperature=0.2, max_tokens=8192)
