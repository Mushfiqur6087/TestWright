import json
import httpx # type: ignore
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all agents with OpenAI/OpenRouter integration and debug logging"""

    # Class-level tracking to avoid duplicate logging
    _debug_initialized = False
    _logged_system_prompts = set()

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        provider: str = "openai",
        debug: bool = False,
        debug_file: str = "debug_log.txt",
    ):
        self.api_key = api_key
        self.model = model
        self.provider = provider.lower()
        self.debug = debug
        self.debug_file = debug_file

        # Set base URL based on provider
        if self.provider == "openai":
            self.base_url = "https://api.openai.com/v1"
        elif self.provider == "github":
            self.base_url = "https://models.inference.ai.azure.com"
        else:  # openrouter
            self.base_url = "https://openrouter.ai/api/v1"

        self.client = httpx.Client(timeout=120.0)
        self._system_prompt_logged = False  # Track if this agent's system prompt was logged

    @classmethod
    def reset_debug_state(cls):
        """Reset debug state for a new session. Call this before initializing agents."""
        cls._debug_initialized = False
        cls._logged_system_prompts = set()

    @classmethod
    def init_debug_session(cls, debug_file: str, model: str):
        """Initialize debug session header. Should be called once at start."""
        if cls._debug_initialized:
            return
        cls._debug_initialized = True
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(f"{'='*80}\n")
            f.write(f"DEBUG SESSION STARTED: {datetime.now().isoformat()}\n")
            f.write(f"Model: {model}\n")
            f.write(f"{'='*80}\n\n")

    def _log_debug(self, label: str, content: str):
        """Log debug information to file"""
        if not self.debug:
            return

        with open(self.debug_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'-'*60}\n")
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {self.name} - {label}\n")
            f.write(f"{'-'*60}\n")
            f.write(str(content))
            f.write("\n")

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the agent name"""
        pass

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass

    def call_llm(
        self,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """Call OpenAI or OpenRouter API with the given prompt"""

        # Log input if debug enabled
        if self.debug:
            # Only log system prompt once per agent to avoid redundancy
            if not self._system_prompt_logged:
                self._log_debug("SYSTEM PROMPT", self.system_prompt)
                self._system_prompt_logged = True
            self._log_debug("USER PROMPT", user_prompt)

        # Build headers based on provider
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Add OpenRouter-specific headers
        if self.provider == "openrouter":
            headers["HTTP-Referer"] = "https://testwright.dev"
            headers["X-Title"] = "TestWright"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        if response_format:
            payload["response_format"] = response_format

        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            provider_name = self.provider.upper()
            error_msg = f"{provider_name} API error: {response.status_code} - {response.text}"
            if self.debug:
                self._log_debug("ERROR", error_msg)
            raise Exception(error_msg)

        result = response.json()
        response_content = result["choices"][0]["message"]["content"]

        # Log output if debug enabled
        if self.debug:
            self._log_debug("LLM RESPONSE", response_content)

        return response_content

    def call_llm_json(
        self,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1500,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """Call LLM and parse response as JSON with retry on parse errors"""
        # Add instruction to return JSON
        json_prompt = f"{user_prompt}\n\nIMPORTANT: Return your response as valid JSON only. No markdown, no code blocks, just pure JSON."

        last_error = None
        for attempt in range(max_retries + 1):
            try:
                response = self.call_llm(
                    user_prompt=json_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                # Clean up response - remove markdown code blocks if present
                response = response.strip()
                if response.startswith("```json"):
                    response = response[7:]
                elif response.startswith("```"):
                    response = response[3:]
                if response.endswith("```"):
                    response = response[:-3]
                response = response.strip()

                parsed = json.loads(response)
                if self.debug:
                    self._log_debug("PARSED JSON", json.dumps(parsed, indent=2))
                return parsed

            except json.JSONDecodeError as e:
                last_error = e
                error_msg = f"Failed to parse LLM response as JSON (attempt {attempt + 1}/{max_retries + 1}): {e}"
                if self.debug:
                    self._log_debug("JSON PARSE ERROR", f"{error_msg}\nResponse: {response[:500]}...")

                if attempt < max_retries:
                    print(f"  Warning: {error_msg}. Retrying...")
                    json_prompt = f"{user_prompt}\n\nIMPORTANT: Return ONLY valid JSON. Ensure all strings are properly quoted and escaped. No markdown formatting."
                else:
                    # Last attempt failed
                    error_msg = f"Failed to parse LLM response as JSON after {max_retries + 1} attempts: {last_error}\nResponse: {response}"
                    if self.debug:
                        self._log_debug("JSON PARSE ERROR - FINAL", error_msg)
                    raise Exception(error_msg)

        # Should never reach here
        raise Exception(f"Failed to parse JSON after {max_retries + 1} attempts")

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute the agent's main task"""
        pass

    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()
