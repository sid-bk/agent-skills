---
name: commit-check
description: Pre-commit safety scan — inspect staged, unstaged, and untracked changes for anything that must not be pushed (secrets, credentials, sensitive personal data, confidential material, machine-local cruft, large binaries). Invoked as `/commit-check`. Use before committing/pushing, whenever the user says "check before I commit", "is this safe to push", "scan my changes", or asks whether something should go in the repo. Reports findings by severity; never commits or pushes on its own.
---

# Commit Check

A gate, not a committer. The user runs `/commit-check` before pushing; you examine
everything that *would* go into a commit and flag anything that violates the repo's
git hygiene rules. You **read and report** — you never `git add`, `git commit`, or
`git push` as part of this skill. Remediation is offered, applied only on the user's
say-so.

## What's in scope

Everything not already in a clean committed state:
- **Staged** changes (`git diff --cached`)
- **Unstaged** changes to tracked files (`git diff`)
- **Untracked** files (`git ls-files --others --exclude-standard`) — these are the
  highest-risk; they're new and unreviewed.

Scan file **contents** (the diff/hunks) and file **paths/names**, not just filenames.

## Procedure

1. **Gather the surface.** Determine the repo root and collect the three sets above.
   If the tree is clean (nothing staged/unstaged/untracked), say so and stop.

2. **Scan for each risk category.** Run over the changed/added content:

   | Category | What to look for |
   |---|---|
   | **Secrets / credentials** | `sk-…`, `ghp_…`/`github_pat_…`, `AKIA[0-9A-Z]{16}`, `-----BEGIN … PRIVATE KEY-----`, `Bearer [A-Za-z0-9._-]{20,}`, `xox[baprs]-…` (Slack), `password`/`passwd`/`secret`/`api[_-]?key`/`token` followed by `=`/`:` and a value, connection strings (`postgres://user:pass@`, `mongodb+srv://…`) |
   | **Env / key files** | any path matching `*.env*`, `*.pem`, `*.key`, `id_rsa*`, `*credential*`, `*secret*`. **Do not open `.env` files** — flag by name alone |
   | **Sensitive personal / health data** | real personal identifiers, medical record numbers, DOB + name pairs, raw call transcripts or records with personal details. De-identified summaries are fine; raw personal data is not |
   | **Client / vendor confidential** | signed contracts, NDA-bound pricing, credentials or artifacts a stakeholder shared in confidence |
   | **Machine-local / cruft** | `.DS_Store`, `._*`, `.claude/settings.local.json`, `.obsidian/workspace*.json`, `.trash/` — if staged, a `.gitignore` rule is missing |
   | **Large binaries** | any added file over ~1 MB (esp. media/PDF); flag for a link-or-storage decision |

   Concrete first pass (adapt paths as needed), then read the flagged hunks with
   judgment:
   ```bash
   git diff --cached; git diff                      # content that would/could commit
   git ls-files --others --exclude-standard          # untracked, unreviewed
   git diff --cached --name-only; git diff --name-only
   # content pattern sweep over tracked changes + untracked files:
   git grep -nIE '(sk-[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{20}|github_pat_[A-Za-z0-9_]{20}|AKIA[0-9A-Z]{16}|-----BEGIN|Bearer [A-Za-z0-9._-]{20}|xox[baprs]-|(password|secret|api[_-]?key|token)\s*[:=])' -- . || true
   # oversize additions:
   git ls-files --others --exclude-standard -z | xargs -0 -I{} du -h "{}" | awk '$1 ~ /M|G/'
   ```
   The regex catches mechanical cases; sensitive personal data and client-confidential
   material need you to actually read the changed content and reason, not just
   pattern-match.

3. **Rank and report.** Group findings by severity:
   - 🔴 **Block** — secrets, credentials, key/env files, raw personal/health data.
     Do **not** push until resolved.
   - 🟡 **Review** — possible confidential material, personal contact details,
     gray-area items; user judgment call.
   - ⚪ **Cleanup** — machine-local cruft or large binaries that should be gitignored
     or moved; not secret but shouldn't be in history.

   For each: file path, line/hunk, category, one-line why. Cite `file:line`. If
   nothing fires, say **"Clean — nothing flagged in staged/unstaged/untracked changes"**
   and note what was scanned.

4. **Offer remediation — apply only on request.** Depending on category, propose the
   fix but wait for a go-ahead:
   - Cruft / env-style file staged → add a `.gitignore` rule + `git rm --cached <file>`.
   - Secret in a to-be-committed change → unstage, remove the value, and (if it's a
     live secret) **advise rotation**.
   - **Secret already in a prior commit** → flag loudly: deletion won't remove it from
     history; it needs a history rewrite (`git filter-repo` / BFG) **and** rotation.
     Surface this; don't attempt the rewrite unprompted.
   - Large binary → suggest a link or external storage placement.

## Rules

- **Never auto-commit or auto-push.** This skill only inspects and advises. The user
  drives the actual commit.
- **Never open `.env`/`*.env*` files** — flag them by filename only.
- **Untracked files are guilty until cleared** — they're new and unreviewed; scan them
  first.
- **Private repo is not a free pass** — history is permanent; a leaked secret is
  compromised the moment it's pushed, private or not. When in doubt, block and ask.
- **Read for sensitive content, don't just grep** — the mechanical patterns miss the
  judgment cases, which are the ones that matter most.
