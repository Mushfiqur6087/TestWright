import asyncio
import json
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime

import litellm  # type: ignore


# Strip provider-incompatible params silently (e.g. temperature on o-series,
# unsupported response_format dialects). LiteLLM handles per-model normalisation.
litellm.drop_params = True


# Module-level concurrency throttle for async LLM calls. Sized by
# ``set_max_concurrency`` (defaults to 10) so a 30-chunk Send fan-out doesn't
# blow past provider rate limits. Built lazily so we don't bind to an event
# loop at import time.
_LLM_SEMAPHORE: Optional[asyncio.Semaphore] = None
_LLM_SEMAPHORE_LIMIT: int = 10


def set_max_concurrency(limit: int) -> None:
    """Set the maximum number of concurrent in-flight async LLM calls."""
    global _LLM_SEMAPHORE_LIMIT, _LLM_SEMAPHORE
    if limit < 1:
        raise ValueError("max concurrency must be >= 1")
    _LLM_SEMAPHORE_LIMIT = limit
    _LLM_SEMAPHORE = None  # re-create on next acquire


def _get_llm_semaphore() -> asyncio.Semaphore:
    global _LLM_SEMAPHORE
    if _LLM_SEMAPHORE is None:
        _LLM_SEMAPHORE = asyncio.Semaphore(_LLM_SEMAPHORE_LIMIT)
    return _LLM_SEMAPHORE


class BaseAgent(ABC):
    """Base class for all agents. Uses LiteLLM for unified provider routing.

    Model strings follow LiteLLM convention:
        - openai/gpt-4o
        - openrouter/anthropic/claude-3.5-sonnet
        - github/gpt-4o
        - anthropic/claude-3-5-sonnet-20241022
    """

    # Class-level tracking to avoid duplicate logging
    _initialized_debug_files: set = set()
    _logged_system_prompts = set()

    def __init__(
        self,
        api_key: str,
        model: str,
        debug: bool = False,
        debug_file: str = "debug_log.txt",
    ):
        self.api_key = api_key
        self.model = model
        self.debug = debug
        self.debug_file = debug_file
        self._system_prompt_logged = False

    @classmethod
    def reset_debug_state(cls):
        """Reset debug state for a new session. Call this before initializing agents."""
        cls._initialized_debug_files = set()
        cls._logged_system_prompts = set()

    @classmethod
    def init_debug_session(cls, debug_file: str, model: str):
        """Write a stage header to debug_file the first time it is referenced per run."""
        if debug_file in cls._initialized_debug_files:
            return
        cls._initialized_debug_files.add(debug_file)
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

    @staticmethod
    def _ts() -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _extra_headers(self) -> Optional[Dict[str, str]]:
        """OpenRouter is polite about attribution headers; pass them through."""
        if self.model.startswith("openrouter/"):
            return {
                "HTTP-Referer": "https://github.com/AutoSpecTest",
                "X-Title": "AutoSpecTest",
            }
        return None

    def _build_completion_kwargs(
        self,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict],
        reasoning_effort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Assemble the kwargs dict shared by sync and async LiteLLM calls."""
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "api_key": self.api_key,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timeout": 300,
            "num_retries": 2,
        }
        if response_format:
            kwargs["response_format"] = response_format
        if reasoning_effort:
            kwargs["reasoning_effort"] = reasoning_effort
        extra_headers = self._extra_headers()
        if extra_headers:
            kwargs["extra_headers"] = extra_headers
        return kwargs

    def _log_response(self, response: Any, elapsed: float) -> str:
        """Extract content + log token usage. Shared by sync and async paths."""
        content = response.choices[0].message.content
        usage = getattr(response, "usage", None) or {}
        if hasattr(usage, "get"):
            prompt_tokens = usage.get("prompt_tokens", "?")
            completion_tokens = usage.get("completion_tokens", "?")
            total_tokens = usage.get("total_tokens", "?")
        else:
            prompt_tokens = getattr(usage, "prompt_tokens", "?")
            completion_tokens = getattr(usage, "completion_tokens", "?")
            total_tokens = getattr(usage, "total_tokens", "?")
        print(
            f"    [{self._ts()}] << {self.name} | "
            f"response in {elapsed:.1f}s | "
            f"tokens: {prompt_tokens}+{completion_tokens}={total_tokens}"
        )
        if self.debug:
            self._log_debug("LLM RESPONSE", content)
        return content

    def _log_request(self, user_prompt: str) -> None:
        if self.debug:
            if not self._system_prompt_logged:
                self._log_debug("SYSTEM PROMPT", self.system_prompt)
                self._system_prompt_logged = True
            self._log_debug("USER PROMPT", user_prompt)
        print(f"    [{self._ts()}] >> {self.name} | sending request (~{len(user_prompt)} chars)")

    def call_llm(
        self,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None,
        reasoning_effort: Optional[str] = None,
    ) -> str:
        """Call the LLM synchronously via LiteLLM and return response content."""
        self._log_request(user_prompt)
        t0 = time.time()
        kwargs = self._build_completion_kwargs(user_prompt, temperature, max_tokens, response_format, reasoning_effort)
        try:
            response = litellm.completion(**kwargs)
        except Exception as err:
            elapsed = time.time() - t0
            msg = f"LiteLLM error ({type(err).__name__}): {err}"
            print(f"    [{self._ts()}] !! {self.name} | {msg} after {elapsed:.1f}s")
            if self.debug:
                self._log_debug("ERROR", msg)
            raise
        return self._log_response(response, time.time() - t0)

    async def acall_llm(
        self,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None,
        reasoning_effort: Optional[str] = None,
    ) -> str:
        """Call the LLM asynchronously via LiteLLM, throttled by the module semaphore."""
        self._log_request(user_prompt)
        kwargs = self._build_completion_kwargs(user_prompt, temperature, max_tokens, response_format, reasoning_effort)
        async with _get_llm_semaphore():
            t0 = time.time()
            try:
                response = await litellm.acompletion(**kwargs)
            except Exception as err:
                elapsed = time.time() - t0
                msg = f"LiteLLM error ({type(err).__name__}): {err}"
                print(f"    [{self._ts()}] !! {self.name} | {msg} after {elapsed:.1f}s")
                if self.debug:
                    self._log_debug("ERROR", msg)
                raise
            return self._log_response(response, time.time() - t0)

    def call_llm_json(
        self,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1500,
        max_retries: int = 2,
        reasoning_effort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Call LLM and parse response as JSON with retry on parse errors"""
        json_prompt = f"{user_prompt}\n\nIMPORTANT: Return your response as valid JSON only. No markdown, no code blocks, just pure JSON."
        use_json_response_format = True

        last_error = None
        for attempt in range(max_retries + 1):
            try:
                response = self.call_llm(
                    user_prompt=json_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"} if use_json_response_format else None,
                    reasoning_effort=reasoning_effort,
                )

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
                    print(f"    [{self._ts()}] ~~ {self.name} | JSON parse failed (attempt {attempt+1}/{max_retries+1}): {e} | retrying...")
                    json_prompt = f"{user_prompt}\n\nIMPORTANT: Return ONLY valid JSON. Ensure all strings are properly quoted and escaped. No markdown formatting."
                else:
                    error_msg = f"Failed to parse LLM response as JSON after {max_retries + 1} attempts: {last_error}\nResponse: {response}"
                    if self.debug:
                        self._log_debug("JSON PARSE ERROR - FINAL", error_msg)
                    raise Exception(error_msg)

            except Exception as e:
                # Some providers/models may reject response_format; retry without it.
                if use_json_response_format and "response_format" in str(e).lower():
                    use_json_response_format = False
                    if attempt < max_retries:
                        print(f"    [{self._ts()}] ~~ {self.name} | response_format unsupported, retrying without it...")
                        continue
                raise

        # Should never reach here
        raise Exception(f"Failed to parse JSON after {max_retries + 1} attempts")

    async def acall_llm_json(
        self,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1500,
        max_retries: int = 2,
        reasoning_effort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Async counterpart of ``call_llm_json`` for use inside Send-API workers."""
        json_prompt = f"{user_prompt}\n\nIMPORTANT: Return your response as valid JSON only. No markdown, no code blocks, just pure JSON."
        use_json_response_format = True

        last_error = None
        for attempt in range(max_retries + 1):
            try:
                response = await self.acall_llm(
                    user_prompt=json_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"} if use_json_response_format else None,
                    reasoning_effort=reasoning_effort,
                )
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
                    print(f"    [{self._ts()}] ~~ {self.name} | JSON parse failed (attempt {attempt+1}/{max_retries+1}): {e} | retrying...")
                    json_prompt = f"{user_prompt}\n\nIMPORTANT: Return ONLY valid JSON. Ensure all strings are properly quoted and escaped. No markdown formatting."
                else:
                    error_msg = f"Failed to parse LLM response as JSON after {max_retries + 1} attempts: {last_error}\nResponse: {response}"
                    if self.debug:
                        self._log_debug("JSON PARSE ERROR - FINAL", error_msg)
                    raise Exception(error_msg)

            except Exception as e:
                if use_json_response_format and "response_format" in str(e).lower():
                    use_json_response_format = False
                    if attempt < max_retries:
                        print(f"    [{self._ts()}] ~~ {self.name} | response_format unsupported, retrying without it...")
                        continue
                raise

        raise Exception(f"Failed to parse JSON after {max_retries + 1} attempts")

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Execute the agent's main task"""
        pass
