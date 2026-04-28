#!/bin/sh

set -eu

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <job-id> <prompt-file> <thread-key> [label]" >&2
  exit 1
fi

JOB_ID="$1"
PROMPT_FILE="$2"
THREAD_KEY="$3"
LABEL="${4:-}"

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
ENV_FILE="${TELEGRAM_RUNNER_ENV:-$SCRIPT_DIR/telegram-runner.env}"
CONFIG_FILE="${TELEGRAM_RUNNER_CONFIG:-$SCRIPT_DIR/telegram-config.json}"
LOG_DIR="${TELEGRAM_RUNNER_LOG_DIR:-$SCRIPT_DIR/logs}"

mkdir -p "$LOG_DIR"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S %Z"
}

LOG_FILE="$LOG_DIR/${JOB_ID}.log"

if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi

{
  echo "[$(timestamp)] START job_id=$JOB_ID thread=$THREAD_KEY prompt_file=$PROMPT_FILE"
} >> "$LOG_FILE"

if [ -n "$LABEL" ]; then
  if python3 "$SCRIPT_DIR/telegram_runner.py" \
    --job-id "$JOB_ID" \
    --prompt-file "$PROMPT_FILE" \
    --thread-key "$THREAD_KEY" \
    --config "$CONFIG_FILE" \
    --label "$LABEL" \
    ${TELEGRAM_RUNNER_DRY_RUN:+--dry-run} >> "$LOG_FILE" 2>&1; then
    STATUS=0
  else
    STATUS=$?
  fi
else
  if python3 "$SCRIPT_DIR/telegram_runner.py" \
    --job-id "$JOB_ID" \
    --prompt-file "$PROMPT_FILE" \
    --thread-key "$THREAD_KEY" \
    --config "$CONFIG_FILE" \
    ${TELEGRAM_RUNNER_DRY_RUN:+--dry-run} >> "$LOG_FILE" 2>&1; then
    STATUS=0
  else
    STATUS=$?
  fi
fi

{
  echo "[$(timestamp)] END job_id=$JOB_ID status=$STATUS"
} >> "$LOG_FILE"

exit "$STATUS"
