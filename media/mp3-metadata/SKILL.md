---
name: mp3-metadata
description: Inspect, verify, clean up, and rename MP3 ID3 metadata (title/artist/album/year/genre). Use when the user wants to check mp3 tags, fix inaccurate or missing metadata, rename downloaded mp3s so the filename matches the song title (artist stays in tags only), or batch-correct tags on a folder of mp3s, e.g. files from a downloader like SPOTISAVER/youtube-dl. Not for other audio formats or for non-metadata audio editing.
---

# MP3 Metadata

Manage ID3 tags on mp3 files: read them, verify they're factually accurate, rename files to match the title tag, and write corrected/missing tags (title, artist, album, year, genre).

## Permission boundary

Installing anything (the venv/mutagen setup) and writing/renaming files are mutations. Only do them directly if the user has explicitly said to run it yourself for this task (e.g. "go ahead and run it"); otherwise hand them the exact commands to run and wait for output. Read-only steps (inspecting tags, `mdls`, web searches to verify facts) can always be run directly.

## Workflow

1. **Find the target files.** E.g. `find <dir> -maxdepth 1 -iname "*.mp3" -newermt "<date> 00:00:00"` for "today's downloads", or a glob the user gives.

2. **Read current tags.** Quickest on macOS without any install: `mdls -name kMDItemTitle -name kMDItemAuthors -name kMDItemAlbum -name kMDItemRecordingYear -name kMDItemMusicalGenre "<file>"` (read-only, reflects embedded ID3 tags via Spotlight). For a reliable, cross-platform read (or once mutagen is set up anyway), use `scripts/inspect_tags.py` instead — it reads the file directly rather than relying on Spotlight's index, which can be stale.

3. **Verify accuracy.** Don't assume existing tags or guessed values are correct. Cross-check title/artist/album/year against an authoritative source (web search: official streaming pages, Wikipedia, label sites). If confidence in any value is less than 100%, stop and ask the user rather than guess or silently "correct" it.

4. **Rename files to title-only.** The convention: filename = song title exactly as in the title tag; artist lives only in metadata, not the filename. Use `scripts/rename_to_title.py` (dry-run by default — only renames with `--apply`). It skips files with no title tag and skips any rename that would collide with another target name or an existing file.

5. **Set up tag-writing capability.** No system-wide install: run `scripts/setup_venv.sh [venv_dir]` (defaults to `~/.cache/mp3-metadata-venv`, reused across runs). It prints the path to a python3 with `mutagen` installed, installed in an isolated venv — never `pip install --break-system-packages` into system Python.

6. **Write corrected/missing tags.** Build a plan: a JSON file mapping absolute file path -> only the fields that need setting (`title`, `artist`, `album`, `date`, `genre`, `tracknumber`). Run `scripts/write_tags.py plan.json` with the venv's python. Genre should use broad categories (e.g. "Pop", "Hip-Hop", "EDM", "Hindi Pop", "Folk Fusion", "Rock") unless the user asks for finer-grained tags.

7. **Spot-check the result** with `mdls` or `inspect_tags.py` on a couple of files before reporting done.

## Scripts

- `scripts/setup_venv.sh [venv_dir]` — idempotent; prints `python3` path with mutagen installed.
- `scripts/inspect_tags.py FILE...` — prints title/artist/album/date/genre/tracknumber/duration as JSON.
- `scripts/write_tags.py plan.json` — applies a `{path: {field: value}}` plan via EasyID3, creating the ID3 tag if the file has none.
- `scripts/rename_to_title.py [--apply] FILE...` — renames each file to `"<title>.<ext>"`; without `--apply` it only prints the plan.
