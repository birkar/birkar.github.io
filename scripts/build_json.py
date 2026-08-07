#!/usr/bin/env python3
"""Regenerates parhan/data.json from data/reading.csv, newest first."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING_CSV = ROOT / "data" / "reading.csv"
OUT_JSON = ROOT / "parhan" / "data.json"

FIELDS = ["date", "author", "title", "format", "url", "tags"]


def main() -> None:
    entries = []
    if READING_CSV.exists():
        with READING_CSV.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                entry = {k: row.get(k, "").strip() for k in FIELDS}
                entry["tags"] = [t.strip() for t in entry["tags"].split(";") if t.strip()]
                entries.append(entry)

    entries.sort(key=lambda e: e["date"], reverse=True)
    OUT_JSON.write_text(json.dumps(entries, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
