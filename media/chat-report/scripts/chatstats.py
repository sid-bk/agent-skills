#!/usr/bin/env python3
"""Read a chat export and print the numbers a report needs.

Read-only. Never writes to the export.

    python3 chatstats.py CHAT.txt                     # the digest
    python3 chatstats.py CHAT.txt --json stats.json   # same, for the charts
    python3 chatstats.py CHAT.txt --grep "sorry" -C 2
    python3 chatstats.py CHAT.txt --day 2023-05-14
    python3 chatstats.py CHAT.txt --range 2023-05-10 2023-05-18
    python3 chatstats.py CHAT.txt --sample 40
    python3 chatstats.py CHAT.txt --person "Alex" --grep "\\?"

Several exports read as one story — the same friendship across two apps, a
group plus its side conversations, a chat exported twice a year apart:

    python3 chatstats.py A.txt B.txt --people          # who's in each file
    python3 chatstats.py A.txt B.txt --alias "Alex M=Alex" --json stats.json
    python3 chatstats.py A.txt B.txt --label "A.txt=The group" --source "The group"

Repeats are dropped, so overlapping exports don't double-count.

Handles WhatsApp (iOS/Android txt or zip), Telegram result.json,
Instagram/Facebook message_N.json, Discord CSV, and anything else via
--regex with named groups ts, who, msg.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta

GAP_HOURS = 6           # silence that counts as a new conversation
SILENCE_HOURS = 24      # silence worth listing

# Marker → what kind of thing was actually sent. Order matters: the first
# marker found wins, so put the specific ones before "<media omitted>".
#
# This split is load-bearing. A person who answers in voice notes looks silent
# and incurious if you only count typed words, and every "they never ask
# anything" verdict written off a flat media count is partly an artifact.
MEDIA_TYPES = {
    "audio omitted": "voice",
    "voice message omitted": "voice",
    ".opus": "voice",          # Android writes <attached: PTT-….opus>
    "image omitted": "image",
    "photo omitted": "image",
    "video omitted": "video",
    "sticker omitted": "sticker",
    "gif omitted": "gif",
    "document omitted": "document",
    "contact card omitted": "contact",
    "<attached:": "unknown",
    "<media omitted>": "unknown",
}
MEDIA_MARKERS = tuple(MEDIA_TYPES)
MEDIA_KINDS = ("voice", "image", "video", "sticker", "gif", "document",
               "contact", "unknown")

DELETED_MARKERS = (
    "this message was deleted", "you deleted this message", "message deleted",
)
# WhatsApp appends this to the final text of an edited message. The earlier
# versions are gone; only the last one survives the export.
EDITED_RE = re.compile(r"\s*<\s*this message was edited\s*>\s*", re.I)
# The placeholder the export leaves where a file used to be. Stripped before
# anything is counted; a caption sitting beside it is real text and survives.
OMITTED_RE = re.compile(
    r"<attached:[^>]*>|<media omitted>|"
    r"\b(?:image|video|audio|sticker|gif|document|photo|contact card|"
    r"voice message)\s+omitted\b", re.I)

MARKERS = {
    "sorry": r"\b(sorry|apolog|my bad|maaf)",
    "love you": r"\b(love you|luv u|ily|i love)",
    "miss you": r"\bmiss (you|u|ya)",
    "thanks": r"\b(thank|thanks|thx|ty)\b",
    "please": r"\bplease\b|\bpls\b|\bplz\b",
    "laughing": r"(haha|hehe|lol|lmao|😂|🤣|😭)",
    "always/never": r"\byou (always|never)\b",
    "it's fine": r"\b(it'?s fine|whatever|nvm|never ?mind)\b",
    "call me": r"\b(call me|can we talk|pick up|are we ok)\b",
    "money": r"(₹|\$|£|€)\s?\d|\b(paid|owe|transfer|split|rent|salary)\b",
}

STOP = set("""a about after all also am an and any are as at be because been before being but by can cant cause come could did didnt do does doesnt doing dont down even ever every for from get got had has have he her here hers him his how i if im in into is isnt it its ive just keep know like ll me more most much my no not now of off oh ok okay on once one only or other our out over own re s she should so some still such t than that thats the their them then there these they this those to too u up us ve very was wasnt way we well were what when where which while who why will with would ya yeah yes yet you your youre""".split())


class Msg:
    __slots__ = ("ts", "who", "text", "system", "source")

    def __init__(self, ts, who, text, system=False, source=""):
        self.ts, self.who, self.text, self.system = ts, who, text, system
        self.source = source

    @property
    def is_media(self):
        low = self.text.lower()
        return any(m in low for m in MEDIA_MARKERS)

    @property
    def media_type(self):
        """'voice' / 'image' / … , or None if this isn't a media placeholder."""
        low = self.text.lower()
        for marker, kind in MEDIA_TYPES.items():
            if marker in low:
                return kind
        return None

    @property
    def is_deleted(self):
        return any(m in self.text.lower() for m in DELETED_MARKERS)

    @property
    def is_edited(self):
        return bool(EDITED_RE.search(self.text))

    @property
    def body(self):
        """What the person actually typed.

        Strips the export's own furniture — the media placeholder and the
        "<This message was edited>" tag — so that "image omitted" doesn't get
        counted as two words of conversation.
        """
        t = OMITTED_RE.sub(" ", EDITED_RE.sub(" ", self.text))
        return " ".join(t.split())


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #

def clean(s):
    for ch in ("‎", "‏", "⁦", "⁩", "‪", "‬"):
        s = s.replace(ch, "")
    return s.replace(" ", " ").replace("\xa0", " ")


IOS_RE = re.compile(r"^\[(?P<ts>[^\]]{6,40})\]\s*(?P<rest>.*)$")
AND_RE = re.compile(
    r"^(?P<ts>\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?"
    r"(?:\s*[APap]\.?[Mm]\.?)?)\s+-\s+(?P<rest>.*)$")

DAYFIRST = [
    "%d/%m/%Y, %H:%M:%S", "%d/%m/%Y, %H:%M", "%d/%m/%y, %H:%M:%S",
    "%d/%m/%y, %H:%M", "%d/%m/%Y, %I:%M:%S %p", "%d/%m/%Y, %I:%M %p",
    "%d/%m/%y, %I:%M:%S %p", "%d/%m/%y, %I:%M %p",
    "%d.%m.%Y, %H:%M:%S", "%d.%m.%Y, %H:%M", "%d.%m.%y, %H:%M",
    "%d-%m-%Y, %H:%M", "%d-%m-%y, %H:%M",
]
MONTHFIRST = [f.replace("%d/%m", "%m/%d").replace("%d.%m", "%m.%d")
              .replace("%d-%m", "%m-%d") for f in DAYFIRST]


def parse_ts(raw, dayfirst):
    raw = clean(raw).strip()
    raw = re.sub(r"\s*([APap])\.?([Mm])\.?\s*$", r" \1\2", raw).strip().upper()
    if "," not in raw:
        raw = re.sub(r"(\d{2,4})\s+(\d{1,2}:)", r"\1, \2", raw, count=1)
    first = DAYFIRST if dayfirst else MONTHFIRST
    for f in first + (MONTHFIRST if dayfirst else DAYFIRST):
        try:
            return datetime.strptime(raw, f)
        except ValueError:
            continue
    return None


def detect_dayfirst(lines):
    """Day-first unless the file proves otherwise."""
    for ln in lines:
        m = IOS_RE.match(ln) or AND_RE.match(ln)
        if not m:
            continue
        nums = re.match(r"\s*(\d{1,2})[/.\-](\d{1,2})", m.group("ts"))
        if not nums:
            continue
        a, b = int(nums.group(1)), int(nums.group(2))
        if a > 12:
            return True
        if b > 12:
            return False
    return True


def load_whatsapp(text, custom_re=None):
    lines = clean(text).splitlines()
    dayfirst = detect_dayfirst(lines[:4000])
    msgs, cur = [], None
    for ln in lines:
        if custom_re:
            m = custom_re.match(ln)
            if m:
                ts = parse_ts(m.group("ts"), dayfirst)
                if ts:
                    if cur:
                        msgs.append(cur)
                    cur = Msg(ts, m.group("who").strip(), m.group("msg"))
                    continue
        m = IOS_RE.match(ln) or AND_RE.match(ln)
        if m:
            ts = parse_ts(m.group("ts"), dayfirst)
            if ts is not None:
                if cur:
                    msgs.append(cur)
                sm = re.match(r"^([^:]{1,60}?):\s(.*)$", m.group("rest"), re.S)
                if sm:
                    cur = Msg(ts, sm.group(1).strip(), sm.group(2))
                else:
                    cur = Msg(ts, None, m.group("rest"), system=True)
                continue
        if cur is not None:
            cur.text += "\n" + ln
    if cur:
        msgs.append(cur)
    return msgs


def load_telegram(obj):
    out = []
    buckets = obj.get("chats", {}).get("list") if "chats" in obj else [obj]
    for b in buckets:
        for m in b.get("messages", []):
            try:
                dt = datetime.fromisoformat(m.get("date", ""))
            except ValueError:
                continue
            t = m.get("text", "")
            if isinstance(t, list):
                t = "".join(x if isinstance(x, str) else x.get("text", "")
                            for x in t)
            out.append(Msg(dt.replace(tzinfo=None), m.get("from") or m.get("actor"),
                           t or "", system=m.get("type") == "service"))
    return out


def fix_meta(s):
    try:
        return s.encode("latin1").decode("utf8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def load_meta(obj):
    out = []
    for m in obj.get("messages", []):
        ts = m.get("timestamp_ms")
        if ts is None:
            continue
        body = m.get("content") or (
            "<media omitted>" if m.get("photos") or m.get("videos")
            or m.get("audio_files") else "")
        out.append(Msg(datetime.fromtimestamp(ts / 1000),
                       fix_meta(m.get("sender_name", "?")), fix_meta(body)))
    out.reverse()
    return out


def load_discord_csv(text):
    out = []
    for row in csv.DictReader(io.StringIO(text)):
        raw = (row.get("Date") or "").strip()
        for f in ("%d-%b-%y %I:%M %p", "%Y-%m-%dT%H:%M:%S.%f%z",
                  "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %I:%M %p"):
            try:
                dt = datetime.strptime(raw, f).replace(tzinfo=None)
                break
            except ValueError:
                dt = None
        if dt:
            out.append(Msg(dt, (row.get("Author") or "?").strip(),
                           row.get("Content") or ""))
    return out


def load(path, custom_re=None, meta=None):
    """Read one export. `meta`, if given, gets the detected format written into
    it — the provenance block needs to say what kind of file this was."""
    def tag(fmt, msgs):
        if meta is not None:
            meta["format"] = fmt
        return msgs

    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            name = next((n for n in z.namelist()
                         if n.endswith(".txt") and not n.startswith("__")), None)
            if not name:
                sys.exit("no .txt inside the zip")
            return tag("whatsapp",
                       load_whatsapp(z.read(name).decode("utf8", "replace"),
                                     custom_re))
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8-sig" if raw[:3] == b"\xef\xbb\xbf" else "utf8",
                      "replace")
    # A WhatsApp iOS export starts with "[" too, so only take the JSON path if
    # the file genuinely parses as JSON.
    obj = None
    if text.lstrip()[:1] in "{[":
        try:
            obj = json.loads(text)
        except ValueError:
            obj = None
    if obj is not None:
        if isinstance(obj, dict) and obj.get("messages") \
                and "timestamp_ms" in obj["messages"][0]:
            return tag("instagram/facebook", load_meta(obj))
        if isinstance(obj, dict) and ("chats" in obj or "messages" in obj):
            return tag("telegram", load_telegram(obj))
        if isinstance(obj, list):
            return tag("telegram", load_telegram({"messages": obj}))
    if path.lower().endswith(".csv"):
        return tag("discord", load_discord_csv(text))
    return tag("whatsapp", load_whatsapp(text, custom_re))


def load_many(paths, custom_re=None, aliases=None, labels=None):
    """Load several exports into one timeline.

    Each message keeps the name of the export it came from. Aliases fold the
    same human's different handles together — the same person is rarely
    written the same way in two exports. Exact repeats (same time, same
    sender, same words) are dropped, so re-exporting an overlapping window
    doesn't double-count.
    """
    aliases = {k.lower(): v for k, v in (aliases or {}).items()}
    labels = labels or {}
    out, seen, sources = [], set(), []
    for path in paths:
        name = labels.get(path) or os.path.splitext(os.path.basename(path))[0]
        fmt = {}
        msgs = [m for m in load(path, custom_re, fmt) if m.ts]
        kept, keys = 0, set()
        for m in msgs:
            if m.who:
                m.who = aliases.get(m.who.strip().lower(), m.who.strip())
            m.source = name
            key = (m.ts, m.who, m.text[:160])
            # Only a repeat of something an EARLIER export already had. Within
            # one file, identical lines in the same second are real — a photo
            # dump is twelve "image omitted" at 00:08.
            if key in seen:
                continue
            keys.add(key)
            out.append(m)
            kept += 1
        seen |= keys
        real = [m for m in msgs if not m.system and m.who]
        by_kind = Counter(m.media_type for m in real if m.is_media)
        sources.append({
            "name": name, "file": path, "messages": kept,
            "format": fmt.get("format", "unknown"),
            "duplicates_dropped": len(msgs) - kept,
            "first": real[0].ts.isoformat() if real else None,
            "last": real[-1].ts.isoformat() if real else None,
            "people": sorted({m.who for m in real}),
            "media": {k: by_kind[k] for k in MEDIA_KINDS if by_kind[k]},
            "media_total": sum(by_kind.values()),
            "deleted": sum(1 for m in real if m.is_deleted),
            "edited": sum(1 for m in real if m.is_edited),
            "system": sum(1 for m in msgs if m.system),
        })
    out.sort(key=lambda m: m.ts)
    return out, sources


def parse_pairs(items):
    """--alias 'Old Name=New Name' → {'Old Name': 'New Name'}"""
    out = {}
    for raw in items or []:
        if "=" not in raw:
            sys.exit(f"expected NAME=NAME, got: {raw}")
        k, v = raw.split("=", 1)
        out[k.strip()] = v.strip()
    return out


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def words(text):
    return re.findall(r"[a-zÀ-￿'-]{2,}",
                      unicodedata.normalize("NFKC", text.lower()))


def median(xs):
    if not xs:
        return None
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def human_delta(minutes):
    if minutes is None:
        return "—"
    if minutes < 1:
        return "under a minute"
    if minutes < 90:
        return f"{round(minutes)} min"
    if minutes < 60 * 48:
        return f"{minutes/60:.1f} hours"
    return f"{minutes/1440:.1f} days"


def snip(s, n=46):
    s = " ".join(s.split())
    return s[:n] + ("…" if len(s) > n else "")


# --------------------------------------------------------------------------- #
# the numbers
# --------------------------------------------------------------------------- #

def compute(msgs, sources=None):
    real = [m for m in msgs if not m.system and m.who]
    if not real:
        sys.exit("no messages parsed — check the format, or pass --regex")
    people = [p for p, _ in Counter(m.who for m in real).most_common()]
    total, first, last = len(real), real[0].ts, real[-1].ts
    span = max(1, (last - first).days)
    d = {"meta": {"total": total, "people": people, "days": span,
                  "first": first.isoformat(), "last": last.isoformat(),
                  "per_day": round(total / span, 1),
                  "system_notices": sum(1 for m in msgs if m.system),
                  "sources": sources or []}}

    if sources and len(sources) > 1:
        names = [s["name"] for s in sources]
        d["by_source"] = [
            {"source": n, "total": sum(1 for m in real if m.source == n),
             "by": {p: sum(1 for m in real if m.source == n and m.who == p)
                    for p in people}} for n in names]
        d["source_months"] = []
        per = defaultdict(Counter)
        for m in real:
            per[f"{m.ts:%Y-%m}"][m.source] += 1
        for k in sorted(per):
            d["source_months"].append(
                {"month": k, "total": sum(per[k].values()),
                 "by": {n: per[k][n] for n in names}})

    counts = Counter(m.who for m in real)
    wc, night, media, dele, ques, excl, edit, typed = (
        defaultdict(int) for _ in range(8))
    kinds = {p: Counter() for p in people}
    hours = {p: [0] * 24 for p in people}
    for m in real:
        body = m.body
        wc[m.who] += len(body.split())
        hours[m.who][m.ts.hour] += 1
        if m.ts.hour < 5:
            night[m.who] += 1
        if m.is_media:
            media[m.who] += 1
            kinds[m.who][m.media_type] += 1
        if m.is_deleted:
            dele[m.who] += 1
        if m.is_edited:
            edit[m.who] += 1
        # A message only counts as "typed" if something survives once the
        # export's own furniture is stripped. A photo with a caption counts;
        # a bare "image omitted" does not.
        if body and not m.is_deleted:
            typed[m.who] += 1
        if "?" in body:
            ques[m.who] += 1
        if "!" in body:
            excl[m.who] += 1

    # per_msg is words over TYPED messages, not over everything. The old
    # denominator made anyone who sends pictures look terse.
    d["share"] = [{"who": p, "count": counts[p],
                   "pct": round(counts[p] / total * 100, 1),
                   "words": wc[p],
                   "typed": typed[p],
                   "per_msg": round(wc[p] / max(1, typed[p]), 1),
                   "per_msg_all": round(wc[p] / max(1, counts[p]), 1)}
                  for p in people]
    d["habits"] = [{"who": p, "questions": ques[p], "media": media[p],
                    "deleted": dele[p], "edited": edit[p],
                    "exclaims": excl[p], "night": night[p]}
                   for p in people]
    d["media"] = [{"who": p, "total": media[p],
                   "by_type": {k: kinds[p][k] for k in MEDIA_KINDS if kinds[p][k]},
                   "voice": kinds[p]["voice"],
                   "media_pct": round(media[p] / max(1, counts[p]) * 100, 1),
                   "voice_pct": round(kinds[p]["voice"] / max(1, counts[p]) * 100, 1)}
                  for p in people]
    # Questions per 100 typed messages. Someone who answers in voice notes
    # scores low on the raw count for reasons that have nothing to do with
    # curiosity; this is the number a verdict should be written off.
    d["questions_adj"] = [{"who": p, "questions": ques[p], "typed": typed[p],
                           "per100": round(ques[p] / max(1, typed[p]) * 100, 1)}
                          for p in people]
    d["hours"] = hours

    starts, ends = Counter(), Counter()
    for i, m in enumerate(real):
        if i == 0 or (m.ts - real[i-1].ts) > timedelta(hours=GAP_HOURS):
            starts[m.who] += 1
            if i:
                ends[real[i-1].who] += 1
    ends[real[-1].who] += 1
    convs = max(1, sum(starts.values()))
    d["opens"] = [{"who": p, "opens": starts[p], "ends": ends[p],
                   "opens_pct": round(starts[p] / convs * 100, 1),
                   "ends_pct": round(ends[p] / convs * 100, 1)} for p in people]
    d["meta"]["conversations"] = convs

    lat = defaultdict(list)
    for i in range(1, len(real)):
        a, b = real[i-1], real[i]
        if a.who != b.who:
            mins = (b.ts - a.ts).total_seconds() / 60
            if 0 <= mins <= 60 * 48:
                lat[b.who].append(mins)
    d["speed"] = [{"who": p, "median_min": round(median(lat[p]) or 0, 1),
                   "label": human_delta(median(lat[p])),
                   "within5": round(sum(1 for x in lat[p] if x <= 5)
                                    / max(1, len(lat[p])) * 100, 1),
                   "over6h": round(sum(1 for x in lat[p] if x >= 360)
                                   / max(1, len(lat[p])) * 100, 1)}
                  for p in people]

    pair = Counter()
    for i in range(1, len(real)):
        a, b = real[i-1], real[i]
        if a.who != b.who and (b.ts - a.ts) <= timedelta(minutes=10):
            pair[(b.who, a.who)] += 1
    d["pairs"] = [{"from": b, "to": a, "n": n} for (b, a), n in pair.most_common(20)]

    runs = defaultdict(list)
    i = 0
    while i < len(real):
        j = i
        while j + 1 < len(real) and real[j+1].who == real[i].who:
            j += 1
        runs[real[i].who].append(j - i + 1)
        i = j + 1
    d["runs"] = [{"who": p, "runs3": sum(1 for x in runs[p] if x >= 3),
                  "longest": max(runs[p]) if runs[p] else 0} for p in people]

    gaps = []
    for i in range(1, len(real)):
        gap = real[i].ts - real[i-1].ts
        if gap >= timedelta(hours=SILENCE_HOURS):
            gaps.append((gap, real[i-1], real[i]))
    gaps.sort(key=lambda g: -g[0])
    d["silences"] = [{"days": round(g.total_seconds() / 86400, 1),
                      "from": f"{a.ts:%Y-%m-%d}", "to": f"{b.ts:%Y-%m-%d}",
                      "last_who": a.who, "last_text": snip(a.text),
                      "broke_who": b.who, "broke_text": snip(b.text)}
                     for g, a, b in gaps[:12]]

    per_month = defaultdict(Counter)
    for m in real:
        per_month[f"{m.ts:%Y-%m}"][m.who] += 1
    d["months"] = [{"month": k, "total": sum(per_month[k].values()),
                    "by": {p: per_month[k][p] for p in people}}
                   for k in sorted(per_month)]
    d["busiest"] = [{"day": day, "n": n} for day, n in
                    Counter(f"{m.ts:%Y-%m-%d}" for m in real).most_common(10)]

    wf = {p: Counter() for p in people}
    for m in real:
        if not m.is_deleted:
            wf[m.who].update(w for w in words(m.body) if w not in STOP)
    tot = {p: max(1, sum(wf[p].values())) for p in people}
    grand = Counter()
    for p in people:
        grand.update(wf[p])
    d["distinctive"] = {}
    for p in people:
        scored = []
        for w, n in wf[p].items():
            if n < 5:
                continue
            others = grand[w] - n
            othertot = max(1, sum(tot.values()) - tot[p])
            scored.append((((n / tot[p]) / ((others / othertot) + 1e-9)), n, w))
        scored.sort(reverse=True)
        d["distinctive"][p] = [{"word": w, "n": n} for _, n, w in scored[:14]]

    ph = Counter()
    for m in real:
        if m.is_deleted:
            continue
        ws = words(m.body)
        for n in (2, 3):
            for i in range(len(ws) - n + 1):
                g = ws[i:i+n]
                if not all(w in STOP for w in g):
                    ph[" ".join(g)] += 1
    d["phrases"] = [{"phrase": g, "n": n} for g, n in ph.most_common(40) if n >= 6]

    d["markers"] = {p: {k: sum(1 for m in real if m.who == p
                               and re.search(rx, m.body.lower()))
                        for k, rx in MARKERS.items()} for p in people}

    d["named"] = {}
    for p in people:
        fn = p.split()[0].lower()
        if len(fn) < 3:
            continue
        said = Counter()
        for m in real:
            if m.who != p and re.search(rf"\b{re.escape(fn)}\b", m.body.lower()):
                said[m.who] += 1
        if said:
            d["named"][p] = dict(said)

    d["bookends"] = {
        "first": [{"ts": f"{m.ts:%Y-%m-%d %H:%M}", "who": m.who,
                   "text": snip(m.text, 120)} for m in real[:3]],
        "last": [{"ts": f"{m.ts:%Y-%m-%d %H:%M}", "who": m.who,
                  "text": snip(m.text, 120)} for m in real[-5:]]}
    d["longest_messages"] = [
        {"ts": f"{m.ts:%Y-%m-%d}", "who": m.who, "words": len(m.body.split()),
         "text": snip(m.body, 80)}
        for m in sorted(real, key=lambda m: -len(m.body))[:5]]
    d["system"] = [{"ts": f"{m.ts:%Y-%m-%d}", "text": snip(m.text, 90)}
                   for m in msgs if m.system][:25]

    # What the export physically cannot contain. Stated as data so the report
    # can't quietly treat the edge of the file as the edge of the friendship.
    fmts = {s.get("format", "unknown") for s in (sources or [])} or {"whatsapp"}
    gone = ["reactions", "pins", "edit history (only the final text survives)",
            "the contents of deleted messages",
            "the contents of voice notes, calls and video calls",
            "anything said on another app, on the phone, or in person"]
    if "whatsapp" in fmts:
        gone.insert(0, "which message a reply was replying to")
    tot_media = sum(1 for m in real if m.is_media)
    d["provenance"] = {
        "formats": sorted(fmts),
        "messages": total,
        "media": tot_media,
        "media_pct": round(tot_media / max(1, total) * 100, 1),
        "media_by_type": {k: v for k, v in
                          Counter(m.media_type for m in real
                                  if m.is_media).items() if v},
        "voice": sum(1 for m in real if m.media_type == "voice"),
        "deleted": sum(1 for m in real if m.is_deleted),
        "edited": sum(1 for m in real if m.is_edited),
        "system": sum(1 for m in msgs if m.system),
        "cannot_show": gone,
    }
    return d


# --------------------------------------------------------------------------- #
# printing
# --------------------------------------------------------------------------- #

def bar(n, top, width=28):
    return "#" * max(1, round(width * n / top)) if n else ""


def head(t):
    print("\n" + t + "\n" + "-" * len(t))


def print_digest(d):
    m = d["meta"]
    print(f"{m['total']:,} messages  |  {m['first'][:10]} to {m['last'][:10]}  "
          f"|  {m['days']:,} days  |  {m['per_day']} a day")
    print(f"{len(m['people'])} " + ("people: " if len(m["people"]) > 1
                                    else "person: ") + ", ".join(m["people"]))
    if m["system_notices"]:
        print(f"({m['system_notices']} system notices — joins, leaves, renames)")

    if len(m.get("sources", [])) > 1:
        head("Where this came from")
        for s in m["sources"]:
            dup = (f"  ({s['duplicates_dropped']:,} repeats dropped)"
                   if s["duplicates_dropped"] else "")
            print(f"{s['name'][:26]:26} {s['messages']:>7,}  "
                  f"{(s['first'] or '?')[:10]} to {(s['last'] or '?')[:10]}"
                  f"{dup}")
            print(f"{'':26} {', '.join(s['people'])}")
            print(f"{'':26} {s.get('format', '?')} · "
                  f"{s.get('media_total', 0):,} media · "
                  f"{s.get('deleted', 0):,} deleted · "
                  f"{s.get('edited', 0):,} edited")
        for row in d.get("by_source", []):
            share = "  ".join(f"{p.split()[0][:10]} {n}"
                              for p, n in row["by"].items() if n)
            print(f"\n{row['source'][:26]:26} {row['total']:>7,}   {share}")

    head("Who talks")
    top = max(r["count"] for r in d["share"])
    for r in d["share"]:
        print(f"{r['who'][:22]:22} {r['count']:>7,}  {r['pct']:5.1f}%  "
              f"{r['words']:>8,} words  {r['per_msg']:4.1f}/typed msg  "
              f"{bar(r['count'], top)}")
    print("  (words exclude 'image omitted' and the edited tag; per-msg is over "
          "typed messages only)")

    head("Habits")
    for r in d["habits"]:
        print(f"{r['who'][:22]:22} {r['questions']:>6,} questions  "
              f"{r['media']:>6,} media  {r['deleted']:>4,} deleted  "
              f"{r['edited']:>4,} edited  "
              f"{r['exclaims']:>6,} '!'  {r['night']:>5,} after 1am")

    if any(r["total"] for r in d.get("media", [])):
        head("What they send instead of typing")
        kinds = [k for k in MEDIA_KINDS
                 if any(r["by_type"].get(k) for r in d["media"])]
        print(f"{'':22} {'media':>7} {'%msgs':>7}  " +
              "  ".join(f"{k[:8]:>8}" for k in kinds))
        for r in d["media"]:
            print(f"{r['who'][:22]:22} {r['total']:>7,} {r['media_pct']:>6.1f}%  " +
                  "  ".join(f"{r['by_type'].get(k, 0):>8,}" for k in kinds))
        head("Questions, adjusted for how they talk")
        for r in d["questions_adj"]:
            print(f"{r['who'][:22]:22} {r['questions']:>6,} questions over "
                  f"{r['typed']:>7,} typed messages   "
                  f"{r['per100']:>5.1f} per 100")
        print("  (raw question counts punish anyone who answers in voice notes)")

    pv = d.get("provenance")
    if pv:
        head("What this export can't show")
        mb = "  ".join(f"{k} {v:,}" for k, v in sorted(pv["media_by_type"].items(),
                                                       key=lambda x: -x[1]))
        print(f"{pv['media']:,} of {pv['messages']:,} messages "
              f"({pv['media_pct']}%) are media you cannot read")
        if mb:
            print(f"  {mb}")
        print(f"{pv['deleted']:,} deleted   {pv['edited']:,} edited "
              f"(only the final text survives)   {pv['system']:,} system notices")
        for line in pv["cannot_show"]:
            print(f"  · {line}")

    head(f"Who reaches first (after {GAP_HOURS}h+ of silence)")
    for r in d["opens"]:
        print(f"{r['who'][:22]:22} opens {r['opens']:>5,} ({r['opens_pct']:4.1f}%)"
              f"   ends {r['ends']:>5,} ({r['ends_pct']:4.1f}%)")

    head("How fast each person answers someone else")
    for r in d["speed"]:
        print(f"{r['who'][:22]:22} typical {r['label']:>13}   "
              f"{r['within5']:4.1f}% within 5 min   {r['over6h']:4.1f}% took 6h+")

    if d["pairs"] and len(d["meta"]["people"]) > 2:
        head("Who answers whom (within 10 minutes)")
        for r in d["pairs"][:14]:
            print(f"{r['from'][:18]:18} -> {r['to'][:18]:18} {r['n']:>6,}")

    head("Talking into the void (3+ in a row, no reply)")
    for r in d["runs"]:
        print(f"{r['who'][:22]:22} {r['runs3']:>6,} runs   "
              f"longest {r['longest']} in a row")

    head(f"Longest silences ({SILENCE_HOURS}h+)")
    for s in d["silences"]:
        print(f"{s['days']:6.1f} days  {s['from']} -> {s['to']}   "
              f"last: {s['last_who'][:14]:14} {s['last_text']!r}   "
              f"broke it: {s['broke_who'][:14]:14} {s['broke_text']!r}")
    if not d["silences"]:
        print("none — this chat never stopped for a full day")

    head("Month by month")
    peak = max(x["total"] for x in d["months"])
    for x in d["months"]:
        share = "  ".join(f"{p.split()[0][:8]} {n}"
                          for p, n in x["by"].items() if n)
        print(f"{x['month']}  {x['total']:>6,}  {bar(x['total'], peak, 24):24}  {share}")

    head("Busiest days (read these)")
    for x in d["busiest"]:
        print(f"{x['day']}  {x['n']:>5,} messages")

    head("Longest single messages")
    for x in d["longest_messages"]:
        print(f"{x['ts']}  {x['who'][:18]:18} {x['words']:>5} words  {x['text']!r}")

    head("Words each person uses that the others don't")
    for p, ws in d["distinctive"].items():
        print(f"{p[:22]:22} " + ", ".join(f"{w['word']} ({w['n']})" for w in ws))

    head("Phrases this chat repeats")
    for x in d["phrases"][:30]:
        print(f"{x['n']:>6,}  {x['phrase']}")

    if d["named"]:
        head("How often each person is named by the others")
        for p, said in d["named"].items():
            print(f"{p[:22]:22} " + "  ".join(f"{k.split()[0]}: {v}"
                                              for k, v in said.items()))

    head("Words that carry weight")
    print(f"{'':22}" + "".join(f"{k[:11]:>13}" for k in MARKERS))
    for p, row in d["markers"].items():
        print(f"{p[:22]:22}" + "".join(f"{row[k]:>13,}" for k in MARKERS))

    head("First and last")
    for x in d["bookends"]["first"]:
        print(f"  {x['ts']}  {x['who']}: {x['text']}")
    print("  ...")
    for x in d["bookends"]["last"]:
        print(f"  {x['ts']}  {x['who']}: {x['text']}")

    if d["system"]:
        head("System notices")
        for x in d["system"]:
            print(f"  {x['ts']}  {x['text']}")


# --------------------------------------------------------------------------- #
# reading modes
# --------------------------------------------------------------------------- #

def show(msgs, idxs, context=0):
    multi = len({m.source for m in msgs}) > 1
    seen = set()
    for i in sorted(idxs):
        for j in range(max(0, i - context), min(len(msgs), i + context + 1)):
            if j in seen:
                continue
            seen.add(j)
            m = msgs[j]
            tag = f"[{m.source}] " if multi else ""
            print(f"{'>' if j == i else ' '} {m.ts:%Y-%m-%d %H:%M}  {tag}"
                  f"{m.who or 'system'}: {m.text}")
        if context:
            print("-" * 60)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="+",
                    help="one export, or several to read as one story")
    ap.add_argument("--json", metavar="OUT", help="write the numbers as JSON")
    ap.add_argument("--alias", action="append", metavar="OLD=NEW",
                    help="fold one sender into another, e.g. "
                         "--alias '+447700900123=Sam'. Repeatable.")
    ap.add_argument("--label", action="append", metavar="PATH=NAME",
                    help="name a source in the report. Repeatable.")
    ap.add_argument("--people", action="store_true",
                    help="list the senders in each file and stop — use this "
                         "first when combining exports, to build the aliases")
    ap.add_argument("--grep", help="regex to find (case-insensitive)")
    ap.add_argument("-C", "--context", type=int, default=0)
    ap.add_argument("--day", help="YYYY-MM-DD")
    ap.add_argument("--range", nargs=2, metavar=("FROM", "TO"))
    ap.add_argument("--sample", type=int, help="N evenly spaced windows")
    ap.add_argument("--person", help="limit to one sender")
    ap.add_argument("--source", help="limit to one export, by its label")
    ap.add_argument("--regex", help="custom header regex with ts, who, msg")
    a = ap.parse_args()

    for p in a.path:
        if not os.path.exists(p):
            sys.exit(f"no such file: {p}")

    custom = re.compile(a.regex) if a.regex else None

    if a.people:
        for p in a.path:
            found = [m for m in load(p, custom) if m.ts and m.who and not m.system]
            print(f"\n{p}  ({len(found):,} messages)")
            for who, n in Counter(m.who for m in found).most_common():
                print(f"  {n:>7,}  {who}")
        print("\nSame person written two ways across these files? Fold them "
              "together with --alias 'As Written=Real Name'")
        return

    msgs, sources = load_many(a.path, custom, parse_pairs(a.alias),
                              parse_pairs(a.label))
    pool = [i for i, m in enumerate(msgs)
            if (not a.person or (m.who and a.person.lower() in m.who.lower()))
            and (not a.source or a.source.lower() in m.source.lower())]

    if a.grep:
        rx = re.compile(a.grep, re.I)
        hits = [i for i in pool if rx.search(msgs[i].text)]
        print(f"{len(hits):,} matches for {a.grep!r}\n")
        show(msgs, hits[:600], a.context)
        if len(hits) > 600:
            print(f"\n(showing first 600 of {len(hits):,})")
        return

    if a.day:
        d = datetime.strptime(a.day, "%Y-%m-%d").date()
        show(msgs, [i for i in pool if msgs[i].ts.date() == d])
        return

    if a.range:
        lo = datetime.strptime(a.range[0], "%Y-%m-%d").date()
        hi = datetime.strptime(a.range[1], "%Y-%m-%d").date()
        show(msgs, [i for i in pool if lo <= msgs[i].ts.date() <= hi])
        return

    if a.sample:
        step = max(1, len(pool) // a.sample)
        for k in range(0, len(pool), step):
            chunk = pool[k:k+12]
            print(f"\n===== {msgs[chunk[0]].ts:%d %b %Y} "
                  f"(message {chunk[0]:,}) =====")
            show(msgs, chunk)
        return

    d = compute(msgs, sources)
    if a.json:
        with open(a.json, "w") as fh:
            json.dump(d, fh, indent=1)
        print(f"numbers written to {a.json}\n")
    print_digest(d)


if __name__ == "__main__":
    main()
