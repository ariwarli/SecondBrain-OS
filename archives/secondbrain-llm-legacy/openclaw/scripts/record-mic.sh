#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OPENCLAW_AUDIO_DIR:-$SCRIPT_DIR/output}"
DEVICE_INDEX="${OPENCLAW_MAC_MIC_DEVICE:-0}"
FORMAT="${OPENCLAW_AUDIO_FORMAT:-m4a}"
DURATION_SECONDS=""
OUTPUT_PATH=""

usage() {
  cat <<'EOF'
Usage:
  record-mic.sh [options]

Options:
  -o, --output PATH       Output file path
  -d, --device INDEX      avfoundation audio device index (default: 0)
  -t, --duration SECONDS  Stop automatically after N seconds
  -f, --format FORMAT     m4a, wav, or mp3 (default: m4a)
      --list-devices      Print available avfoundation devices
  -h, --help              Show this help

Examples:
  scripts/record-mic.sh --list-devices
  scripts/record-mic.sh -t 90
  scripts/record-mic.sh -d 1 -o ~/Desktop/brain-dump.m4a
EOF
}

list_devices() {
  ffmpeg -hide_banner -f avfoundation -list_devices true -i "" 2>&1 || true
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)
      OUTPUT_PATH="${2:-}"
      shift 2
      ;;
    -d|--device)
      DEVICE_INDEX="${2:-}"
      shift 2
      ;;
    -t|--duration)
      DURATION_SECONDS="${2:-}"
      shift 2
      ;;
    -f|--format)
      FORMAT="${2:-}"
      shift 2
      ;;
    --list-devices)
      list_devices
      exit 0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg is required but not installed." >&2
  exit 1
fi

case "$FORMAT" in
  m4a|wav|mp3)
    ;;
  *)
    echo "Unsupported format: $FORMAT" >&2
    exit 1
    ;;
esac

if [[ -z "$OUTPUT_PATH" ]]; then
  mkdir -p "$OUTPUT_DIR"
  timestamp="$(date '+%Y%m%d-%H%M%S')"
  OUTPUT_PATH="$OUTPUT_DIR/voice-$timestamp.$FORMAT"
else
  mkdir -p "$(dirname "$OUTPUT_PATH")"
fi

ffmpeg_args=(
  -hide_banner
  -loglevel
  error
  -f
  avfoundation
  -i
  ":$DEVICE_INDEX"
  -ac
  1
  -ar
  16000
)

if [[ -n "$DURATION_SECONDS" ]]; then
  ffmpeg_args+=(-t "$DURATION_SECONDS")
fi

case "$FORMAT" in
  m4a)
    ffmpeg_args+=(-c:a aac -b:a 96k)
    ;;
  wav)
    ffmpeg_args+=(-c:a pcm_s16le)
    ;;
  mp3)
    ffmpeg_args+=(-c:a libmp3lame -b:a 128k)
    ;;
esac

echo "Recording from mic device $DEVICE_INDEX"
echo "Output: $OUTPUT_PATH"
if [[ -n "$DURATION_SECONDS" ]]; then
  echo "Duration: ${DURATION_SECONDS}s"
else
  echo "Duration: until Ctrl+C"
fi

ffmpeg "${ffmpeg_args[@]}" "$OUTPUT_PATH"

echo "Saved: $OUTPUT_PATH"
