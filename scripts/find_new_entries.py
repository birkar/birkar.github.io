#!/usr/bin/env python3
"""
Compares data/sheet_raw.csv against the last-processed timestamp cursor,
extracts new-row پڑھن (reading) entries, and writes them to data/.pending.json
for the enrichment step. Prints the pending item count to stdout (only).
"""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = ROOT / "data" / "sheet_raw.csv"
CURSOR_FILE = ROOT / "data" / ".last_synced_ts"
PENDING_FILE = ROOT / "data" / ".pending.json"
PENDING_TS_FILE = ROOT / "data" / ".pending_ts"

COL_TIMESTAMP = "Timestamp"
COL_START_DATE = "آغاز تاریخ"
COL_READING = "پڑھن"

TS_FORMAT = "%m/%d/%Y %H:%M:%S"
DATE_FORMAT = "%m/%d/%Y"


def parse_timestamp(raw: str) -> datetime:
    return datetime.strptime(raw.strip(), TS_FORMAT)


def row_date(row: dict, ts: datetime) -> str:
    start = row.get(COL_START_DATE, "").strip()
    if start:
        try:
            return datetime.strptime(start, DATE_FORMAT).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return ts.strftime("%Y-%m-%d")


def main() -> int:
    if not RAW_CSV.exists():
        print("find_new_entries: data/sheet_raw.csv missing, run fetch_sheet.sh first", file=sys.stderr)
        return 1

    last_synced = None
    if CURSOR_FILE.exists():
        cursor_raw = CURSOR_FILE.read_text().strip()
        if cursor_raw:
            last_synced = parse_timestamp(cursor_raw)

    with RAW_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    pending = []
    max_ts = last_synced
    max_ts_raw = CURSOR_FILE.read_text().strip() if CURSOR_FILE.exists() else ""

    for row in rows:
        ts_raw = row.get(COL_TIMESTAMP, "").strip()
        if not ts_raw:
            continue
        ts = parse_timestamp(ts_raw)

        if last_synced is not None and ts <= last_synced:
            continue

        if max_ts is None or ts > max_ts:
            max_ts = ts
            max_ts_raw = ts_raw

        reading_cell = row.get(COL_READING, "") or ""
        for line in reading_cell.splitlines():
            line = line.strip()
            if line:
                pending.append({"row_date": row_date(row, ts), "raw": line})

    PENDING_FILE.write_text(json.dumps(pending, ensure_ascii=False, indent=2))
    if max_ts_raw:
        PENDING_TS_FILE.write_text(max_ts_raw)

    print(len(pending))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
