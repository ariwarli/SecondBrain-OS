#!/bin/bash
# Usage: ./set_reminder.sh "Pesan untuk Bani" "waktu (e.g. tomorrow 15:00)"
if [ "$#" -ne 2 ]; then
  echo "Error: Need exactly 2 arguments: 'message' and 'time'."
  exit 1
fi
MSG="$1"
TIME="$2"
echo "set -a; . /home/hermes/banirisset/automation/telegram-runner.env; set +a; /usr/bin/python3 /home/hermes/banirisset/automation/telegram_runner.py --job-id reminder --thread-key inbox --config /home/hermes/banirisset/automation/telegram-config.json --message \"🔔 REMINDER DARI REED: $MSG\"" | at "$TIME"
echo "Reminder successfully scheduled for: $TIME"
