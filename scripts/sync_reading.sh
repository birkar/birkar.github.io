#!/bin/bash
# Weekly orchestrator: fetch sheet -> find new پڑھن entries -> enrich via
# headless Claude -> rebuild parhan/data.json -> commit & push if changed.
# Run manually to test, or via the com.birkar.parhan-sync launchd job.
set -euo pipefail
cd "$(dirname "$0")/.."

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

log "starting sync"

./scripts/fetch_sheet.sh
NEW_COUNT=$(python3 scripts/find_new_entries.py)
log "found $NEW_COUNT new پڑھن item(s) since last sync"

if [ "$NEW_COUNT" -gt 0 ]; then
  ./scripts/enrich_and_append.sh
  python3 scripts/build_json.py

  if [ -f data/.pending_ts ]; then
    cp data/.pending_ts data/.last_synced_ts
  fi

  git add data/reading.csv parhan/data.json data/.last_synced_ts

  if git diff --cached --quiet; then
    log "enrichment ran but produced no net changes"
  else
    git commit -m "parhan: weekly sync $(date '+%Y-%m-%d'), $NEW_COUNT item(s) evaluated"
    git push origin main
    log "pushed update"
  fi
else
  log "nothing new"
fi

rm -f data/.pending.json data/.pending_ts
log "done"
