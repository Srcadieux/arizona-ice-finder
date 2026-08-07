"""
Arizona Ice Finder — statewide source registry / collector starter.

This file is intentionally conservative: it will NOT overwrite the calendar with
unverified scraper output. Each rink needs a source-specific adapter.

The frontend's stable contract:
  data/rinks.json
  data/events.json

When a live adapter is added, normalize each session to:
  id, title, type, rink, start, end, age, url
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RINKS = json.loads((ROOT / "data" / "rinks.json").read_text())["rinks"]

def main():
    print(f"Arizona Ice Finder: {len(RINKS)} rink facilities configured")
    for rink in RINKS:
        print(f"- {rink['name']} | {rink['city']} | {rink['status']} | {rink['source_url']}")
    print("\nNo live event data was overwritten. Add/test one adapter at a time.")

if __name__ == "__main__":
    main()
