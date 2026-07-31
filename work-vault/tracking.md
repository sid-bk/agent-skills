---
name: tracking
description: Quick-log an activity into today's record and update memory as needed. Invoked as `/tracking <activity details>` — capture what the user just did (with optional time/duration), append it to today's daily log, and propagate anything memory-worthy (project status, decision, new person, blocker, tool verdict) to the right files. Use whenever the user runs /tracking, or says "log that", "track this", "note that I just…".
---

# Tracking

A low-friction logger. The user types `/tracking <activity details>` and you record
it without a back-and-forth. Default action is **append to today's daily log**;
escalate to memory only when the activity contains a settled fact. Be fast — this is
capture, not a session.

The activity text is whatever follows `/tracking` (in `args`). Today's date is
provided by the harness.

This skill is designed for an Obsidian-style work vault. Expected structure:
`daily_obs/YYYY-MM-DD.md` for daily notes and `memory/` for state files.

## Procedure

1. **Parse the activity.** From the text, pull:
   - **What** happened (the activity / outcome).
   - **Project** — infer and `[[link]]` it against `memory/projects.md`; if none
     fits, leave unlinked (don't force one).
   - **Time/duration** — only if stated: `1.5h`, `90m`, `9:00–10:30`. Never invent
     times.
   - **Signal** — does it also imply a decision, status change, blocker, new person,
     or tool verdict?

2. **Log it to the daily note** (`daily_obs/YYYY-MM-DD.md`):
   - Create the note from the daily log template if today's doesn't exist yet.
   - If a duration/time was given → add a **Time Log** row and update **Totals by
     project**.
   - Always add a one-line **Progress** bullet (outcome-focused), with the
     `[[project]]` link.
   - If it's a blocker → add to **Blockers / Open** as `- [ ] …`.

3. **Update memory only when warranted** — apply the `inbox-sort` routing,
   lightweight:
   | Signal in the activity | Update |
   |---|---|
   | Project status changed (started/blocked/done) | `memory/projects.md` + the project note |
   | A decision was made | `memory/decisions.md` + a `decisions_obs/DNNN` record |
   | A new person appeared | `memory/people.md` (+ `people_obs/` if recurring) |
   | A tool reached a verdict | `memory/tools.md` |
   Apply obvious, low-risk updates directly. For something bigger or ambiguous (a
   real decision, a new project, a status flip), make the update **and state it
   plainly** so the user can correct — or ask one tight question if you genuinely
   can't tell.

4. **Confirm in one line.** Report what was logged and any memory file touched, e.g.:
   `Logged to 2026-06-10 daily (1.5h → [[Project Name]]). Updated projects.md: status → Active.`
   Nothing more unless something needs the user's decision.

## Rules

- **Speed over ceremony.** One capture, one confirmation. Don't open a dialogue for
  a routine log.
- **Don't invent.** No fabricated times, projects, or detail not in the input.
  Missing time → Progress bullet only.
- **Outcomes, not transcripts.** Record what moved, tersely.
- **Escalate, don't bury.** If the activity hides a decision or blocker, surface it
  into the right file — that's the "memory updated as needed" part — but say you did.
