---
tags: [reference, system]
---
# Daily Log & Timesheet

The reference for tracking activity, time, and progress day to day. Copy the **template** below into `daily_obs/YYYY-MM-DD.md` each day (or have the assistant create it). It doubles as a timesheet: the **Time Log** records hours by project, the **Totals** roll them up, and the `weekly-review` skill aggregates these across the week.

Keep it lightweight — a log you'll actually maintain beats a perfect one you abandon. Fill the Time Log as you go or reconstruct it at end of day.

---

## How to use it

- **One note per day**, named `YYYY-MM-DD`, in `daily_obs/`.
- **Intent** is set in the morning (1–3 things). **Progress** and the **Time Log** are filled through/after the day.
- **Time Log** rows are the timesheet. Use `HH:MM–HH:MM`, decimal hours (`1.5`, not `1:30`), and link the project with `[[...]]` so totals reconcile against `projects_obs/`.
- **Totals by project** is the day's billable/effort summary — what you'd copy into an external timesheet.
- Action items use `- [ ] (owner) … — due …`; carry unfinished ones into Tomorrow and into the next day's note.
- At week's end, run `weekly-review` — it reads these notes, sums time by project, and surfaces what slipped.

---

## Template

For a light day (few time-tracked activities, no coding session), use the
plain template:

```markdown
---
date: YYYY-MM-DD
tags: [daily]
---
# YYYY-MM-DD

## Intent
The 1–3 things that would make today a win.
- ...

## Time Log
| Time | Hrs | Project | Activity | Notes |
|---|---|---|---|---|
| 09:00–10:30 | 1.5 | [[project]] | what you did | optional |
| 10:30–11:00 | 0.5 | — | email / admin | |

## Totals by project
| Project | Hrs |
|---|---|
| [[project]] | 0.0 |
| Admin / overhead | 0.0 |
| **Total** | **0.0** |

## Progress
What actually moved — done, advanced, learned.
- ...

## Blockers / Open
- [ ] (owner) ... — due ...

## Tomorrow
Carry-forward and next steps.
- ...
```

### Engineering-session template (default for coding days)

For a day spent writing/fixing code in a project, skip Intent/Time Log/Totals
and use this shape instead — one entry per bug/task, terse, reference-style.
Make this the default if most of your days are coding days; if they aren't,
delete this variant and keep the plain template above.

```markdown
# YYYY-MM-DD

## Focus
One line — project + what today is about.

## Done

### [Non-bug work, e.g. a root-cause investigation or refactor]
2-4 sentences max: what broke, what the fix was, who/what merged it. No
retrospective narrative — state the mechanism, not the journey.

[Bug NNNN](ticket-url): Ticket title
**Branch:** `bug/AB#NNNN-slug`
**File(s):** `path/to/file.ts`
One or two sentences: the mechanical fix (what changed, where it guards/lives).
Commit hash + message if committed; PR number + merged/open status.

## Config / process updates
Only if something about *how* you work changed today (new convention, new
skill, new CLAUDE.md rule) — not code changes, those go in Done.
- ...

## Open
- One line per open item, `~~strikethrough~~` items that closed today.

## EOD

*EOD — YYYY-MM-DD*
Done:
• One bullet per bug/task, terse.

Blockers / need:
• One bullet per blocker.

Next: one line.
```

---

## Conventions

- **Decimal hours**, so they sum cleanly (`0.25`, `0.5`, `1.5`). Only applies
  to the plain template's Time Log.
- **`Admin / overhead`** is a valid non-project bucket — meetings without a
  home, email, context-switching. Track it; don't hide it. (Plain template.)
- A row with no clear project gets `—`; if it recurs, that's a signal
  something needs a project. (Plain template.)
- Don't backfill fiction. If a block is unaccounted for, leave it out and note
  "untracked" rather than inventing activity — the weekly review flags gaps
  honestly.
- **Terse over narrative, always.** Each bug/task entry is a handful of
  sentences stating the mechanism (what changed, where, what it does) — not a
  retrospective walking through false starts, reasoning, or back-and-forth.
  If something needs more detail than that, it belongs in `decisions_obs/` or
  a project note, linked from here, not inlined.
