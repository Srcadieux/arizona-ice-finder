#!/usr/bin/env python3
"""
Arizona Ice Finder automatic updater.

Conservative design:
- Only publish sessions that can be parsed with high confidence.
- Never invent times.
- Mullett/Sportified is the primary verified automatic source.
- SportsEngine adapters are best-effort and fail closed.
- DaySmart and PDF calendars remain official-source links until a stable public
  machine-readable feed is available.

The script is suitable for GitHub Actions and updates data/events.json.
"""

from __future__ import annotations

from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from urllib.parse import urljoin
import hashlib
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dtparser

AZ = ZoneInfo("America/Phoenix")
HEADERS = {
    "User-Agent": "Mozilla/5.0 ArizonaIceFinder/1.1 (+GitHub Pages personal rink calendar)"
}
TIMEOUT = 25
ROOT = Path(__file__).resolve().parents[1]
EVENTS_FILE = ROOT / "data" / "events.json"

KEYWORDS = (
    "stick time",
    "stick & puck",
    "stick and puck",
    "open hockey",
    "pickup hockey",
    "pick-up hockey",
    "flow hockey",
    "power skate",
    "hockey skills",
    "hockey clinic",
    "hockey camp",
)


def get(url, **kwargs):
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, **kwargs)
    r.raise_for_status()
    return r


def classify(title):
    low = title.lower()

    if "flow hockey" in low:
        return "Flow Hockey", "Adult"

    if (
        "open hockey" in low
        or "pickup hockey" in low
        or "pick-up hockey" in low
    ):
        return "Open Hockey", "Adult"

    if (
        "stick time" in low
        or "stick & puck" in low
        or "stick and puck" in low
    ):
        if "adult" in low:
            age = "Adult"
        elif any(x in low for x in ["youth", "mite", "squirt", "peewee", "bantam"]):
            age = "Youth"
        else:
            age = "All"
        return "Stick Time", age

    if any(
        x in low
        for x in ["power skate", "hockey skills", "hockey clinic", "hockey camp"]
    ):
        return "Clinic", ("Youth" if "youth" in low else "All")

    return None, None


def iso_local(date_str, time_str):
    dt = dtparser.parse(f"{date_str} {time_str}", fuzzy=True)
    return dt.replace(tzinfo=AZ)


def midnight_az(day):
    """Convert a date to an Arizona-aware midnight datetime."""
    return datetime.combine(day, time.min, tzinfo=AZ)


def stable_id(source, rink, start, title):
    raw = f"{source}|{rink}|{start.isoformat()}|{title}".encode()
    return source + "-" + hashlib.sha1(raw).hexdigest()[:12]


def collect_mullett(today):
    base = "https://mullett.sportified.net"
    rink = "Mullett Arena / Mountain America Community Iceplex"
    events = []
    cutoff = midnight_az(today - timedelta(days=1))

    starts = [
        today - timedelta(days=1),
        today + timedelta(days=6),
        today + timedelta(days=13),
        today + timedelta(days=20),
        today + timedelta(days=27),
    ]

    seen = set()

    date_re = re.compile(
        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
        r"([A-Za-z]+)\s+(\d{1,2})\s+(\d{4})$"
    )
    time_re = re.compile(
        r"^(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*(\d{1,2}:\d{2}\s*[ap]m)$",
        re.I,
    )

    for start_date in starts:
        url = f"{base}/schedule?date={start_date.isoformat()}"

        try:
            soup = BeautifulSoup(get(url).text, "html.parser")
        except Exception as exc:
            print("Mullett fetch failed:", url, exc, file=sys.stderr)
            continue

        current_date = None

        for node in soup.find_all(["h1", "h2", "h3", "h4", "h5", "tr"]):
            text_value = " ".join(node.stripped_strings)
            md = date_re.match(text_value)

            if md:
                current_date = text_value
                continue

            if node.name != "tr" or not current_date:
                continue

            cells = [
                " ".join(td.stripped_strings)
                for td in node.find_all(["td", "th"])
            ]

            if len(cells) < 2:
                continue

            mt = time_re.match(cells[0])
            if not mt:
                continue

            title = cells[1].strip()
            typ, age = classify(title)

            if not typ:
                continue

            start_dt = iso_local(current_date, mt.group(1))
            end_dt = iso_local(current_date, mt.group(2))

            if end_dt <= start_dt:
                end_dt += timedelta(days=1)

            if start_dt < cutoff:
                continue

            link = url
            for anchor in node.find_all("a", href=True):
                href = anchor["href"]
                if (
                    "product" in href
                    or "register" in anchor.get_text(" ", strip=True).lower()
                ):
                    link = urljoin(base, href)
                    break

            key = (start_dt.isoformat(), title)
            if key in seen:
                continue

            seen.add(key)
            events.append(
                {
                    "id": stable_id("mullett", rink, start_dt, title),
                    "title": title,
                    "type": typ,
                    "rink": rink,
                    "start": start_dt.isoformat(),
                    "end": end_dt.isoformat(),
                    "age": age,
                    "url": link,
                    "source": "mullett",
                }
            )

        # Fallback text parser if the table layout changes.
        if not any(e["url"].startswith(url) for e in events):
            lines = [
                x.strip()
                for x in soup.get_text("\n").splitlines()
                if x.strip()
            ]
            current_date = None
            i = 0

            while i < len(lines):
                if date_re.match(lines[i]):
                    current_date = lines[i]
                    i += 1
                    continue

                mt = time_re.match(lines[i])

                if current_date and mt and i + 1 < len(lines):
                    title = lines[i + 1]
                    typ, age = classify(title)

                    if typ:
                        start_dt = iso_local(current_date, mt.group(1))
                        end_dt = iso_local(current_date, mt.group(2))

                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)

                        if start_dt >= cutoff:
                            key = (start_dt.isoformat(), title)

                            if key not in seen:
                                seen.add(key)
                                events.append(
                                    {
                                        "id": stable_id(
                                            "mullett", rink, start_dt, title
                                        ),
                                        "title": title,
                                        "type": typ,
                                        "rink": rink,
                                        "start": start_dt.isoformat(),
                                        "end": end_dt.isoformat(),
                                        "age": age,
                                        "url": url,
                                        "source": "mullett",
                                    }
                                )

                    i += 2
                    continue

                i += 1

    return events


SPORTSENGINE = [
    (
        "Ice Den Scottsdale",
        "https://www.icedenscottsdale.com",
        "https://www.icedenscottsdale.com/node_list/node_list?model=event",
    ),
    (
        "Ice Den Chandler",
        "https://www.icedenchandler.com",
        "https://www.icedenchandler.com/page/show/2803608-calendar",
    ),
    (
        "Coyotes Community Ice Center",
        "https://www.coyotescommunityicecenter.com",
        "https://www.coyotescommunityicecenter.com/page/show/5540662-calendar",
    ),
]


def collect_sportsengine(today):
    out = []
    cutoff = midnight_az(today - timedelta(days=1))
    event_link_re = re.compile(r"/event/show/\d+")

    for rink, base, calendar in SPORTSENGINE:
        candidates = {}
        urls = [calendar]

        for offset in (0, 31):
            d = today + timedelta(days=offset)
            sep = "&" if "?" in calendar else "?"
            urls.append(f"{calendar}{sep}mth={d.month}&yr={d.year}")

        for url in urls:
            try:
                html = get(url).text
            except Exception as exc:
                print("SportsEngine index failed:", rink, url, exc, file=sys.stderr)
                continue

            soup = BeautifulSoup(html, "html.parser")

            for anchor in soup.find_all("a", href=True):
                href = anchor["href"]
                label = " ".join(anchor.stripped_strings)

                if (
                    event_link_re.search(href)
                    and any(k in label.lower() for k in KEYWORDS)
                ):
                    candidates[urljoin(base, href)] = label

            for match in re.finditer(
                r'["\']([^"\']*/event/show/\d+[^"\']*)["\']',
                html,
            ):
                href = match.group(1).replace("\\/", "/")
                candidates.setdefault(urljoin(base, href), "")

        for event_url, label in list(candidates.items())[:80]:
            try:
                soup = BeautifulSoup(get(event_url).text, "html.parser")
                title_node = soup.find("h1") or soup.find("h2")
                title = (
                    " ".join(title_node.stripped_strings)
                    if title_node
                    else label
                )

                typ, age = classify(title)
                if not typ:
                    continue

                text_value = " ".join(soup.stripped_strings)

                match = re.search(
                    r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s*-\s*"
                    r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s+"
                    r"([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4})",
                    text_value,
                    re.I,
                )

                if not match:
                    continue

                date_clean = re.sub(
                    r"(\d{1,2})(st|nd|rd|th)",
                    r"\1",
                    match.group(3),
                    flags=re.I,
                )

                start_dt = dtparser.parse(
                    f"{date_clean} {match.group(1)}"
                ).replace(tzinfo=AZ)

                end_dt = dtparser.parse(
                    f"{date_clean} {match.group(2)}"
                ).replace(tzinfo=AZ)

                if end_dt <= start_dt:
                    end_dt += timedelta(days=1)

                if start_dt < cutoff:
                    continue

                out.append(
                    {
                        "id": stable_id(
                            "sportsengine", rink, start_dt, title
                        ),
                        "title": title,
                        "type": typ,
                        "rink": rink,
                        "start": start_dt.isoformat(),
                        "end": end_dt.isoformat(),
                        "age": age,
                        "url": event_url,
                        "source": "sportsengine",
                    }
                )

            except Exception as exc:
                print(
                    "SportsEngine event failed:",
                    rink,
                    event_url,
                    exc,
                    file=sys.stderr,
                )

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    return list(dedup.values())


def main():
    today = datetime.now(AZ).date()

    collected = []
    collected += collect_mullett(today)
    collected += collect_sportsengine(today)
    collected.sort(key=lambda e: e["start"])

    # Fail-safe: never blank the website if a source is unavailable or changes layout.
    if not collected:
        print(
            "No events collected. Preserving existing data/events.json.",
            file=sys.stderr,
        )
        return 0

    live_names = sorted(
        set(e["rink"] for e in collected if e["source"] == "mullett")
    )
    auto_names = sorted(
        set(e["rink"] for e in collected if e["source"] == "sportsengine")
    )

    payload = {
        "updated": datetime.now(AZ).isoformat(),
        "mode": "live-partial",
        "source_summary": {
            "live_auto": live_names,
            "auto_attempt": auto_names,
            "official_link": [
                "AZ Ice Arcadia",
                "AZ Ice Gilbert",
                "AZ Ice Peoria",
                "Jay Lively Activity Center",
                "Findlay Toyota Center",
                "Tucson Convention Center / Tucson Arena",
            ],
            "future": [
                "Fire 'n' Ice Sports Arena",
                "MQ Iceplex at Mosaic Quarter",
            ],
        },
        "events": collected,
    }

    EVENTS_FILE.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"Wrote {len(collected)} collected events.")
    for name in sorted(set(e["rink"] for e in collected)):
        count = sum(1 for e in collected if e["rink"] == name)
        print(f" - {name}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
