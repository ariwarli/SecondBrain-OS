#!/bin/sh

set -eu

BASE_DIR="$(CDPATH= cd -- "$(dirname "$0")" && pwd)"
LOG_DIR="${TELEGRAM_RUNNER_LOG_DIR:-$BASE_DIR/logs}"

echo "== Scheduler Status =="
date "+Now: %Y-%m-%d %H:%M:%S %Z"
echo

echo "== Crontab =="
crontab -l || true
echo

echo "== Recent Logs =="
if [ -d "$LOG_DIR" ]; then
  for file in "$LOG_DIR"/*.log; do
    [ -e "$file" ] || continue
    echo "-- $(basename "$file")"
    tail -n 3 "$file" || true
    echo
  done
else
  echo "Log directory not found: $LOG_DIR"
fi
