---
name: timesheet
description: Summarize tracked time over a custom date range — parse the range, read the daily notes in it, total hours by project, show a per-day breakdown, and flag untracked days. Invoked as `/timesheet <range>` (e.g. `/timesheet last 2 weeks`, `/timesheet 1 Jun to 11 Jun`, `/timesheet May`). Use when the user wants a timesheet, hours summary, time report, or "how much time did I spend on X" over an arbitrary window — anything not tied to a single ISO week (that's weekly-review).
---

# Timesheet

A reporting view over the daily timesheets: pick any window, get the hours. This
summarizes time from daily notes, totalled across whatever range the user asks for.

It is **reporting only** — it reads the daily notes and totals them. It does not set
priorities, reconcile memory, or write a review narrative. If the user wants a full
weekly roll-up with next-week priorities, that's `weekly-review`; if they want time
spent over an arbitrary span (a fortnight, a month, a client engagement, "since I
started the eval"), this is it.

This skill is designed for an Obsidian-style work vault. Expected structure:
`daily_obs/YYYY-MM-DD.md` with Time Log rows (`Hrs`, `Project`, `Activity`) and a
Totals by project block; `planning_obs/` for saved output files.

## When to use

The user runs `/timesheet <range>`, or asks for a timesheet / hours summary / time
report / time breakdown over a span that isn't a single ISO week.

## Procedure

1. **Resolve the range.** The text after `/timesheet` is in `args`; today's date is
   provided by the harness. Parse it into an explicit `start`–`end` (inclusive), then
   **state the resolved range** before reporting. Handle:
   - Explicit: `2026-06-01 to 2026-06-11`, `1 Jun – 11 Jun`, `01/06–11/06`.
   - Named: `this week`, `last week`, `this month`, `last month`, `May`, `Q2`,
     `last 2 weeks`, `last 10 days`.
   - Open-ended: `since 1 Jun` / `from 1 Jun` → start through today; `up to 9 Jun`
     → earliest note through that date.
   - Single day: report just that day.
   - **No args** → default to **current month-to-date** and say so.
   Ask only if the range is genuinely ambiguous. Convert all relative dates to
   absolute using today's date.

2. **Gather the daily notes in range.** Read every `daily_obs/YYYY-MM-DD.md` whose
   date falls within `[start, end]`. Skip `_placeholder.md`. From each, take the
   **Time Log** rows (`Hrs`, `Project`, `Activity`) and the **Totals by project** block.

3. **Total the hours.**
   - Sum `Hrs` per project across all in-range days. Prefer the per-row **Time Log**;
     if a day has only **Totals by project** filled (no rows), use those. If a day
     has neither, it's untracked.
   - Keep **`Admin / overhead`** and `—` (no-project) as their own buckets — don't
     fold them into projects.
   - Resolve `[[project]]` links to plain names for the table; group rows that point
     at the same project.

4. **Flag gaps honestly.** List every in-range day with **no daily note** or a note
   marked `_Untracked._` / empty Time Log as **untracked** — do not estimate or
   backfill hours for them. Report tracked-day count and the calendar span both, so
   coverage is visible.

5. **Render the summary** (see structure below): the resolved range, total hours,
   by-project totals, a compact per-day breakdown, and the untracked days. Add one
   short activity line per project from the Time-Log activities only if it adds signal
   — keep it terse; this is a timesheet, not a narrative.

6. **Output to chat by default.** Offer to save a copy to
   `planning_obs/YYYY-MM-DD — Timesheet (start–end).md` only if the user wants a
   file to export or share — don't write one unprompted.

## Output Structure

```markdown
# Timesheet — <Mon DD> to <Mon DD, YYYY>  (N tracked of M days)

## By project
| Project | Hrs |
|---|---|
| [[project]] | 0.0 |
| Admin / overhead | 0.0 |
| **Total** | **0.0** |

## By day
| Date | Hrs | Top project | Note |
|---|---|---|---|
| 2026-06-11 | 0.0 | [[project]] | one-line what moved |
| 2026-06-12 | — | — | untracked |

_Untracked days: 2026-06-12, …_
_Avg over tracked days: 0.0 h/day_
```

For a single-day range, drop the **By day** table and just show **By project** +
the day's activities.

## Rules

- **Don't invent hours.** Only sum what the Time Logs / Totals record. Missing or
  empty days are untracked, reported as such — never estimated.
- **Decimal hours**, summed cleanly (`0.25`, `0.5`, `1.5`); match the daily-log
  convention.
- **Keep buckets honest.** `Admin / overhead` and `—` stay visible as their own
  lines; don't reassign them to a project to make a project look bigger.
- **Reporting only.** No priority-setting, no `projects.md` reconciliation, no
  decision/status changes — if you spot drift worth acting on, mention it in one line
  but don't act. That's `weekly-review`'s and `tracking`'s job.
- **State the window.** Always echo the resolved start–end and the tracked-vs-total
  day count, so the numbers are interpretable.
