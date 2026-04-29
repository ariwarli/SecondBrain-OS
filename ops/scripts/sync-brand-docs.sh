#!/bin/bash
# sync-brand-docs.sh
# Sync Claude Desktop project docs → ~/banirisset → VPS via git

PROJECT_CACHE="/Users/banirisset/Library/Application Support/Claude/local-agent-mode-sessions/de9b52f6-c0c6-4c2c-956f-fa9fe7bf99a1/4248d960-33d4-4a95-9767-d42b724acd17/.project-cache/019ce2f4-061c-7342-899c-0fe16c10f0fe"
DEST="/Users/banirisset/2_Areas/banirisset/brand-os/claude-project"
REPO="/Users/banirisset/2_Areas/banirisset"

# Copy files
rsync -a --delete "$PROJECT_CACHE/docs/" "$DEST/docs/"
cp "$PROJECT_CACHE/memory.md" "$DEST/memory.md"
cp "$PROJECT_CACHE/metadata.json" "$DEST/metadata.json"

# Git push hanya kalau ada perubahan
cd "$REPO"
if ! git diff --quiet || ! git diff --cached --quiet; then
  git add "brand-os/claude-project/"
  git commit -m "sync: brand docs dari Claude Desktop $(date '+%Y-%m-%d %H:%M')"
  GIT_SSH_COMMAND="ssh -i ~/.ssh/deepthree" git push vps main
fi
