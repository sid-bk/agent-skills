# Work-vault template

A portable, employer-agnostic copy of a work vault's setup: the Claude context system (`CLAUDE.md` + `claude_config/`), the note templates (`template_md/`), the vault skills, the Obsidian config, the git-hygiene layer, and the `*_obs/` folder scaffolding — with every project, person, decision, and client detail stripped out.

Use it to stand up a work vault (new job, side engagement, a separate client) without re-deriving the structure. This is the sanitized export; see `../README.md` for how this repo's sanitized/operational split works in general.

---

## Install

```bash
vault_template/install-into.sh ~/path/to/new-vault
```

Copies everything into the target, creates the folder scaffolding, and wires the pre-push hook if the target is a git repo. It **never overwrites an existing file** — anything already there is skipped and reported, so re-running it fills gaps instead of clobbering work.

Then, in the new vault:

```
load CLAUDE.md and run the Setup section
```

The Setup section at the bottom of the copied `CLAUDE.md` is the bootstrap. It interviews you to fill the `<<placeholders>>`, then deletes itself.

---

## What's inside

```
vault_template/
├── CLAUDE.md                  # vault context — placeholdered, ends with a Setup section
├── install-into.sh            # the installer
├── claude_config/
│   ├── README.md              # how the context system works
│   ├── sessions/              # 5 session modes: project, meeting, decision, research, planning
│   ├── memory/                # 6 memory files — empty scaffolds, formats intact
│   └── commands/              # skills catalog + paste-able session/memory prompts
├── template_md/                # 12 note templates — one per note type + an index README
├── skills/                     # 7 vault skills → installed to .claude/skills/
├── .obsidian/                 # core plugins + neutral defaults
├── .githooks/pre-push         # mechanical secret/blob backstop
├── .gitignore                 # secrets, macOS cruft, volatile Obsidian state
├── references_obs/            # seeded with the Daily Log & Timesheet note
└── *_obs/                     # empty folder scaffolding (.gitkeep)
```

**Skills ship as `skills/`, not `.claude/skills/`, on purpose.** Claude Code discovers nested `.claude/` directories and registers what it finds as live skills — a dotted directory here would inject seven duplicate skills into this repo's own skill list. The installer places them at `.claude/skills/` in the target vault, where they belong. (This mirrors why they aren't just pointed at `~/.claude/skills/` the way `feature-team`/`draft-commit` are: vault skills are path-bound to the `*_obs/` folder conventions, not machine-global.)

**In the live vault this template lives dot-prefixed (`.vault_template/`)** so Obsidian ignores it as a folder in the vault's own graph/search/quick-switcher while it stays tracked in git. Here — a plain folder in a sanitized-export repo, not nested inside an active Obsidian vault — the dot prefix serves no purpose, so it's dropped.

---

## What was stripped

Everything in `claude_config/memory/` is an empty scaffold: the format blocks and the verdict/status vocabularies are kept (they're the reusable part), the actual projects, people, decisions, and tool verdicts are gone. `template_md/` was already generic (field structures, no real data) and needed no changes. The domain-specific parts of `CLAUDE.md` — identity, working style, the regulated-data category, and the repo origin — are `<<placeholders>>`.

The `<<placeholders>>` are deliberately not neutral defaults. A vague "how I work" section silently mis-tunes every session that reads it, so the template forces the answer rather than guessing.

---

## Keeping it current

The template is a **snapshot**, not a symlink — improving a session file or skill in a live vault does not propagate here. Sanitize on export; never sync the other direction (same rule as the rest of this repo — see `../README.md`). When a live vault's structure changes (a new session mode, a skill, a convention), port it across deliberately by diffing the two:

```bash
diff -ru vault_template/claude_config/sessions   /path/to/live-vault/claude_config/sessions
diff -ru vault_template/template_md              /path/to/live-vault/template_md
diff -ru vault_template/skills                   /path/to/live-vault/.claude/skills
```

Those directories are meant to stay near-identical (modulo real skill implementations vs. this repo's own duplicate copies under `../*/`); `claude_config/memory/` and `CLAUDE.md` are meant to diverge, so don't diff those expecting a match.
