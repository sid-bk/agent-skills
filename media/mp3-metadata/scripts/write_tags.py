#!/usr/bin/env python3
"""Batch-write ID3 tags from a JSON plan.

Usage: python3 write_tags.py plan.json

plan.json shape: a dict keyed by absolute file path, each value a dict of
EasyID3 fields to set (only include fields that need changing):
{
  "/path/to/Song.mp3": {"title": "Song", "artist": "Artist", "album": "Album",
                          "date": "2024", "genre": "Pop"}
}

Valid EasyID3 keys: title, artist, album, date, genre, tracknumber,
albumartist, composer, discnumber.
"""
import json
import sys

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError


def write_one(path: str, fields: dict) -> None:
    try:
        tags = EasyID3(path)
    except ID3NoHeaderError:
        tags = EasyID3()
        tags.save(path)
        tags = EasyID3(path)
    for key, value in fields.items():
        tags[key] = str(value)
    tags.save()
    print(f"{path} -> {fields}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: write_tags.py plan.json", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        plan = json.load(fh)
    for path, fields in plan.items():
        write_one(path, fields)


if __name__ == "__main__":
    main()
