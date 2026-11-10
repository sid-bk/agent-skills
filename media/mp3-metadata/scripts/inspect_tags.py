#!/usr/bin/env python3
"""Print ID3 tags for one or more mp3 files as JSON.

Usage: python3 inspect_tags.py FILE.mp3 [FILE2.mp3 ...]
"""
import json
import sys

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

FIELDS = ["title", "artist", "album", "date", "genre", "tracknumber"]


def read_one(path: str) -> dict:
    out = {"file": path}
    try:
        tags = EasyID3(path)
    except Exception:
        tags = {}
    for field in FIELDS:
        values = tags.get(field) if tags else None
        out[field] = values[0] if values else None
    try:
        out["duration_seconds"] = round(MP3(path).info.length, 1)
    except Exception:
        out["duration_seconds"] = None
    return out


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: inspect_tags.py FILE.mp3 [FILE2.mp3 ...]", file=sys.stderr)
        sys.exit(1)
    results = [read_one(p) for p in sys.argv[1:]]
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
