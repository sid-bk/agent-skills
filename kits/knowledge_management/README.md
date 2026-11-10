# Knowledge management

A **work vault** — an Obsidian vault paired with a file-based Claude context system — used as the system of record for work that doesn't live in a code repo or a ticketing tool: projects and their state, meeting notes and action items, decisions and their rationale, the people involved, and research into tools and approaches.

The pairing is the point. Files are ground truth for both the human (Obsidian: search, backlinks, graph) and the assistant (Claude: loads the relevant files at the start of a session and holds the full state of the work in context — a colleague who's read everything, not a search engine).

This is the sanitized write-up + installable template. See `../../README.md` for how this repo's sanitized/operational split works generally.

---

## The model

**Folders split by artifact type**, one `*_obs/` per kind of thing:

| Folder | Holds |
|---|---|
| `projects_obs/` | One note (or folder) per active project / initiative |
| `meetings_obs/` | Dated meeting notes + action items |
| `decisions_obs/` | Decision records, ADR-style (`DNNN — Title`) |
| `people_obs/` | Stakeholders, teammates, clients, vendors |
| `research_obs/` | Tool / tech evaluations and comparisons |
| `planning_obs/` | Roadmaps, priorities, goals |
| `daily_obs/` | Daily / standup logs (`YYYY-MM-DD`) |
| `inbox_obs/` | Raw capture — triaged regularly, nothing stays |
| `references_obs/` | Runbooks, how-tos, reference docs |
| `attachments_obs/` | Files, images, PDFs |
| `archive_obs/` | Completed / inactive work (read-only) |

**A Claude config layer sits on top** (`CLAUDE.md` + `claude_config/`) — no plugins, no agents, just markdown the assistant loads:

| Layer | Role |
|---|---|
| `CLAUDE.md` | Identity, working style, vault structure, launch behaviour. Always loaded. |
| `claude_config/sessions/` | One mode per session — `project`, `meeting`, `decision`, `research`, `planning`. Load exactly one; don't mix modes in a session. |
| `claude_config/memory/` | Stable, settled state — projects, decisions, people, tool verdicts, conventions, a vault map. The assistant's long-term memory across sessions. |
| `claude_config/commands/` | Reusable prompts for starting a session and persisting context at the end of one. |
| `template_md/` | One note template per type (daily, meeting, decision, project, research, planning, person, bug-fix, issues, user-stories) — copy into the right `*_obs/` folder and fill in. |

**A `/skills` layer automates the recurring loops** — capture, roll-up, triage, safety. Vault-specific ones (`tracking`, `eod-summary`, `weekly-review`, `timesheet`, `inbox-sort`, `commit-check`) are sanitized individually under `../../work-vault/` (`commit-check` under `../../dev-workflow/`); this template bundles installable copies of them at `vault_template/skills/` so a new vault is self-contained without depending on this repo staying cloned nearby. `workshop` and `storm-research` are general-purpose skills (`../../learning/workshop.md`, `../../learning/storm-research.md`) that happen to be useful here too — the vault's `CLAUDE.md` flags them as global rather than vault-bundled. `timeline` (dependency-aware project timelines / Gantt) is documented as a live workflow in `claude_config/commands/skills.md` but isn't packaged as a standalone skill file here.

---

## Principles

- **Context over conversation.** Invest in the files, not re-explaining every session.
- **Files are ground truth.** If it isn't in a file, the assistant doesn't know it next session.
- **Memory is settled state.** In-progress thinking lives in project notes; only stable, won't-be-revisited facts go in `memory/`.
- **Every action item has an owner.** Unowned work is a dropped thread.
- **One session mode at a time.** Don't mix project work and tool research in the same load.
- **A decision, once made, doesn't get silently re-litigated.** Superseding a decision means a new record that links back, not an edit.

---

## Using the template

```bash
vault_template/install-into.sh ~/path/to/new-vault
```

Then open it in Claude Code and say `load CLAUDE.md and run the Setup section` — it interviews you to fill the identity/working-style `<<placeholders>>`, then deletes the setup instructions. Open the same folder in Obsidian (`Open folder as vault`) and you're running.

Full detail — what's inside, what was stripped, how to keep it in sync with a live vault — in `vault_template/README.md`.
