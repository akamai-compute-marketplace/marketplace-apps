from __future__ import annotations

import logging
import os
import threading
import time

import psutil
from locust import events

logger = logging.getLogger(__name__)


class _Stats:
    def __init__(self) -> None:
        self.total: int = 0
        self.failures: int = 0
        self.ttft_values: list[float] = []
        self.tps_values: list[float] = []
        self.input_tokens_total: int = 0
        self.output_tokens_total: int = 0
        self._lock = threading.Lock()

    def record(self, ttft_ms: float, tokens_per_sec: float,
               input_tokens: int, output_tokens: int, success: bool) -> None:
        with self._lock:
            self.total += 1
            if not success:
                self.failures += 1
            if ttft_ms > 0:
                self.ttft_values.append(ttft_ms)
            if tokens_per_sec > 0:
                self.tps_values.append(tokens_per_sec)
            self.input_tokens_total += input_tokens
            self.output_tokens_total += output_tokens


_stats = _Stats()
_test_start_perf: float = 0.0
_cpu_samples: list[float] = []
_cpu_stop = threading.Event()


def _mean(data: list[float]) -> float:
    return sum(data) / len(data) if data else 0.0


def _cpu_sampler() -> None:
    psutil.cpu_percent()  # discard first reading (always 0.0)
    while not _cpu_stop.wait(timeout=2.0):
        _cpu_samples.append(psutil.cpu_percent())


def record_llm_request(
    response_time_ms: float,
    ttft_ms: float,
    input_tokens: int,
    output_tokens: int,
    tokens_per_sec: float,
    success: bool,
    error: str = "",
) -> None:
    _stats.record(ttft_ms, tokens_per_sec, input_tokens, output_tokens, success)


def _on_test_start(**_kwargs) -> None:
    global _test_start_perf
    _test_start_perf = time.perf_counter()
    _cpu_stop.clear()
    threading.Thread(target=_cpu_sampler, daemon=True).start()


def _on_quitting(**_kwargs) -> None:
    _cpu_stop.set()

    s = _stats
    if s.total == 0:
        logger.info("[perf] No requests recorded.")
        return

    elapsed_sec = time.perf_counter() - _test_start_perf if _test_start_perf else 1.0
    sustained_tph = int(s.output_tokens_total / (elapsed_sec / 3600))
    mean_tps = _mean(s.tps_values)
    mean_ttft = _mean(s.ttft_values)
    mean_cpu = _mean(_cpu_samples)
    max_cpu = max(_cpu_samples) if _cpu_samples else 0.0
    error_rate = 100 * s.failures / s.total

    price_per_hour = float(os.environ.get("LINODE_PRICE_PER_HOUR", "0"))
    price_str = (
        f"${(price_per_hour / sustained_tph) * 1_000_000:.4f}"
        if sustained_tph > 0 and price_per_hour > 0
        else "n/a"
    )

    test_name     = os.environ.get("TEST_NAME",           "LLM Test")
    model_name    = os.environ.get("LLM_MODEL",         "unknown")
    instance_type = os.environ.get("LINODE_INSTANCE_TYPE", "unknown")

    W = 54
    sep = "═" * W

    def ln(label: str, value: str) -> str:
        pad = W - 2 - len(label) - len(value)
        return f"║  {label}{' ' * max(1, pad)}{value}║"

    lines = [
        f"╔{sep}╗",
        f"║{'  LLM Performance Test':<{W}}║",
        f"╠{'─' * W}╣",
        f"║  {test_name:<{W - 2}}║",
        f"║  Model:    {model_name:<{W - 12}}║",
        f"║  Instance: {instance_type:<{W - 12}}║",
        f"╠{'─' * W}╣",
        ln("Elapsed",                f"{elapsed_sec / 60:.1f} min"),
        ln("Requests",               f"{s.total - s.failures} ok / {s.failures} failed  ({error_rate:.1f}%)"),
        ln("Input tokens total",     f"{s.input_tokens_total:,}"),
        ln("Output tokens total",    f"{s.output_tokens_total:,}"),
        ln("Tokens / sec  (mean)",   f"{mean_tps:.1f}"),
        ln("Tokens / hour",          f"{sustained_tph:,}"),
        ln("Price per 1M tokens",    price_str),
        ln("TTFT (mean)",            f"{mean_ttft:.0f} ms"),
        ln("CPU (mean)",             f"{mean_cpu:.1f}%"),
        ln("CPU (max)",              f"{max_cpu:.1f}%"),
        f"╚{sep}╝",
    ]

    print("\n" + "\n".join(lines) + "\n")


_listeners_attached = False


def attach_listeners() -> None:
    global _listeners_attached
    if _listeners_attached:
        return
    _listeners_attached = True
    events.test_start.add_listener(_on_test_start)
    events.quitting.add_listener(_on_quitting)
