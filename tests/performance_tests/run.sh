#!/usr/bin/env bash
# =============================================================================
# LLM performance test runner
# Run this directly on the Linode where the model is serving.
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# -- Virtual environment setup ------------------------------------------------
VENV_DIR="${SCRIPT_DIR}/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at ${VENV_DIR} ..."
  python3 -m venv "$VENV_DIR"
fi
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

echo "Installing requirements ..."
pip install --quiet --upgrade pip
pip install --quiet -r "${SCRIPT_DIR}/requirements.txt"
echo "Requirements installed."
echo ""

# -- Linode config -------------------------------------------------------------
read -rp "Linode instance type [e.g. RTX4000 Ada x1 Small] : " LINODE_INSTANCE_TYPE
LINODE_INSTANCE_TYPE="${LINODE_INSTANCE_TYPE:-unknown}"

read -rp "Linode price per hour USD [e.g. 0.50]  : " LINODE_PRICE_PER_HOUR
LINODE_PRICE_PER_HOUR="${LINODE_PRICE_PER_HOUR:-0}"

# -- Model list - uncomment to enable  (label  tag  port) ---------------------
MODELS=(
  "llama3.2:3b      (Ollama - 11434)"  "llama3.2:3b"    11434
# "mistral:7b       (Ollama - 11434)"  "mistral:7b"     11434
# "deepseek-r1:7b   (vLLM   - 8000)"   "deepseek-r1:7b" 8000
# "qwen2.5:7b       (vLLM   - 8000)"   "qwen2.5:7b"     8000
# "gemma3:4b        (vLLM   - 8000)"   "gemma3:4b"      8000
)

echo ""
echo "  Models:"
IDX=1
for ((i=0; i<${#MODELS[@]}; i+=3)); do
  echo "    ${IDX})  ${MODELS[$i]}"
  IDX=$((IDX+1))
done
MODEL_COUNT=$((IDX-1))
echo ""
read -rp "Pick model [1-${MODEL_COUNT}]                        : " MODEL_CHOICE
MODEL_CHOICE="${MODEL_CHOICE:-1}"

IDX=1; LLM_MODEL=""; PORT=""
for ((i=0; i<${#MODELS[@]}; i+=3)); do
  if [ "$IDX" -eq "$MODEL_CHOICE" ]; then
    LLM_MODEL="${MODELS[$((i+1))]}"
    PORT="${MODELS[$((i+2))]}"
    break
  fi
  IDX=$((IDX+1))
done
[ -z "$LLM_MODEL" ] && echo "ERROR: Invalid choice." && exit 1
echo "  -> $LLM_MODEL on port $PORT"

# -- Test type ----------------------------------------------------------------
echo ""
echo "  Tests:"
echo "    1)  Single user  - 1 user, baseline tokens/hour"
echo "    2)  Concurrency  - 1->5->10->25->50 users, 5 min each (~25 min)"
echo "    3)  Soak         - sustained load, 45+ min"
echo ""
read -rp "Pick test [1/2/3]                      : " TEST_CHOICE

case "$TEST_CHOICE" in
  1)
    LOCUSTFILE="locustfiles/single_user_test.py"
    TEST_NAME="Single User Test"
    read -rp "Duration              [10m]            : " DURATION
    DURATION="${DURATION:-10m}"; USERS=1; SPAWN_RATE=1
    ;;
  2)
    LOCUSTFILE="locustfiles/concurrency_test.py"
    TEST_NAME="Concurrency Test"
    ;;
  3)
    LOCUSTFILE="locustfiles/soak_test.py"
    TEST_NAME="Soak Test"
    read -rp "Concurrent users      [10]             : " USERS
    USERS="${USERS:-10}"
    read -rp "Spawn rate users/s    [2]              : " SPAWN_RATE
    SPAWN_RATE="${SPAWN_RATE:-2}"
    read -rp "Duration              [45m]            : " DURATION
    DURATION="${DURATION:-45m}"
    ;;
  *)
    echo "ERROR: Invalid choice."; exit 1 ;;
esac

echo ""

# -- Run Locust ----------------------------------------------------------------
export PYTHONPATH="${SCRIPT_DIR}"
export LLM_MODEL
export LINODE_PRICE_PER_HOUR
export LINODE_INSTANCE_TYPE
export TEST_NAME

if [ "$TEST_CHOICE" = "2" ]; then
  locust -f "${SCRIPT_DIR}/${LOCUSTFILE}" --headless --host "http://localhost:${PORT}"
else
  locust -f "${SCRIPT_DIR}/${LOCUSTFILE}" --headless --host "http://localhost:${PORT}" -u "$USERS" -r "$SPAWN_RATE" -t "$DURATION"
fi

echo ""
echo "Done"
