#!/bin/bash
# Runs headless Claude Code to resolve pending پڑھن entries into structured
# rows and append them to data/reading.csv. No-ops if nothing is pending.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -s data/.pending.json ] || [ "$(cat data/.pending.json)" = "[]" ]; then
  echo "enrich_and_append: nothing pending"
  exit 0
fi

claude -p "$(cat scripts/enrich_prompt.txt)" \
  --allowedTools "Read,Write,Edit,WebSearch,WebFetch" \
  --output-format text
