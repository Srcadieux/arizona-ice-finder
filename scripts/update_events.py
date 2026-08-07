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
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urljoin
import hashlib, json, re, sys

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dtparser

AZ = ZoneInfo("America/Phoenix")
HEADERS = {"User-Agent":"Mozilla/5.0 ArizonaIceFinder/1.0 (+GitHub Pages personal rink calendar)"}
TIMEOUT = 25
ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
EVENTS_FILE = ROOT/"data"/"events.json"

KEYWORDS = (
    "stick time","stick & puck","stick and puck","open hockey","pickup hockey","pick-up hockey",
    "flow hockey","power skate","hockey skills","hockey clinic","hockey camp"
)

def get(url, **kwargs):
    r=requests.get(url, headers=HEADERS, timeout=TIMEOUT, **kwargs)
    r.raise_for_status()
    return r

def classify(title):
    low=title.lower()
    if "flow hockey" in low: return "Flow Hockey","Adult"
    if "open hockey" in low or "pickup hockey" in low or "pick-up hockey" in low: return "Open Hockey","Adult"
    if "stick time" in low or "stick & puck" in low or "stick and puck" in low:
        return "Stick Time",("Adult" if "adult" in low else ("Youth" if any(x in low for x in ["youth","mite","squirt","peewee","bantam"]) else "All"))
    if any(x in low for x in ["power skate","hockey skills","hockey clinic","hockey camp"]):
        return "Clinic",("Youth" if "youth" in low else "All")
    return None,None

def iso_local(date_str, time_str):
    # Example date: Monday, August 10 2026; time: 5:10 pm
    dt=dtparser.parse(f"{date_str} {time_str}", fuzzy=True)
    return dt.replace(tzinfo=AZ)

def stable_id(source, rink, start, title):
    s=f"{source}|{rink}|{start.isoformat()}|{title}".encode()
    return source+"-"+hashlib.sha1(s).hexdigest()[:12]

def collect_mullett(today):
    base="https://mullett.sportified.net"
    rink="Mullett Arena / Mountain America Community Iceplex"
    events=[]
    # Four windows covers roughly the next month and reduces stale-page risk.
    starts=[today-timedelta(days=1), today+timedelta(days=6), today+timedelta(days=13), today+timedelta(days=20), today+timedelta(days=27)]
    seen=set()
    date_re=re.compile(r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+([A-Za-z]+)\s+(\d{1,2})\s+(\d{4})$")
    time_re=re.compile(r"^(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*(\d{1,2}:\d{2}\s*[ap]m)$",re.I)

    for start_date in starts:
        url=f"{base}/schedule?date={start_date.isoformat()}"
        try:
            soup=BeautifulSoup(get(url).text,"html.parser")
        except Exception as e:
            print("Mullett fetch failed:",url,e,file=sys.stderr); continue

        # Preferred: parse visible table rows while tracking the nearest date heading.
        current_date=None
        for node in soup.find_all(["h1","h2","h3","h4","h5","tr"]):
            text=" ".join(node.stripped_strings)
            md=date_re.match(text)
            if md:
                current_date=text; continue
            if node.name!="tr" or not current_date: continue
            cells=[" ".join(td.stripped_strings) for td in node.find_all(["td","th"])]
            if len(cells)<2: continue
            mt=time_re.match(cells[0])
            if not mt: continue
            title=cells[1].strip()
            typ,age=classify(title)
            if not typ: continue
            s=iso_local(current_date,mt.group(1)); e=iso_local(current_date,mt.group(2))
            if e<=s: e+=timedelta(days=1)
            if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
            link=url
            for a in node.find_all("a", href=True):
                href=a["href"]
                if "product" in href or "register" in a.get_text(" ",strip=True).lower():
                    link=urljoin(base,href); break
            key=(s.isoformat(),title)
            if key in seen: continue
            seen.add(key)
            events.append({"id":stable_id("mullett",rink,s,title),"title":title,"type":typ,"rink":rink,"start":s.isoformat(),"end":e.isoformat(),"age":age,"url":link,"source":"mullett"})

        # Fallback: flattened text parser for schedule pages whose table markup changes.
        if not any(e["url"].startswith(url) for e in events):
            lines=[x.strip() for x in soup.get_text("\n").splitlines() if x.strip()]
            current_date=None; i=0
            while i<len(lines):
                if date_re.match(lines[i]):
                    current_date=lines[i]; i+=1; continue
                mt=time_re.match(lines[i])
                if current_date and mt and i+1<len(lines):
                    title=lines[i+1]
                    typ,age=classify(title)
                    if typ:
                        s=iso_local(current_date,mt.group(1)); e=iso_local(current_date,mt.group(2))
                        if e<=s:e+=timedelta(days=1)
                 if s >= datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ):
                            key=(s.isoformat(),title)
                            if key not in seen:
                                seen.add(key)
                                events.append({"id":stable_id("mullett",rink,s,title),"title":title,"type":typ,"rink":rink,"start":s.isoformat(),"end":e.isoformat(),"age":age,"url":url,"source":"mullett"})
                    i+=2; continue
                i+=1
    return events

SPORTSENGINE = [
    ("Ice Den Scottsdale","https://www.icedenscottsdale.com","https://www.icedenscottsdale.com/node_list/node_list?model=event"),
    ("Ice Den Chandler","https://www.icedenchandler.com","https://www.icedenchandler.com/page/show/2803608-calendar"),
    ("Coyotes Community Ice Center","https://www.coyotescommunityicecenter.com","https://www.coyotescommunityicecenter.com/page/show/5540662-calendar"),
]

def collect_sportsengine(today):
    out=[]
    event_link_re=re.compile(r"/event/show/\d+")
    for rink,base,calendar in SPORTSENGINE:
        candidates={}
        # Try current and next month views plus the supplied index page.
        urls=[calendar]
        for offset in (0,31):
            d=today+timedelta(days=offset)
            sep="&" if "?" in calendar else "?"
            urls.append(f"{calendar}{sep}mth={d.month}&yr={d.year}")
        for u in urls:
            try:
                html=get(u).text
            except Exception as e:
                print("SportsEngine index failed:",rink,u,e,file=sys.stderr); continue
            soup=BeautifulSoup(html,"html.parser")
            for a in soup.find_all("a",href=True):
                href=a["href"]; label=" ".join(a.stripped_strings)
                if event_link_re.search(href) and any(k in label.lower() for k in KEYWORDS):
                    candidates[urljoin(base,href)]=label
            # Some calendars embed event URLs in scripts/JSON.
            for m in re.finditer(r'["\']([^"\']*/event/show/\d+[^"\']*)["\']',html):
                href=m.group(1).replace("\\/","/")
                candidates.setdefault(urljoin(base,href),"")
        for event_url,label in list(candidates.items())[:80]:
            try:
                soup=BeautifulSoup(get(event_url).text,"html.parser")
                title=(soup.find("h1") or soup.find("h2"))
                title=" ".join(title.stripped_strings) if title else label
                typ,age=classify(title)
                if not typ: continue
                text=" ".join(soup.stripped_strings)
                # SportsEngine event pages generally expose "1:30pm MST - 3:00pm MST July 7th, 2026"
                m=re.search(r'(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s*-\s*(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s+([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4})',text,re.I)
                if not m: continue
                date_clean=re.sub(r'(\d{1,2})(st|nd|rd|th)',r'\1',m.group(3),flags=re.I)
                s=dtparser.parse(f"{date_clean} {m.group(1)}").replace(tzinfo=AZ)
                e=dtparser.parse(f"{date_clean} {m.group(2)}").replace(tzinfo=AZ)
                if e<=s:e+=timedelta(days=1)
               if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
                out.append({"id":stable_id("sportsengine",rink,s,title),"title":title,"type":typ,"rink":rink,"start":s.isoformat(),"end":e.isoformat(),"age":age,"url":event_url,"source":"sportsengine"})
            except Exception as e:
                print("SportsEngine event failed:",rink,event_url,e,file=sys.stderr)
    # Dedupe
    dedup={}
    for e in out: dedup[(e["rink"],e["start"],e["title"])]=e
    return list(dedup.values())

def main():
    today=datetime.now(AZ).date()
    prior=json.loads(EVENTS_FILE.read_text()) if EVENTS_FILE.exists() else {"events":[]}
    collected=[]
    collected += collect_mullett(today)
    collected += collect_sportsengine(today)
    collected.sort(key=lambda e:e["start"])

    # Fail-safe: if a network/layout issue yields zero, keep the existing event file.
    if not collected:
        print("No events collected. Preserving existing data/events.json.",file=sys.stderr)
        return 0

    live_names=sorted(set(e["rink"] for e in collected if e["source"]=="mullett"))
    auto_names=sorted(set(e["rink"] for e in collected if e["source"]=="sportsengine"))
    payload={
        "updated":datetime.now(AZ).isoformat(),
        "mode":"live-partial",
        "source_summary":{
            "live_auto":live_names,
            "auto_attempt":auto_names,
            "official_link":["AZ Ice Arcadia","AZ Ice Gilbert","AZ Ice Peoria","Jay Lively Activity Center","Findlay Toyota Center","Tucson Convention Center / Tucson Arena"],
            "future":["Fire 'n' Ice Sports Arena","MQ Iceplex at Mosaic Quarter"]
        },
        "events":collected
    }
    EVENTS_FILE.write_text(json.dumps(payload,indent=2)+"\n")
    print(f"Wrote {len(collected)} collected events.")
    for name in sorted(set(e["rink"] for e in collected)):
        print(f" - {name}: {sum(1 for e in collected if e['rink']==name)}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
