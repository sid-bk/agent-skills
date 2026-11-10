#!/usr/bin/env python3
"""Rename mp3 files to '<title tag>.mp3', leaving artist only in metadata.

Usage:
  python3 rename_to_title.py FILE.mp3 [FILE2.mp3 ...]        # dry run, prints plan
  python3 rename_to_title.py --apply FILE.mp3 [FILE2.mp3 ...]  # actually renames

Skips (and reports) any file with no title tag, or whose target name
collides with another file or an existing file on disk.
"""
import os
import sys

from mutagen.easyid3 import EasyID3

INVALID_CHARS = "/"  # ':' and '/' are the only chars macOS truly forbids; ':' maps to '/' on disk


def target_name(path: str) -> str | None:
    try:
        tags = EasyID3(path)
    except Exception:
        return None
    title = tags.get("title")
    if not title:
        return None
    clean = "".join(c for c in title[0] if c not in INVALID_CHARS).strip()
    if not clean:
        return None
    ext = os.path.splitext(path)[1]
    return f"{clean}{ext}"


def main() -> None:
    args = sys.argv[1:]
    apply = "--apply" in args
    files = [a for a in args if a != "--apply"]
    if not files:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    plan = {}
    seen_targets = {}
    for path in files:
        name = target_name(path)
        if name is None:
            print(f"SKIP (no title tag): {path}")
            continue
        new_path = os.path.join(os.path.dirname(path), name)
        if new_path == path:
            continue
        if name in seen_targets or (os.path.exists(new_path) and new_path != path):
            print(f"SKIP (name collision): {path} -> {name}")
            continue
        seen_targets[name] = path
        plan[path] = new_path

    for old, new in plan.items():
        print(f"{'RENAME' if apply else 'WOULD RENAME'}: {old} -> {new}")
        if apply:
            os.rename(old, new)


if __name__ == "__main__":
    main()
