#!/usr/bin/env bash
# Install the work-vault template into a target directory.
# Usage: install-into.sh /path/to/new-vault
# Safe: never overwrites an existing file. Anything that already exists is skipped
# and reported, so re-running it fills gaps rather than clobbering work.
set -euo pipefail

TARGET="${1:?usage: install-into.sh <vault-dir>}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$TARGET"
TARGET="$(cd "$TARGET" && pwd)"

[ "$TARGET" = "$SRC" ] && { echo "error: refusing to install the template into itself" >&2; exit 1; }

copy() { # copy <relative-src> <relative-dest>
  local src="$SRC/$1" dest="$TARGET/$2"
  if [ -e "$dest" ]; then
    echo "  skip    $2 (already exists)"
  else
    mkdir -p "$(dirname "$dest")"
    cp -R "$src" "$dest"
    echo "  copied  $2"
  fi
}

echo "Installing work-vault template → $TARGET"

# 1. Vault context + config
copy CLAUDE.md      CLAUDE.md
copy claude_config  claude_config
copy template_md    template_md

# 2. Skills land at .claude/skills/ — they are stored un-dotted in the template so
#    Claude Code doesn't register them as live skills of whatever repo holds it.
copy skills .claude/skills

# 3. Obsidian config (core plugins + neutral defaults; no community plugins)
copy .obsidian .obsidian

# 4. Git hygiene: ignore rules + the mechanical pre-push backstop
copy .gitignore .gitignore
copy .githooks  .githooks

# 5. Vault folder scaffolding
for d in projects_obs meetings_obs decisions_obs people_obs research_obs \
         planning_obs daily_obs inbox_obs references_obs attachments_obs archive_obs; do
  if [ -d "$TARGET/$d" ]; then
    echo "  skip    $d/ (already exists)"
  else
    mkdir -p "$TARGET/$d"; touch "$TARGET/$d/.gitkeep"
    echo "  created $d/"
  fi
done

# 6. Seed reference notes
copy "references_obs/Daily Log & Timesheet.md" "references_obs/Daily Log & Timesheet.md"

# 7. Activate the pre-push hook if this is a git repo (local config; never travels with a clone)
if git -C "$TARGET" rev-parse --git-dir >/dev/null 2>&1; then
  git -C "$TARGET" config core.hooksPath .githooks
  echo "  wired   core.hooksPath → .githooks"
else
  echo "  note    not a git repo — skipped the pre-push hook."
  echo "          After 'git init', run: git config core.hooksPath .githooks"
fi

cat <<EOF

Done.

Next:
  1. Open $TARGET in Claude Code and say:  load CLAUDE.md and run the Setup section
     It will interview you to fill the <<placeholders>> — identity, how you work,
     and the regulated-data category for the git-hygiene rules.
  2. Open the same folder in Obsidian:  Open folder as vault
EOF
