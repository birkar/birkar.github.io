#!/bin/bash
# Pulls the public CSV export of the "log (Responses)" sheet to data/sheet_raw.csv.
set -euo pipefail
cd "$(dirname "$0")/.."

SHEET_URL="https://docs.google.com/spreadsheets/d/1ccddSZjlNvuGXzcRa0xbMXA1Jb0LbZ7Vr1cwQD0mb1c/export?format=csv"

curl -sL "$SHEET_URL" -o data/sheet_raw.csv

if ! file data/sheet_raw.csv | grep -qi "csv\|ascii\|utf-8"; then
  echo "fetch_sheet: response doesn't look like CSV (sheet sharing may have changed)" >&2
  exit 1
fi

if ! head -1 data/sheet_raw.csv | grep -q "Timestamp"; then
  echo "fetch_sheet: unexpected header row, aborting" >&2
  exit 1
fi
