#!/usr/bin/env bash
# Create (or reuse) an isolated venv with mutagen installed.
# Never installs into system/global Python (avoids PEP 668 "externally managed" breakage).
set -euo pipefail

VENV_DIR="${1:-$HOME/.cache/mp3-metadata-venv}"

if [ -x "$VENV_DIR/bin/python3" ] && "$VENV_DIR/bin/python3" -c "import mutagen" 2>/dev/null; then
  echo "$VENV_DIR/bin/python3"
  exit 0
fi

python3 -m venv "$VENV_DIR" >&2
"$VENV_DIR/bin/pip" install --quiet mutagen >&2

echo "$VENV_DIR/bin/python3"
