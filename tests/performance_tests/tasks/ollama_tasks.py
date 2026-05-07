import json
import os
import random
import time
import logging
from pathlib import Path

from locust import TaskSet, task

from utils.metrics import record_llm_request

logger = logging.getLogger(__name__)

_PROMPTS_FILE = Path(__file__).parents[1] / "config" / "prompts.json"
with open(_PROMPTS_FILE, encoding="utf-8") as _f:
    _PROMPTS = json.load(_f)["prompts"]


class LLMTaskSet(TaskSet):
    model_name: str = os.environ.get("LLM_MODEL", "llama3.2:3b")
    prompts: list = _PROMPTS

    def _run_inference(self, prompt: str) -> None:
        payload = {"model": self.model_name, "prompt": prompt, "stream": True}

        t_start = time.perf_counter()
        ttft_ms: float = 0.0
        input_tokens: int = 0
        output_tokens: int = 0
        tokens_per_sec: float = 0.0
        success = False
        error = ""

        try:
            with self.client.post(
                "/api/generate",
                json=payload,
                name="/api/generate",
                catch_response=True,
                stream=True,
            ) as response:
                if response.status_code != 200:
                    error = f"HTTP {response.status_code}"
                    response.failure(error)
                else:
                    for raw_line in response.iter_lines():
                        if not raw_line:
                            continue
                        try:
                            chunk = json.loads(raw_line)
                        except json.JSONDecodeError:
                            continue

                        if ttft_ms == 0.0 and chunk.get("response"):
                            ttft_ms = (time.perf_counter() - t_start) * 1000

                        if chunk.get("done"):
                            input_tokens = chunk.get("prompt_eval_count", 0)
                            output_tokens = chunk.get("eval_count", 0)
                            eval_dur_ns = chunk.get("eval_duration", 0)
                            if eval_dur_ns > 0:
                                tokens_per_sec = output_tokens / (eval_dur_ns / 1e9)
                            response.success()
                            success = True
                            break

        except Exception as exc:
            error = str(exc)
            logger.warning("[ollama] request failed: %s", exc)

        record_llm_request(
            response_time_ms=(time.perf_counter() - t_start) * 1000,
            ttft_ms=ttft_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            tokens_per_sec=tokens_per_sec,
            success=success,
            error=error,
        )

    @task
    def generate(self) -> None:
        if self.prompts:
            self._run_inference(random.choice(self.prompts))
