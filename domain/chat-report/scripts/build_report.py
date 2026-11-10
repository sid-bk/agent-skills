#!/usr/bin/env python3
"""Wrap the written sections in the report shell and produce one HTML file.

    python3 build_report.py \
        --content content.html \
        --stats stats.json \
        --out "Book Club report.html" \
        --title "Somebody Call First" \
        --standfirst "Two years, two cities, and the one trip nobody booked."

The content file is a sequence of:

    <section data-tab="read" data-label="The Read" data-icon="🪞"> … </section>

Tabs are built from those, in the order they first appear. Everything else —
theme, charts, tooltips, print styling — comes from the shell.
"""

import argparse
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHELL = os.path.join(HERE, "..", "assets", "report-shell.html")

KNOWN_CHARTS = {"share", "timeline", "speed", "opens", "hours", "silences",
                "markers", "questions", "pairs", "runs",
                "sources", "sourceTimeline"}

SECTION_RE = re.compile(
    r'<section\b[^>]*\bdata-tab=["\'](?P<tab>[^"\']+)["\'][^>]*>', re.I)
LABEL_RE = re.compile(r'\bdata-label=["\'](?P<v>[^"\']*)["\']', re.I)
ICON_RE = re.compile(r'\bdata-icon=["\'](?P<v>[^"\']*)["\']', re.I)


def tabs_from(content):
    """Ordered [(slug, label, icon)] from the section tags in the content."""
    out, seen = [], set()
    for tag in re.findall(r"<section\b[^>]*>", content, re.I):
        m = SECTION_RE.match(tag)
        if not m:
            continue
        slug = m.group("tab")
        if slug in seen:
            continue
        seen.add(slug)
        lab = LABEL_RE.search(tag)
        ico = ICON_RE.search(tag)
        out.append((slug,
                    lab.group("v") if lab else slug.replace("-", " ").title(),
                    ico.group("v") if ico else ""))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--content", required=True)
    ap.add_argument("--stats", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--standfirst", default="")
    ap.add_argument("--eyebrow", default="")
    ap.add_argument("--brandline", default="")
    ap.add_argument("--updated", default="",
                    help="one line under the standfirst for a revised report, "
                         "e.g. 'Updated 2 Mar 2023 — now includes the group "
                         "chat, and I was wrong about the October silence.'")
    ap.add_argument("--shell", default=SHELL)
    a = ap.parse_args()

    for p in (a.content, a.stats, a.shell):
        if not os.path.exists(p):
            sys.exit(f"missing: {p}")

    content = open(a.content, encoding="utf8").read()
    shell = open(a.shell, encoding="utf8").read()
    stats = json.load(open(a.stats, encoding="utf8"))
    meta = stats.get("meta", {})

    tabs = tabs_from(content)
    if not tabs:
        sys.exit("no <section data-tab=\"…\"> found in the content file")

    bar = "".join(
        f'<button class="tab" role="tab" data-tab="{html.escape(slug)}" '
        f'aria-selected="false">{html.escape(icon)}{" " if icon else ""}'
        f'{html.escape(label)}</button>'
        for slug, label, icon in tabs)

    people = meta.get("people", [])
    srcs = meta.get("sources", [])
    first, last = meta.get("first", "")[:10], meta.get("last", "")[:10]
    eyebrow = a.eyebrow or (
        f"{meta.get('total', 0):,} messages · {first} to {last}"
        + (f" · {len(srcs)} conversations" if len(srcs) > 1 else ""))
    brandline = a.brandline or " · ".join(p.split()[0] for p in people[:4])

    used = set(re.findall(r'data-chart=["\']([^"\']+)["\']', content))
    for k in sorted(used - KNOWN_CHARTS):
        print(f"warning: unknown chart '{k}' — it will render empty. "
              f"Known: {', '.join(sorted(KNOWN_CHARTS))}", file=sys.stderr)

    out = shell
    for key, val in (("{{TABS}}", bar),
                     ("{{CONTENT}}", content),
                     ("{{DATA}}", json.dumps(stats, ensure_ascii=False)
                      .replace("</", "<\\/")),
                     ("{{TITLE}}", html.escape(a.title)),
                     ("{{STANDFIRST}}", a.standfirst),
                     ("{{EYEBROW}}", html.escape(eyebrow)),
                     ("{{UPDATED}}", a.updated),
                     ("{{BRANDLINE}}", html.escape(brandline))):
        out = out.replace(key, val)

    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        print(f"warning: unfilled placeholders {set(left)}", file=sys.stderr)

    with open(a.out, "w", encoding="utf8") as fh:
        fh.write(out)

    size = os.path.getsize(a.out) / 1024
    print(f"wrote {a.out}  ({size:.0f} KB, {len(tabs)} tabs, "
          f"{len(used)} charts, {len(people)} people"
          + (f", {len(srcs)} sources" if len(srcs) > 1 else "") + ")")
    print("open it with:  open " + json.dumps(a.out))


if __name__ == "__main__":
    main()
