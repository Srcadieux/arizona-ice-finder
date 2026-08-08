#!/usr/bin/env python3
"""Arizona Ice Finder updater.

Live now: Mullett, Ice Den Scottsdale, Ice Den Chandler, AZ Ice Arcadia.
Diagnostic only: finds AZ Ice Gilbert's DaySmart facility ID.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin
from zoneinfo import ZoneInfo
import hashlib, json, re, sys

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dtparser
from dateutil.rrule import rrulestr

AZ = ZoneInfo("America/Phoenix")
ROOT = Path(__file__).resolve().parents[1]
EVENTS_FILE = ROOT / "data" / "events.json"
TIMEOUT = 25
HEADERS = {"User-Agent": "Mozilla/5.0 ArizonaIceFinder/2.0"}
DAYSMART_EVENTS = "https://apps.daysmartrecreation.com/dash/jsonapi/api/v1/events"


def fetch(url, **kwargs):
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, **kwargs)
    r.raise_for_status()
    return r


def clean(v):
    return re.sub(
        r"\s+",
        " ",
        BeautifulSoup(str(v or ""), "html.parser").get_text(" ", strip=True),
    ).strip()


def sid(source, rink, start, title):
    raw = f"{source}|{rink}|{start.isoformat()}|{title}".encode()
    return source + "-" + hashlib.sha1(raw).hexdigest()[:12]


def classify(title):
    low = clean(title).lower()

    youth = any(
        x in low
        for x in (
            "youth",
            "mite",
            "squirt",
            "peewee",
            "bantam",
            "8u",
            "10u",
            "12u",
            "14u",
            "16u",
            "18u",
        )
    )

    adult = "adult" in low or "18+" in low
    age = "Youth" if youth else ("Adult" if adult else "All")

    if "flow hockey" in low:
        return "Flow Hockey", "Adult"

    if any(
        x in low
        for x in (
            "open hockey",
            "pickup hockey",
            "pick up hockey",
            "pick-up hockey",
            "drop-in hockey",
            "drop in hockey",
        )
    ):
        return "Open Hockey", age

    if any(
        x in low
        for x in (
            "stick time",
            "sticktime",
            "stick & puck",
            "stick and puck",
            "stick n puck",
            "stick-n-puck",
        )
    ):
        return "Stick Time", age

    if any(
        x in low
        for x in (
            "hockey skills",
            "hockey clinic",
            "hockey camp",
            "power skate",
        )
    ):
        return "Clinic", age

    return None, None


# ------------------------------------------------------------
# MULLETT
# ------------------------------------------------------------

def collect_mullett(today):
    rink = "Mullett Arena / Mountain America Community Iceplex"
    base = "https://mullett.sportified.net"

    cutoff = datetime.combine(
        today - timedelta(days=1),
        datetime.min.time(),
        tzinfo=AZ,
    )

    date_re = re.compile(
        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
        r"[A-Za-z]+\s+\d{1,2}\s+\d{4}$"
    )

    time_re = re.compile(
        r"^(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*"
        r"(\d{1,2}:\d{2}\s*[ap]m)$",
        re.I,
    )

    out = []
    seen = set()

    query_dates = (
        today - timedelta(days=1),
        today + timedelta(days=6),
        today + timedelta(days=13),
        today + timedelta(days=20),
        today + timedelta(days=27),
    )

    for query_date in query_dates:
        url = f"{base}/schedule?date={query_date.isoformat()}"

        try:
            soup = BeautifulSoup(fetch(url).text, "html.parser")
        except Exception as exc:
            print("Mullett fetch failed:", exc, file=sys.stderr)
            continue

        current_date = None

        for node in soup.find_all(
            ["h1", "h2", "h3", "h4", "h5", "tr"]
        ):
            text = " ".join(node.stripped_strings)

            if date_re.match(text):
                current_date = text
                continue

            if node.name != "tr" or not current_date:
                continue

            cells = [
                " ".join(x.stripped_strings)
                for x in node.find_all(["td", "th"])
            ]

            if len(cells) < 2:
                continue

            match = time_re.match(cells[0])

            if not match:
                continue

            title = cells[1].strip()
            typ, age = classify(title)

            if not typ:
                continue

            start = dtparser.parse(
                f"{current_date} {match.group(1)}",
                fuzzy=True,
            ).replace(tzinfo=AZ)

            end = dtparser.parse(
                f"{current_date} {match.group(2)}",
                fuzzy=True,
            ).replace(tzinfo=AZ)

            if end <= start:
                end += timedelta(days=1)

            if start < cutoff:
                continue

            link = url

            for anchor in node.find_all("a", href=True):
                if (
                    "product" in anchor["href"]
                    or "register"
                    in anchor.get_text(" ", strip=True).lower()
                ):
                    link = urljoin(base, anchor["href"])
                    break

            key = (start.isoformat(), title)

            if key in seen:
                continue

            seen.add(key)

            out.append(
                {
                    "id": sid("mullett", rink, start, title),
                    "title": title,
                    "type": typ,
                    "rink": rink,
                    "start": start.isoformat(),
                    "end": end.isoformat(),
                    "age": age,
                    "url": link,
                    "source": "mullett",
                }
            )

    print(f"Mullett: {len(out)} hockey sessions")
    return out


# ------------------------------------------------------------
# SPORTSENGINE ICAL
# ------------------------------------------------------------

def unfold_ical(text):
    out = []

    for line in (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .split("\n")
    ):
        if line.startswith((" ", "\t")) and out:
            out[-1] += line[1:]
        else:
            out.append(line)

    return out


def parse_ical(text):
    events = []
    current = None

    for line in unfold_ical(text):
        if line == "BEGIN:VEVENT":
            current = {}
            continue

        if line == "END:VEVENT":
            if current is not None:
                events.append(current)

            current = None
            continue

        if current is None or ":" not in line:
            continue

        key, value = line.split(":", 1)
        base = key.split(";", 1)[0]

        current.setdefault(base, []).append((key, value))

    return events


def ical_dt(key, value):
    tzid = None

    for param in key.split(";")[1:]:
        if param.startswith("TZID="):
            tzid = param.split("=", 1)[1]

    value = value.strip()

    if re.fullmatch(r"\d{8}", value):
        day = datetime.strptime(value, "%Y%m%d").date()

        return datetime.combine(
            day,
            datetime.min.time(),
            tzinfo=AZ,
        )

    if value.endswith("Z"):
        return (
            datetime.strptime(value, "%Y%m%dT%H%M%SZ")
            .replace(tzinfo=ZoneInfo("UTC"))
            .astimezone(AZ)
        )

    dt = datetime.strptime(value, "%Y%m%dT%H%M%S")

    if tzid:
        try:
            return dt.replace(
                tzinfo=ZoneInfo(tzid)
            ).astimezone(AZ)
        except Exception:
            pass

    return dt.replace(tzinfo=AZ)


def collect_ical(
    today,
    rink,
    source,
    feeds,
    default_url,
):
    out = []

    window_start = datetime.combine(
        today - timedelta(days=1),
        datetime.min.time(),
        tzinfo=AZ,
    )

    window_end = datetime.combine(
        today + timedelta(days=35),
        datetime.max.time(),
        tzinfo=AZ,
    )

    for feed in feeds:
        try:
            text = fetch(feed).text

            if "BEGIN:VCALENDAR" not in text:
                raise ValueError("not iCal")

        except Exception as exc:
            print(
                f"{rink} iCal failed: {exc}",
                file=sys.stderr,
            )
            continue

        for event in parse_ical(text):
            if not event.get("SUMMARY") or not event.get("DTSTART"):
                continue

            title = (
                event["SUMMARY"][0][1]
                .replace("\\,", ",")
                .replace("\\n", " ")
                .strip()
            )

            typ, age = classify(title)

            if not typ:
                continue

            start = ical_dt(*event["DTSTART"][0])

            if event.get("DTEND"):
                end = ical_dt(*event["DTEND"][0])
            else:
                end = start + timedelta(hours=1)

            duration = (
                end - start
                if end > start
                else timedelta(hours=1)
            )

            if event.get("RRULE"):
                try:
                    occurrences = list(
                        rrulestr(
                            event["RRULE"][0][1],
                            dtstart=start,
                        ).between(
                            window_start,
                            window_end,
                            inc=True,
                        )
                    )

                except Exception:
                    occurrences = []

            else:
                occurrences = (
                    [start]
                    if window_start <= start <= window_end
                    else []
                )

            link = default_url

            if event.get("URL"):
                link = event["URL"][0][1].strip()

            for occurrence in occurrences:
                if occurrence.tzinfo:
                    occurrence = occurrence.astimezone(AZ)
                else:
                    occurrence = occurrence.replace(tzinfo=AZ)

                occurrence_end = occurrence + duration

                out.append(
                    {
                        "id": sid(
                            source,
                            rink,
                            occurrence,
                            title,
                        ),
                        "title": title,
                        "type": typ,
                        "rink": rink,
                        "start": occurrence.isoformat(),
                        "end": occurrence_end.isoformat(),
                        "age": age,
                        "url": link,
                        "source": source,
                    }
                )

    dedup = {
        (
            event["rink"],
            event["start"],
            event["end"],
            event["title"],
        ): event
        for event in out
    }

    result = sorted(
        dedup.values(),
        key=lambda event: event["start"],
    )

    print(
        f"{rink}: {len(result)} hockey sessions"
    )

    return result


SCOTTSDALE_FEEDS = (
    "https://www.icedenscottsdale.com/ical_feed?"
    "tags=2670384%2C2670407%2C2678497%2C2662957",

    "https://www.icedenscottsdale.com/ical_feed?"
    "tags=2670384%2C2670407%2C2665577%2C2678497%2C2662957",
)


CHANDLER_FEEDS = (
    "https://www.icedenchandler.com/ical_feed?tags=2703965%2C2703970%2C2711738",
    "https://www.icedenchandler.com/ical_feed?tags=2703965",
    "https://www.icedenchandler.com/ical_feed?tags=2703970",
    "https://www.icedenchandler.com/ical_feed?tags=2711738",
)

def collect_scottsdale(today):
    return collect_ical(
        today, "Ice Den Scottsdale", "icedenscottsdale", SCOTTSDALE_FEEDS,
        "https://www.icedenscottsdale.com/page/show/2662960-calendar"
    )

def collect_chandler(today):
    return collect_ical(
        today, "Ice Den Chandler", "icedenchandler", CHANDLER_FEEDS,
        "https://www.icedenchandler.com/page/show/2803608-calendar"
    )

def ds_lookup(payload):
    out = {}
    for obj in payload.get("included", []) if isinstance(payload, dict) else []:
        a = obj.get("attributes") or {}
        name = a.get("name") or a.get("title") or a.get("desc") or a.get("description")
        if name:
            out[(str(obj.get("type") or ""), str(obj.get("id") or ""))] = clean(name)
    return out

def ds_dt(value):
    dt = dtparser.isoparse(str(value))
    return dt.replace(tzinfo=AZ) if dt.tzinfo is None else dt.astimezone(AZ)

def day_smart_payload(today, facility_id, days=35):
    params = {
        "company": "azice",
        "filter[facility_id]": str(facility_id),
        "filter[start_date]": today.isoformat(),
        "filter[end_date]": (today + timedelta(days=days)).isoformat(),
        "include": "eventType,resource,resourceArea,league,homeTeam,visitingTeam",
    }

    headers = {
        **HEADERS,
        "Accept": "application/vnd.api+json, application/json;q=0.9, */*;q=0.8",
        "Origin": "https://member.daysmartrecreation.com",
    }

    r = requests.get(
        DAYSMART_EVENTS,
        params=params,
        headers=headers,
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    return r.json()

def collect_arcadia(today):
    rink = "AZ Ice Arcadia"
    url = (
        "https://member.daysmartrecreation.com/"
        "#/online/azice/calendar?location=3"
    )

    try:
        payload = day_smart_payload(today, 3, 35)
    except Exception as exc:
        print("Arcadia DaySmart failed:", exc, file=sys.stderr)
        return []

    lookup = ds_lookup(payload)

    leagues = {
        i: n for (t, i), n in lookup.items()
        if t == "leagues"
    }

    teams = {
        i: n for (t, i), n in lookup.items()
        if t == "teams"
    }

    event_types = {
        i: n for (t, i), n in lookup.items()
        if t == "event-types"
    }

    out = []
    raw = payload.get("data", [])

    for item in raw:
        a = item.get("attributes") or {}

        try:
            start = ds_dt(a.get("start"))
            end = ds_dt(a.get("end"))
        except Exception:
            continue

        labels = []

        if a.get("league_id") is not None:
            name = leagues.get(str(a["league_id"]))
            if name:
                labels.append(name)

        if a.get("team_id") is not None:
            name = teams.get(str(a["team_id"]))
            if name:
                labels.append(name)

        for key in ("desc", "description"):
            if a.get(key):
                labels.append(clean(a[key]))

        if a.get("event_type_id") is not None:
            name = event_types.get(str(a["event_type_id"]))
            if name:
                labels.append(name)

        labels = list(dict.fromkeys(x for x in labels if x))

        combined = " | ".join(labels)
        typ, age = classify(combined)

        if not typ:
            continue

        source_title = next(
            (x for x in labels if classify(x)[0]),
            combined,
        )

        if typ == "Open Hockey":
            title = (
                "Adult Pick Up Hockey"
                if age == "Adult"
                else "Youth Open Hockey"
                if age == "Youth"
                else "Open Hockey"
            )

        elif typ == "Stick Time":
            title = (
                "Adult Stick Time"
                if age == "Adult"
                else "Youth Stick Time"
                if age == "Youth"
                else "Stick Time"
            )

        else:
            title = source_title

        out.append({
            "id": sid("azicearcadia", rink, start, title),
            "title": title,
            "type": typ,
            "rink": rink,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "age": age,
            "url": url,
            "source": "azicearcadia",
        })

    result = sorted(
        {
            (e["rink"], e["start"], e["end"], e["title"]): e
            for e in out
        }.values(),
        key=lambda e: e["start"],
    )

    print(
        f"AZ Ice Arcadia DaySmart: "
        f"{len(result)} public hockey sessions "
        f"from {len(raw)} returned events"
    )

    return result

def diagnose_gilbert(today):
    print("AZ Ice Gilbert facility discovery BEGIN")

    for facility_id in range(1, 13):
        try:
            payload = day_smart_payload(today, facility_id, 7)

        except Exception as exc:
            print(
                f"GILBERT_PROBE facility_id={facility_id} FAILED: {exc}",
                file=sys.stderr,
            )
            continue

        data = payload.get("data", [])
        lookup = ds_lookup(payload)

        ids = {
            "resources": set(),
            "resource-areas": set(),
            "leagues": set(),
            "teams": set(),
        }

        for item in data:
            a = item.get("attributes") or {}

            if a.get("resource_id") is not None:
                ids["resources"].add(str(a["resource_id"]))

            if a.get("resource_area_id") is not None:
                ids["resource-areas"].add(str(a["resource_area_id"]))

            if a.get("league_id") is not None:
                ids["leagues"].add(str(a["league_id"]))

            for key in (
                "team_id",
                "home_team_id",
                "visiting_team_id",
            ):
                if a.get(key) is not None:
                    ids["teams"].add(str(a[key]))

        names = {
            typ: sorted({
                lookup[(typ, i)]
                for i in vals
                if (typ, i) in lookup
            })
            for typ, vals in ids.items()
        }

        clue = " | ".join(
            names["resources"]
            + names["resource-areas"]
            + names["leagues"]
            + names["teams"]
        ).lower()

        likely = (
            "north pole" in clue
            or "south pole" in clue
        )

        print(
            f"GILBERT_PROBE facility_id={facility_id} "
            f"events={len(data)} "
            f"{'<<< LIKELY GILBERT >>>' if likely else ''}"
        )

        print(
            "  resources:",
            names["resources"] or "none",
        )

        print(
            "  areas:",
            names["resource-areas"] or "none",
        )

        print(
            "  leagues:",
            names["leagues"][:20] or "none",
        )

    print("AZ Ice Gilbert facility discovery END")

def main():
    today = datetime.now(AZ).date()

    diagnose_gilbert(today)

    collected = (
        collect_arcadia(today)
        + collect_mullett(today)
        + collect_scottsdale(today)
        + collect_chandler(today)
    )

    collected.sort(
        key=lambda e: e["start"]
    )

    if not collected:
        print(
            "No events collected. "
            "Preserving existing data/events.json.",
            file=sys.stderr,
        )
        return 0

    payload = {
        "updated": datetime.now(AZ).isoformat(),

        "mode": "live-partial",

        "source_summary": {
            "live_auto": sorted({
                e["rink"]
                for e in collected
            }),

            "auto_attempt": [],

            "official_link": [
                "AZ Ice Gilbert",
                "AZ Ice Peoria",
                "Coyotes Community Ice Center",
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

    EVENTS_FILE.write_text(
        json.dumps(payload, indent=2) + "\n"
    )

    print(
        f"Wrote {len(collected)} collected events."
    )

    for rink in sorted({
        e["rink"]
        for e in collected
    }):
        count = sum(
            1
            for e in collected
            if e["rink"] == rink
        )

        print(
            f" - {rink}: {count}"
        )

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
