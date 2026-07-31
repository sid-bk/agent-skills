---
name: weekly-review
description: Run a weekly review across the work vault — aggregate the week's daily logs, meetings, and decisions; total time by project from the daily timesheets; surface what got done, what's blocked, what slipped, and unowned/overdue action items; then write a dated review note in planning_obs/ with next week's priorities. Use when the user wants a weekly review, retro, status roll-up, end-of-week summary, or to close out the week.
---

# Weekly Review

Roll up the week across the whole vault into one honest picture — what moved, what
stalled, where time went — and set next week's priorities. The output is a dated
review note in `planning_obs/` plus reconciled project statuses in memory.

This skill is designed for an Obsidian-style work vault. Expected structure:
`daily_obs/`, `meetings_obs/`, `decisions_obs/`, `planning_obs/`, `inbox_obs/`,
and `memory/` for state files.

## When to use

The user asks for a weekly review / retro / status roll-up / end-of-week summary, or
it's the weekly maintenance pass.

## Procedure

1. **Set the window.** Default to the current ISO week (Monday → today) or the last
   completed week if it's the weekend/Monday. State the exact date range you're using;
   ask only if genuinely ambiguous.

2. **Triage the inbox first.** If `inbox_obs/` has anything but `_placeholder.md`,
   say so and offer to run `inbox-sort` before reviewing — otherwise the review misses
   uncaptured work. Don't force it; proceed if the user declines.

3. **Gather inputs in range.** Read:
   - `daily_obs/` notes dated in the window — Intent, Progress, Time Logs, Blockers
   - `meetings_obs/` notes in the window
   - `decisions_obs/` records dated in the window
   - `memory/projects.md` — current status + open items
   - `memory/tools.md` — verdicts reached this week

4. **Total time by project.** Sum the `Hrs` from each daily's Time Log, grouped by
   project (and the `Admin / overhead` bucket). Note any days in the window with
   **no daily note** — report them as untracked, don't guess hours.

5. **Synthesize the week.** Write a short narrative: what shipped or advanced,
   decisions made, notable meetings and people, and where time actually went vs. where
   intent said it would.

6. **Surface what needs attention.** Explicitly list:
   - Action items still open — especially **unowned** or **overdue**
   - Anything `#blocked` — and what it's waiting on
   - Projects **untouched all week** (stale — possible drift or a status that should
     change)
   - Decisions still **Proposed**, not Accepted

7. **Set next week.** Propose 3–5 priorities from open items and blockers; carry
   forward unfinished action items with their owners intact. Confirm these with the
   user rather than deciding unilaterally.

8. **Write the review note** to `planning_obs/` named
   `YYYY-Www — Weekly Review.md` (ISO week, e.g. `2026-W24 — Weekly Review.md`),
   using the structure below.

9. **Reconcile memory.** Apply any status changes to `projects.md` (confirm each
   first), bump its `Last updated`, and update `memory/vault-map.md` if content grew
   materially.

10. **Report.** Summarise the week in chat and end with the attention list — the
    things the user must act on.

## Review Note Structure

```markdown
---
tags: [review]
week: YYYY-Www
---
# YYYY-Www — Weekly Review (Mon DD – Sun DD)

## Summary
2–4 sentences: the shape of the week.

## Shipped / Moved
- [[project]] — what advanced

## Decisions
- [[DNNN — Title]] — one line

## Meetings & People
- [[YYYY-MM-DD — Meeting]] — outcome

## Time by Project
| Project | Hrs |
|---|---|
| [[project]] | 0.0 |
| Admin / overhead | 0.0 |
| **Total** | **0.0** |
_Untracked days: ..._

## Attention
- **Blocked:** ...
- **Unowned / overdue actions:** ...
- **Stale projects:** ...
- **Open decisions:** ...

## Next Week
- Priorities: ...
- Carry-forward: - [ ] (owner) ... — due ...
```

## Rules

- **Don't invent activity.** Report only what the logs, meetings, and decisions show;
  flag missing daily notes as untracked rather than estimating.
- **Confirm before changing project statuses** or committing next week's priorities
  — propose, don't impose.
- **Carry-forward actions keep their owner.** Never drop an owner when moving an item
  to next week.
- **Honest over flattering.** A week where little moved should read that way — the
  value is in surfacing drift, not manufacturing progress.
