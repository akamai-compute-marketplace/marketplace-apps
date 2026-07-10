# LLM Performance Tests (Locust)

Performance tests for open-source LLMs running on Linode GPU instances.
Supports Ollama (port 11434) and vLLM (port 8000) backends.
Tests run **directly on the Linode** where the model is served — no SSH tunnel required.

---

## Project structure

```
tests/performance_tests/
├── run.sh                        # entry point — run this on the Linode
├── requirements.txt
├── config/
│   ├── prompts.json              # all test prompts (edit to add your own)
│   └── settings.py
├── locustfiles/
│   ├── single_user_test.py       # Test 1 — baseline, 1 user
│   ├── concurrency_test.py       # Test 2 — ramp 1 -> 50 users
│   └── soak_test.py              # Test 3 — sustained load, 45+ min
├── tasks/
│   └── ollama_tasks.py           # Ollama streaming inference + TTFT / tokens-per-sec
└── utils/
    └── metrics.py                # end-of-run summary
```

---

## Running tests on the Linode

### 1. Copy the tests folder to the Linode

```bash
# from your local machine
scp -r tests/performance_tests root@<LINODE_IP>:~/performance_tests
```

### 2. SSH into the Linode

```bash
ssh root@<LINODE_IP>
cd ~/performance_tests
```

### 3. Run

```bash
bash run.sh
```

`run.sh` will:
1. Create a `.venv` virtual environment (first run only)
2. Install all dependencies from `requirements.txt`
3. Prompt you for instance details and test options
4. Start Locust in headless mode

---

## Interactive prompts

When you run `run.sh`, it asks:

| Prompt | Example |
|--------|---------|
| Linode instance type | `RTX4000 Ada x1 Small` |
| Price per hour USD | `0.50` |
| Pick model | `1` |
| Pick test | `1` / `2` / `3` |
| Duration (test 1 & 3) | `10m` / `45m` |
| Concurrent users (test 3) | `10` |
| Spawn rate (test 3) | `2` |

---

## Test types

### Test 1 — Single User (baseline)
- **1 user**, no think time
- Default duration: **10 min**
- Measures theoretical tokens/hour ceiling

### Test 2 — Concurrency
- Ramps **1 → 5 → 10 → 25 → 50 users**, 5 min per step (~25 min total)
- Finds the saturation point and throughput sweet spot
- Shape is automatic — no extra flags needed

### Test 3 — Soak
- Configurable user count and duration (default 10 users, 45 min)
- Measures sustained throughput and latency drift over time

---

## Prompts

All prompts live in `config/prompts.json`:

```json
{
  "prompts": [
    "Explain the concept of gradient descent in simple terms.",
    "..."
  ]
}
```

Each test request picks a prompt at random. Edit this file to add, remove, or replace prompts.

---

## Metrics collected

| Metric | How it is measured |
|--------|--------------------|
| TTFT (ms) | Wall-clock time to first non-empty streaming chunk |
| Output tokens/sec | `eval_count / (eval_duration_ns / 1e9)` from Ollama |
| Input tokens | `prompt_eval_count` from Ollama final chunk |
| Output tokens | `eval_count` from Ollama final chunk |
| Tokens/hour | `tokens_per_sec × 3600` |
| Price / 1M tokens | `(price_per_hour / tokens_per_hour) × 1_000_000` |
| CPU utilization | `psutil` sampled every second on the test machine |

---

## End-of-run summary

After each run a summary box is printed to stdout, for example:

```
╔══════════════════════════════════════════╗
║   LLM Performance Test Summary           ║
╠══════════════════════════════════════════╣
║  Test          : Single User Test        ║
║  Model         : llama3.2:3b             ║
║  Instance type : RTX4000 Ada x1 Small    ║
╠══════════════════════════════════════════╣
║  Elapsed       : 600 s                   ║
║  Requests      : 48 (0 failed)           ║
║  Input tokens  : 24 816                  ║
║  Output tokens : 72 480                  ║
║  Tokens/sec    : 120.4                   ║
║  Tokens/hour   : 433 440                 ║
║  Price/1M tok  : $1.15                   ║
║  TTFT mean     : 312 ms                  ║
║  CPU mean      : 28 %                    ║
║  CPU max       : 61 %                    ║
╚══════════════════════════════════════════╝
```

---

## Adding models

Models are defined in the `MODELS` array inside `run.sh`. Each entry is a triple:
`display label`, `model tag`, `port`. Uncomment or add lines to enable more:

```bash
MODELS=(
  "llama3.2:3b      (Ollama - 11434)"  "llama3.2:3b"    11434
# "mistral:7b       (Ollama - 11434)"  "mistral:7b"     11434
# "deepseek-r1:7b   (vLLM   - 8000)"   "deepseek-r1:7b" 8000
# "qwen2.5:7b       (vLLM   - 8000)"   "qwen2.5:7b"     8000
# "gemma3:4b        (vLLM   - 8000)"   "gemma3:4b"      8000
)
```

| Backend | Default port | Models (examples) |
|---------|-------------|-------------------|
| Ollama  | `11434`     | llama3.2, mistral, gemma3 |
| vLLM    | `8000`      | deepseek-r1, qwen2.5, mistral |

The tasks layer (`tasks/ollama_tasks.py`) uses the Ollama `/api/generate` streaming
endpoint. If you add vLLM models, point them at vLLM's OpenAI-compatible `/v1/completions`
endpoint by adding a corresponding task file and locustfile.
