#!/usr/bin/env python3
"""
Arizona Ice Finder automatic updater.

Live sources:
- Mullett / Mountain America Community Iceplex: public Sportified schedule.
- Ice Den Scottsdale: official SportsEngine iCal calendar feed.
- Ice Den Chandler: official SportsEngine iCal discovery + official-page fallback.
- Coyotes Community Ice Center: best-effort SportsEngine HTML fallback.

Conservative design:
- Only publish sessions that can be parsed with high confidence.
- Never invent times.
- If a source fails, the script preserves the last known event file rather than
  blanking the live website.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urljoin
import hashlib
import json
import re
import sys

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dtparser
from dateutil.rrule import rrulestr

AZ = ZoneInfo("America/Phoenix")
HEADERS = {
    "User-Agent": "Mozilla/5.0 ArizonaIceFinder/1.2 (+GitHub Pages personal rink calendar)"
}
TIMEOUT = 25
ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
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

ICE_DEN_SCOTTSDALE_ICAL_FEEDS = (
    # Current Ice Den Scottsdale calendar tag set surfaced by its official iCal page.
    "https://www.icedenscottsdale.com/ical_feed?tags=2670384%2C2670407%2C2678497%2C2662957",
    # Alternate current/legacy tag set also surfaced by the official calendar.
    "https://www.icedenscottsdale.com/ical_feed?tags=2670384%2C2670407%2C2665577%2C2678497%2C2662957",
    # Full/default calendar feed fallback.
    "https://www.icedenscottsdale.com/ical_feed?tags=",
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
        elif any(
            x in low
            for x in ("youth", "mite", "squirt", "peewee", "bantam")
        ):
            age = "Youth"
        else:
            age = "All"
        return "Stick Time", age

    if any(
        x in low
        for x in ("power skate", "hockey skills", "hockey clinic", "hockey camp")
    ):
        return "Clinic", ("Youth" if "youth" in low else "All")

    return None, None


def iso_local(date_str, time_str):
    dt = dtparser.parse(f"{date_str} {time_str}", fuzzy=True)
    return dt.replace(tzinfo=AZ)


def stable_id(source, rink, start, title):
    raw = f"{source}|{rink}|{start.isoformat()}|{title}".encode()
    return source + "-" + hashlib.sha1(raw).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Mullett / Sportified
# ---------------------------------------------------------------------------

def collect_mullett(today):
    base = "https://mullett.sportified.net"
    rink = "Mullett Arena / Mountain America Community Iceplex"
    events = []

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
    cutoff = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
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
            text = " ".join(node.stripped_strings)
            match_date = date_re.match(text)

            if match_date:
                current_date = text
                continue

            if node.name != "tr" or not current_date:
                continue

            cells = [
                " ".join(td.stripped_strings)
                for td in node.find_all(["td", "th"])
            ]

            if len(cells) < 2:
                continue

            match_time = time_re.match(cells[0])
            if not match_time:
                continue

            title = cells[1].strip()
            typ, age = classify(title)

            if not typ:
                continue

            start_dt = iso_local(current_date, match_time.group(1))
            end_dt = iso_local(current_date, match_time.group(2))

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

        # Fallback text parser if Sportified changes table markup.
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

                match_time = time_re.match(lines[i])

                if current_date and match_time and i + 1 < len(lines):
                    title = lines[i + 1]
                    typ, age = classify(title)

                    if typ:
                        start_dt = iso_local(current_date, match_time.group(1))
                        end_dt = iso_local(current_date, match_time.group(2))

                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)

                        if start_dt >= cutoff:
                            key = (start_dt.isoformat(), title)

                            if key not in seen:
                                seen.add(key)
                                events.append(
                                    {
                                        "id": stable_id(
                                            "mullett",
                                            rink,
                                            start_dt,
                                            title,
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


# ---------------------------------------------------------------------------
# Ice Den Scottsdale — official SportsEngine iCal feed
# ---------------------------------------------------------------------------

def unfold_ical(text):
    """Unfold RFC 5545 continuation lines."""
    physical = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    logical = []

    for line in physical:
        if line.startswith((" ", "\t")) and logical:
            logical[-1] += line[1:]
        else:
            logical.append(line)

    return logical


def unescape_ical_text(value):
    return (
        value.replace("\\n", " ")
        .replace("\\N", " ")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\\\", "\\")
        .strip()
    )


def parse_ical_datetime(key, value):
    """
    Parse DTSTART/DTEND values commonly emitted by SportsEngine.
    Supports UTC, TZID parameters, local date-time, and date-only values.
    """
    params = key.split(";")[1:]
    tzid = None
    value_is_date = False

    for param in params:
        if param.startswith("TZID="):
            tzid = param.split("=", 1)[1]
        if param == "VALUE=DATE":
            value_is_date = True

    value = value.strip()

    if value_is_date or re.fullmatch(r"\d{8}", value):
        day = datetime.strptime(value[:8], "%Y%m%d").date()
        return datetime.combine(day, datetime.min.time(), tzinfo=AZ)

    if value.endswith("Z"):
        parsed = datetime.strptime(value, "%Y%m%dT%H%M%SZ")
        return parsed.replace(tzinfo=ZoneInfo("UTC")).astimezone(AZ)

    parsed = datetime.strptime(value, "%Y%m%dT%H%M%S")

    if tzid:
        try:
            return parsed.replace(tzinfo=ZoneInfo(tzid)).astimezone(AZ)
        except Exception:
            pass

    return parsed.replace(tzinfo=AZ)


def parse_ical_events(text):
    """Return raw VEVENT dictionaries from an iCalendar payload."""
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
        base_key = key.split(";", 1)[0]

        if base_key in current:
            if not isinstance(current[base_key], list):
                current[base_key] = [current[base_key]]
            current[base_key].append((key, value))
        else:
            current[base_key] = (key, value)

    return events


def first_ical_value(event, field):
    item = event.get(field)
    if item is None:
        return None

    if isinstance(item, list):
        item = item[0]

    return item


def all_ical_values(event, field):
    item = event.get(field)
    if item is None:
        return []

    if isinstance(item, list):
        return item

    return [item]


def expand_ical_event(event, today, horizon_days=35):
    summary_item = first_ical_value(event, "SUMMARY")
    start_item = first_ical_value(event, "DTSTART")

    if not summary_item or not start_item:
        return []

    title = unescape_ical_text(summary_item[1])
    typ, age = classify(title)

    if not typ:
        return []

    start_dt = parse_ical_datetime(*start_item)

    end_item = first_ical_value(event, "DTEND")
    if end_item:
        end_dt = parse_ical_datetime(*end_item)
    else:
        end_dt = start_dt + timedelta(hours=1)

    duration = end_dt - start_dt
    if duration <= timedelta(0):
        duration = timedelta(hours=1)

    url_item = first_ical_value(event, "URL")
    description_item = first_ical_value(event, "DESCRIPTION")
    location_item = first_ical_value(event, "LOCATION")

    link = (
        unescape_ical_text(url_item[1])
        if url_item
        else "https://www.icedenscottsdale.com/page/show/2662960-calendar"
    )

    # SportsEngine sometimes includes the event URL only in DESCRIPTION.
    if description_item:
        description = unescape_ical_text(description_item[1])
        match = re.search(
            r"https?://(?:www\.)?icedenscottsdale\.com/event/show/\d+(?:\?[^\s]+)?",
            description,
            re.I,
        )
        if match:
            link = match.group(0)

    location = (
        unescape_ical_text(location_item[1])
        if location_item
        else "Ice Den Scottsdale"
    )

    # Reject events that are clearly not Scottsdale if the feed ever mixes facilities.
    location_low = location.lower()
    if "chandler" in location_low and "scottsdale" not in location_low:
        return []

    window_start = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )
    window_end = datetime.combine(
        today + timedelta(days=horizon_days),
        datetime.max.time(),
        tzinfo=AZ,
    )

    occurrences = []

    rrule_item = first_ical_value(event, "RRULE")

    if rrule_item:
        rule_text = rrule_item[1].strip()

        try:
            rule = rrulestr(rule_text, dtstart=start_dt)
            occurrences = list(rule.between(window_start, window_end, inc=True))
        except Exception as exc:
            print(
                "Ice Den Scottsdale RRULE parse failed:",
                title,
                rule_text,
                exc,
                file=sys.stderr,
            )
            occurrences = [start_dt] if window_start <= start_dt <= window_end else []
    else:
        if window_start <= start_dt <= window_end:
            occurrences = [start_dt]

    excluded = set()

    for ex_key, ex_value in all_ical_values(event, "EXDATE"):
        for raw in ex_value.split(","):
            try:
                excluded.add(parse_ical_datetime(ex_key, raw).isoformat())
            except Exception:
                continue

    output = []
    rink = "Ice Den Scottsdale"

    for occurrence in occurrences:
        if occurrence.tzinfo is None:
            occurrence = occurrence.replace(tzinfo=AZ)
        else:
            occurrence = occurrence.astimezone(AZ)

        if occurrence.isoformat() in excluded:
            continue

        occurrence_end = occurrence + duration

        output.append(
            {
                "id": stable_id(
                    "icedenscottsdale",
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
                "source": "icedenscottsdale",
            }
        )

    return output


def collect_ice_den_scottsdale(today):
    out = []
    feed_success = False

    for feed_url in ICE_DEN_SCOTTSDALE_ICAL_FEEDS:
        try:
            response = get(feed_url)
            text = response.text

            if "BEGIN:VCALENDAR" not in text:
                raise ValueError("response was not an iCalendar feed")

            feed_success = True

            for raw_event in parse_ical_events(text):
                out.extend(expand_ical_event(raw_event, today))

        except Exception as exc:
            print(
                "Ice Den Scottsdale iCal feed failed:",
                feed_url,
                exc,
                file=sys.stderr,
            )

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    result = sorted(dedup.values(), key=lambda e: e["start"])

    if feed_success:
        print(f"Ice Den Scottsdale iCal: {len(result)} hockey sessions")

    return result



# ---------------------------------------------------------------------------
# Ice Den Chandler — official SportsEngine iCal discovery + page fallback
# ---------------------------------------------------------------------------

ICE_DEN_CHANDLER_BASE = "https://www.icedenchandler.com"
ICE_DEN_CHANDLER_ICAL_FEEDS = (
    # Current official Ice Den Chandler calendar tag set published by SportsEngine.
    "https://www.icedenchandler.com/ical_feed?tags=9213634%2C9213662%2C9213663%2C9213664%2C9213665%2C9213666%2C9213667%2C9213672%2C9213674%2C9213675%2C9213676%2C9213677%2C9213678%2C9213679",
    # Legacy/alternate official tag set retained as a fallback.
    "https://www.icedenchandler.com/ical_feed?tags=5248139%2C5251279%2C5251281%2C5251282%2C5251284%2C5251286%2C5251288%2C5251289%2C5252225",
)

ICE_DEN_CHANDLER_MINDBODY_BASE = "https://clients.mindbodyonline.com/classic/ws"
ICE_DEN_CHANDLER_STUDIO_ID = "884177"


def diagnose_chandler_mindbody(today):
    """
    Diagnostic pass against Ice Den Chandler's current Mindbody booking pages.
    This intentionally DOES NOT publish Chandler events yet. It prints enough
    information in GitHub Actions to determine the stable server-rendered shape
    before we normalize it into the live calendar.
    """
    date_value = today.strftime("%m/%d/%Y")

    urls = [
        (
            "adult-hockey-week",
            f"{ICE_DEN_CHANDLER_MINDBODY_BASE}"
            f"?sLoc=1&sTG=28&sTrn=100000014&sView=week"
            f"&studioid={ICE_DEN_CHANDLER_STUDIO_ID}&stype=-103"
            f"&date={date_value}",
        ),
        (
            "all-classes-day-date",
            f"{ICE_DEN_CHANDLER_MINDBODY_BASE}"
            f"?sLoc=0&sView=day&studioid={ICE_DEN_CHANDLER_STUDIO_ID}"
            f"&stype=-102&date={date_value}",
        ),
        (
            "all-classes-day-sDate",
            f"{ICE_DEN_CHANDLER_MINDBODY_BASE}"
            f"?sLoc=0&sView=day&studioid={ICE_DEN_CHANDLER_STUDIO_ID}"
            f"&stype=-102&sDate={date_value}",
        ),
    ]

    hockey_terms = (
        "stick time",
        "open hockey",
        "adult skills",
        "hockey skills",
        "youth stick",
        "pond hockey",
    )

    for label, url in urls:
        try:
            response = requests.get(
                url,
                headers={
                    **HEADERS,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Referer": "https://www.icedenchandler.com/",
                    "Accept-Language": "en-US,en;q=0.9",
                },
                timeout=TIMEOUT,
                allow_redirects=True,
            )
            print(
                f"Chandler Mindbody diagnostic [{label}]: "
                f"status={response.status_code} bytes={len(response.content)} "
                f"final={response.url}"
            )

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            snippets = []

            for node in soup.find_all(["tr", "li", "div", "article", "section"]):
                block = " ".join(node.stripped_strings)
                low = block.lower()

                if any(term in low for term in hockey_terms):
                    cleaned = re.sub(r"\s+", " ", block).strip()
                    if cleaned and cleaned not in snippets:
                        snippets.append(cleaned)

                if len(snippets) >= 12:
                    break

            if snippets:
                print(
                    f"Chandler Mindbody hockey candidate blocks "
                    f"[{label}]: {len(snippets)}"
                )
                for snippet in snippets[:12]:
                    print("  MINDbody candidate:", snippet[:700])
            else:
                page_text = re.sub(
                    r"\s+",
                    " ",
                    " ".join(soup.stripped_strings),
                )
                print(
                    f"Chandler Mindbody hockey candidate blocks "
                    f"[{label}]: 0"
                )
                print("  Mindbody text sample:", page_text[:900])

        except Exception as exc:
            print(
                f"Chandler Mindbody diagnostic [{label}] failed:",
                exc,
                file=sys.stderr,
            )


ICE_DEN_CHANDLER_PAGES = (
    "https://www.icedenchandler.com/",
    "https://www.icedenchandler.com/node_list/node_list?model=event",
    "https://www.icedenchandler.com/page/show/2803608-calendar",
    "https://www.icedenchandler.com/adult-stick-time",
    "https://www.icedenchandler.com/adult-open-hockey",
    "https://www.icedenchandler.com/youth-programs",
    "https://www.icedenchandler.com/youth-skills-clinics",
    "https://www.icedenchandler.com/adult-hockey",
    "https://www.icedenchandler.com/hockey",
)


def chandler_feed_from_href(href):
    """
    Convert a SportsEngine iCal-instructions or direct-feed URL into the
    direct /ical_feed?tags=... URL.
    """
    if not href:
        return None

    href = href.replace("&amp;", "&")
    match = re.search(
        r"(?:event/ical_instructions|ical_feed)\?tags=([^\"'&<>\s]*)",
        href,
        re.I,
    )
    if not match:
        return None

    tags = match.group(1)
    if not tags:
        return None

    return f"{ICE_DEN_CHANDLER_BASE}/ical_feed?tags={tags}"


def discover_chandler_ical_feeds():
    feeds = set()

    for page_url in ICE_DEN_CHANDLER_PAGES:
        try:
            html = get(page_url).text
        except Exception as exc:
            print(
                "Ice Den Chandler discovery page failed:",
                page_url,
                exc,
                file=sys.stderr,
            )
            continue

        soup = BeautifulSoup(html, "html.parser")

        for anchor in soup.find_all("a", href=True):
            feed = chandler_feed_from_href(anchor.get("href"))
            if feed:
                feeds.add(feed)

        # Catch iCal links embedded in scripts/data attributes.
        for match in re.finditer(
            r"(?:event/ical_instructions|ical_feed)\?tags=[^\"'&<>\s]*",
            html,
            re.I,
        ):
            feed = chandler_feed_from_href(match.group(0))
            if feed:
                feeds.add(feed)

    print(f"Ice Den Chandler iCal feeds discovered: {len(feeds)}")
    return sorted(feeds)


def expand_chandler_ical_event(event, today, horizon_days=35):
    summary_item = first_ical_value(event, "SUMMARY")
    start_item = first_ical_value(event, "DTSTART")

    if not summary_item or not start_item:
        return []

    title = unescape_ical_text(summary_item[1])
    typ, age = classify(title)

    if not typ:
        return []

    start_dt = parse_ical_datetime(*start_item)

    end_item = first_ical_value(event, "DTEND")
    if end_item:
        end_dt = parse_ical_datetime(*end_item)
    else:
        end_dt = start_dt + timedelta(hours=1)

    duration = end_dt - start_dt
    if duration <= timedelta(0):
        duration = timedelta(hours=1)

    url_item = first_ical_value(event, "URL")
    description_item = first_ical_value(event, "DESCRIPTION")
    location_item = first_ical_value(event, "LOCATION")

    link = (
        unescape_ical_text(url_item[1])
        if url_item
        else "https://www.icedenchandler.com/page/show/2803608-calendar"
    )

    if description_item:
        description = unescape_ical_text(description_item[1])
        match = re.search(
            r"https?://(?:www\.)?icedenchandler\.com/event/show/\d+(?:\?[^\s]+)?",
            description,
            re.I,
        )
        if match:
            link = match.group(0)

    location = (
        unescape_ical_text(location_item[1])
        if location_item
        else "Ice Den Chandler"
    )

    location_low = location.lower()
    if "scottsdale" in location_low and "chandler" not in location_low:
        return []

    window_start = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )
    window_end = datetime.combine(
        today + timedelta(days=horizon_days),
        datetime.max.time(),
        tzinfo=AZ,
    )

    occurrences = []
    rrule_item = first_ical_value(event, "RRULE")

    if rrule_item:
        rule_text = rrule_item[1].strip()
        try:
            rule = rrulestr(rule_text, dtstart=start_dt)
            occurrences = list(rule.between(window_start, window_end, inc=True))
        except Exception as exc:
            print(
                "Ice Den Chandler RRULE parse failed:",
                title,
                rule_text,
                exc,
                file=sys.stderr,
            )
            occurrences = [start_dt] if window_start <= start_dt <= window_end else []
    else:
        if window_start <= start_dt <= window_end:
            occurrences = [start_dt]

    excluded = set()

    for ex_key, ex_value in all_ical_values(event, "EXDATE"):
        for raw in ex_value.split(","):
            try:
                excluded.add(parse_ical_datetime(ex_key, raw).isoformat())
            except Exception:
                continue

    output = []
    rink = "Ice Den Chandler"

    for occurrence in occurrences:
        if occurrence.tzinfo is None:
            occurrence = occurrence.replace(tzinfo=AZ)
        else:
            occurrence = occurrence.astimezone(AZ)

        if occurrence.isoformat() in excluded:
            continue

        occurrence_end = occurrence + duration

        output.append(
            {
                "id": stable_id(
                    "icedenchandler",
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
                "source": "icedenchandler",
            }
        )

    return output


def collect_chandler_event_pages(today):
    """
    Crawl Ice Den Chandler's official SportsEngine event index plus hockey
    program pages, then parse current event detail pages directly.
    """
    candidates = set()
    cutoff = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )
    horizon = datetime.combine(
        today + timedelta(days=35), datetime.max.time(), tzinfo=AZ
    )

    source_urls = list(ICE_DEN_CHANDLER_PAGES)

    for offset in (0, 31):
        day = today + timedelta(days=offset)
        source_urls.append(
            "https://www.icedenchandler.com/node_list/node_list"
            f"?model=event&mth={day.month}&yr={day.year}"
        )

    for page_url in source_urls:
        try:
            response = requests.get(
                page_url,
                headers={
                    **HEADERS,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Referer": "https://www.icedenchandler.com/",
                    "Accept-Language": "en-US,en;q=0.9",
                },
                timeout=TIMEOUT,
                allow_redirects=True,
            )
            response.raise_for_status()
            html = response.text
            print(
                f"Ice Den Chandler index source: "
                f"status={response.status_code} bytes={len(response.content)} "
                f"url={response.url}"
            )
        except Exception as exc:
            print(
                "Ice Den Chandler event-index failed:",
                page_url,
                exc,
                file=sys.stderr,
            )
            continue

        soup = BeautifulSoup(html, "html.parser")

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            if re.search(r"/event/show/\d+", href):
                candidates.add(urljoin(ICE_DEN_CHANDLER_BASE, href))

        for match in re.finditer(
            r'["\']([^"\']*/event/show/\d+[^"\']*)["\']',
            html,
        ):
            href = match.group(1).replace("\\/", "/")
            candidates.add(urljoin(ICE_DEN_CHANDLER_BASE, href))

    print(f"Ice Den Chandler event candidates: {len(candidates)}")

    out = []

    for event_url in sorted(candidates)[:220]:
        try:
            response = requests.get(
                event_url,
                headers={
                    **HEADERS,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Referer": "https://www.icedenchandler.com/",
                    "Accept-Language": "en-US,en;q=0.9",
                },
                timeout=TIMEOUT,
                allow_redirects=True,
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title_node = soup.find("h1") or soup.find("h2")
            if not title_node:
                continue

            title = " ".join(title_node.stripped_strings)
            typ, age = classify(title)
            if not typ:
                continue

            page_text = " ".join(soup.stripped_strings)

            match = re.search(
                r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s*-\s*"
                r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s+"
                r"([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4})",
                page_text,
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

            if start_dt < cutoff or start_dt > horizon:
                continue

            out.append(
                {
                    "id": stable_id(
                        "icedenchandler",
                        "Ice Den Chandler",
                        start_dt,
                        title,
                    ),
                    "title": title,
                    "type": typ,
                    "rink": "Ice Den Chandler",
                    "start": start_dt.isoformat(),
                    "end": end_dt.isoformat(),
                    "age": age,
                    "url": event_url,
                    "source": "icedenchandler",
                }
            )

        except Exception as exc:
            print(
                "Ice Den Chandler event page failed:",
                event_url,
                exc,
                file=sys.stderr,
            )

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    result = sorted(dedup.values(), key=lambda e: e["start"])
    print(f"Ice Den Chandler official event index: {len(result)} hockey sessions")
    return result


def collect_ice_den_chandler(today):
    out = []
    feed_success = False

    feed_urls = set(ICE_DEN_CHANDLER_ICAL_FEEDS)
    feed_urls.update(discover_chandler_ical_feeds())

    print(f"Ice Den Chandler iCal feeds to try: {len(feed_urls)}")

    for feed_url in sorted(feed_urls):
        try:
            response = get(feed_url)
            payload = response.text

            if "BEGIN:VCALENDAR" not in payload:
                raise ValueError("response was not an iCalendar feed")

            feed_success = True

            for raw_event in parse_ical_events(payload):
                out.extend(expand_chandler_ical_event(raw_event, today))

        except Exception as exc:
            print(
                "Ice Den Chandler iCal feed failed:",
                feed_url,
                exc,
                file=sys.stderr,
            )

    # Always merge the official-page fallback. This covers sessions whose
    # current SportsEngine tags are not included in the main calendar feed.
    out.extend(collect_chandler_event_pages(today))

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    result = sorted(dedup.values(), key=lambda e: e["start"])

    if feed_success:
        print(f"Ice Den Chandler iCal: {len(result)} hockey sessions")
    else:
        print(f"Ice Den Chandler collected: {len(result)} hockey sessions")

    return result


# ---------------------------------------------------------------------------
# SportsEngine HTML fallback — Mesa
# ---------------------------------------------------------------------------

SPORTSENGINE = [
    (
        "Coyotes Community Ice Center",
        "https://www.coyotescommunityicecenter.com",
        "https://www.coyotescommunityicecenter.com/page/show/5540662-calendar",
    ),
]


def collect_sportsengine(today):
    out = []
    event_link_re = re.compile(r"/event/show/\d+")
    cutoff = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )

    for rink, base, calendar in SPORTSENGINE:
        candidates = {}
        urls = [calendar]

        for offset in (0, 31):
            day = today + timedelta(days=offset)
            sep = "&" if "?" in calendar else "?"
            urls.append(f"{calendar}{sep}mth={day.month}&yr={day.year}")

        for url in urls:
            try:
                html = get(url).text
            except Exception as exc:
                print(
                    "SportsEngine index failed:",
                    rink,
                    url,
                    exc,
                    file=sys.stderr,
                )
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

                text = " ".join(soup.stripped_strings)

                match = re.search(
                    r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s*-\s*"
                    r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s+"
                    r"([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4})",
                    text,
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
                            "sportsengine",
                            rink,
                            start_dt,
                            title,
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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    today = datetime.now(AZ).date()

    collected = []
    collected += collect_mullett(today)
    collected += collect_ice_den_scottsdale(today)
    collected += collect_ice_den_chandler(today)
    collected += collect_sportsengine(today)
    collected.sort(key=lambda e: e["start"])

    # Fail-safe: if every network/layout source fails, preserve the prior file.
    if not collected:
        print(
            "No events collected. Preserving existing data/events.json.",
            file=sys.stderr,
        )
        return 0

    live_sources = sorted(
        set(
            e["rink"]
            for e in collected
            if e["source"] in ("mullett", "icedenscottsdale", "icedenchandler")
        )
    )
    auto_attempt = sorted(
        set(
            e["rink"]
            for e in collected
            if e["source"] == "sportsengine"
        )
    )

    payload = {
        "updated": datetime.now(AZ).isoformat(),
        "mode": "live-partial",
        "source_summary": {
            "live_auto": live_sources,
            "auto_attempt": auto_attempt,
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
