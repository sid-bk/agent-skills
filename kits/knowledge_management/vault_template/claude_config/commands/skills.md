# Skills / Slash-Commands

Live skills available in this vault. Type `/<name> [args]` to invoke. Most of the
table ships with the vault template and lives in `.claude/skills/` — vault-aware,
reading/writing the `*_obs/` folders and `memory/`. A couple are global utilities
that happen to be load-bearing here too, flagged as such.

---

## Vault skills

| Command | What it does | Writes to |
| --- | --- | --- |
| `/tracking <activity>` | Low-friction logger. Captures what you just did (optional time/duration) and escalates to memory only when it carries a settled fact. Capture, not a session. | `daily_obs/YYYY-MM-DD.md` (+ memory if a fact lands) |
| `/eod-summary` | Tight team-facing end-of-day update (3–6 lines for Slack/standup) from today's daily log, meetings, and decisions. A broadcast, not a log. Produces **two versions** — technical and non-technical. | output only; reads the day's notes |
| `/weekly-review` | Weekly roll-up: aggregates the week's daily logs/meetings/decisions, totals time by project from the timesheets, surfaces what moved/stalled/slipped and unowned action items, sets next week's priorities. Offers to run `inbox-sort` first. | dated note in `planning_obs/` (+ reconciles `memory/projects.md`) |
| `/timesheet <range>` | Hours summary over **any** date range (not just one ISO week). Reads the in-range daily notes, totals time by project, shows a per-day breakdown, flags untracked days. Reporting only — no priorities, no memory changes. | output only (offers a file in `planning_obs/` to export) |
| `/inbox-sort` | Triage and clear `inbox_obs/` — classify each capture, route it to the right folder, update memory, leave the inbox empty. | the routed folders + `memory/*.md` |
| `/timeline` | Dependency-aware project timeline — decompose into phases/tasks, estimate effort, compute working-day dates, critical path, and slack vs a deadline. | Markdown timeline (table + Mermaid Gantt + risks) in `planning_obs/` |
| `/storm-research <question>` *(global skill)* | Multi-source, fact-checked research harness — fan-out web searches, fetch, adversarially verify, synthesize a cited report. Ask 2–3 scoping questions first if underspecified. | cited report (output) |
| `/workshop <topic>` | Ruthless time-boxed crash course — asks how many hours you have, then makes you *functional* in the topic before the clock runs out. Tells you what to learn, what to completely ignore, and the one exercise that puts you ahead. | interactive (output); optional 1-line `/tracking` note at the end |
| `/commit-check` | Pre-push safety gate — scans staged, unstaged, and untracked changes for anything that must not hit the remote (secrets, credentials, env/key files, raw regulated data, client-confidential material, machine-local cruft, large binaries) and reports by severity. Read-only: never commits or pushes. | output only (offers `.gitignore`/unstage/rotation remediation on request) |

## How they chain

- `/tracking` feeds the daily timesheets → `/weekly-review` totals time from them.
- `/timesheet` reads the same daily timesheets as `/weekly-review` but over an arbitrary range, and reports only (no priorities/memory changes) — use it for ad-hoc spans, fortnights, months, or per-engagement hours.
- `/inbox-sort` clears captures before `/weekly-review` so the review doesn't miss uncaptured work (the review prompts for this).
- `/eod-summary` (daily broadcast) and `/weekly-review` (weekly roll-up) both read what `/tracking` logged.
- `/eod-summary` always ends by running `/commit-check` — EOD doubles as the vault's git checkpoint, so the safety scan runs before any end-of-day commit.

The dependency worth knowing: `/tracking` is the input to everything downstream. If the daily notes are empty, the roll-ups have nothing to read and will say so rather than invent work.

---

## Global utilities

Claude Code built-ins (`/code-review`, `/run`, `/verify`, `/simplify`, `/schedule`, `/loop`, …) and any personal skills in `~/.claude/skills/` are available here too. They aren't vault-specific and don't ship with the template — if you add one that the vault depends on, list it here so the dependency isn't invisible.

---

## Not skills — prompt templates

`new-session.md` and `update-memory.md` in this folder are *reusable prompts you paste*, not slash-commands. See those files.
