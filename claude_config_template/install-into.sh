#!/usr/bin/env bash
# Install the claude_config template into a target project.
# Usage: install-into.sh /path/to/project
# Safe: never overwrites an existing CLAUDE.md or claude_config/.
set -euo pipefail

TARGET="${1:?usage: install-into.sh <project-dir>}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[ -d "$TARGET" ] || { echo "error: $TARGET is not a directory" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"

# 1. claude_config/
if [ -e "$TARGET/claude_config" ]; then
  echo "skip: $TARGET/claude_config already exists"
else
  cp -R "$SRC/claude_config" "$TARGET/claude_config"
  echo "copied: claude_config/"
fi

# 2. root CLAUDE.md (don't clobber)
if [ -e "$TARGET/CLAUDE.md" ]; then
  cp "$SRC/CLAUDE.md" "$TARGET/CLAUDE.md.from-template"
  echo "exists: CLAUDE.md kept — template saved as CLAUDE.md.from-template (merge by hand)"
else
  cp "$SRC/CLAUDE.md" "$TARGET/CLAUDE.md"
  echo "copied: CLAUDE.md"
fi

# 3. docs/current_task.md (seed if missing)
mkdir -p "$TARGET/docs"
if [ ! -e "$TARGET/docs/current_task.md" ]; then
  cp "$SRC/docs/current_task.md" "$TARGET/docs/current_task.md"
  echo "copied: docs/current_task.md"
fi

echo
echo "Done. Open $TARGET in Claude Code and type:  load CLAUDE.md"
echo "(first load runs the bootstrap to fill placeholders + project context)"
