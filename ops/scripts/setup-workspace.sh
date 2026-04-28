#!/bin/bash
# Setup workspace Bani Risset
# Jalankan sekali: bash setup-workspace.sh

ROOT="$HOME/banirisset"

mkdir -p "$ROOT/personal-brand/threads"
mkdir -p "$ROOT/personal-brand/ideas-bank"
mkdir -p "$ROOT/personal-brand/research"

mkdir -p "$ROOT/clients/_template/briefs"
mkdir -p "$ROOT/clients/_template/deliverables"
mkdir -p "$ROOT/clients/_template/research"
mkdir -p "$ROOT/clients/_template/content"

mkdir -p "$ROOT/ops/scripts"
mkdir -p "$ROOT/ops/templates"
mkdir -p "$ROOT/ops/archive"

# File placeholder
touch "$ROOT/personal-brand/threads/.gitkeep"
touch "$ROOT/clients/_template/notes.md"
touch "$ROOT/ops/scripts/.gitkeep"

echo "✓ Workspace siap di $ROOT"
