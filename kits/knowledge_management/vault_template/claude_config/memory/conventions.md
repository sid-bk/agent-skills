# Vault Conventions

How this work vault is structured and how notes are maintained.

---

## Folders

| Folder | Holds | Rule |
|---|---|---|
| `projects_obs/` | one file (or folder) per active project / initiative | Keep status current; archive when done |
| `meetings_obs/` | dated meeting notes + action items | One note per meeting, `YYYY-MM-DD Title` |
| `decisions_obs/` | decision records (ADR-style) | One per decision, `DNNN — Title`; never edit a superseded one — add a new record |
| `people_obs/` | stakeholders, teammates, clients, vendors | One note per recurring person |
| `research_obs/` | tool / tech evaluations and comparisons | One per tool or comparison |
| `planning_obs/` | roadmaps, priorities, goals, weekly reviews | Weekly reviews named `YYYY-Www — Weekly Review` |
| `daily_obs/` | daily logs + timesheets | One per day, `YYYY-MM-DD`; follow [[Daily Log & Timesheet]] |
| `inbox_obs/` | raw capture only | Triage regularly; nothing stays here permanently |
| `references_obs/` | runbooks, how-tos, reference docs | Linked from projects and meetings |
| `attachments_obs/` | files, images, PDFs | Never scatter across other folders |
| `archive_obs/` | completed / inactive work | Read-only; reference it, don't edit |

---

## Capture → Triage Workflow

```
New thought / note / artifact
        ↓
   inbox_obs/
        ↓
   What is it?
   ├── Action     → the relevant project (with an owner) or daily_obs/
   ├── Decision   → decisions_obs/ + memory/decisions.md
   ├── Person     → people_obs/ + memory/people.md
   ├── Tool eval  → research_obs/ + memory/tools.md
   ├── Reference  → references_obs/
   └── Noise      → discard
```

---

## Naming

- **Meetings & dailies:** `YYYY-MM-DD ...`
- **Decisions:** `DNNN — Title` (sequential, e.g. `D007 — Pick queue backend`)
- **Projects:** short descriptive name
- **Evaluations:** `[Tool] — evaluation`

---

## Tags (YAML frontmatter)

| Tag | Use for |
|---|---|
| `#project` | Project notes |
| `#meeting` | Meeting notes |
| `#decision` | Decision records |
| `#research` / `#tool` | Tool / tech evaluation |
| `#person` | People notes |
| `#blocked` | Anything waiting on someone/something |
| `#action` | An owned action item |
| `#reference` | Runbooks, how-tos |
| `#archive` | Inactive / historical |

---

## Linking

- Meeting notes link to the project(s) they affect
- Decisions link to the project and the people involved
- Project notes link to their open decisions and recent meetings
- Every action item has an owner — unowned work is a dropped thread

---

## Maintenance

| Frequency | Task |
|---|---|
| Daily | Keep a daily log + timesheet ([[Daily Log & Timesheet]]); capture meetings same day; dump loose notes to `inbox_obs/`; share an EOD update (`eod-summary` skill) |
| Weekly | Triage the inbox (`inbox-sort` skill); run the `weekly-review` skill; update project status; review open action items and their owners |
| Monthly | Archive done projects; prune stale items; resolve or re-own anything `#blocked` |
