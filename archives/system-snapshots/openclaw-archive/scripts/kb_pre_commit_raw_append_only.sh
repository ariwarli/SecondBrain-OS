#!/usr/bin/env bash
set -euo pipefail

# KB raw/ append-only guard
# - allowed: Add new files under raw/
# - blocked: Modify/Delete/Rename existing files under raw/
#
# Emergency bypass (explicit):
#   KB_ALLOW_RAW_MUTATION=1 git commit ...

if [[ "${KB_ALLOW_RAW_MUTATION:-0}" == "1" ]]; then
  exit 0
fi

violations=()

while IFS=$'\t' read -r status path rest; do
  [[ -z "${status:-}" ]] && continue

  target_path="$path"
  if [[ "$status" == R* || "$status" == C* ]]; then
    # rename/copy format: status <old> <new>
    target_path="$rest"
  fi

  if [[ "$target_path" == raw/* ]]; then
    if [[ "$status" != A* ]]; then
      violations+=("$status $target_path")
    fi
  fi
done < <(git diff --cached --name-status)

if (( ${#violations[@]} > 0 )); then
  echo ""
  echo "ERROR: raw/ bersifat append-only. Commit dibatalkan."
  echo "Pelanggaran:"
  for v in "${violations[@]}"; do
    echo "  - $v"
  done
  echo ""
  echo "Gunakan folder wiki/ untuk revisi ringkasan."
  echo "Jika benar-benar darurat, jalankan sekali dengan:"
  echo "  KB_ALLOW_RAW_MUTATION=1 git commit ..."
  echo ""
  exit 1
fi

exit 0
