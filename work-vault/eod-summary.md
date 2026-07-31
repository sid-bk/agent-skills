---
name: eod-summary
description: Generate a concise end-of-day summary of the day's work, formatted to share with the team (Slack / standup channel). Pulls from today's daily log, meetings, decisions, and project/action-item changes, then writes a tight team-facing update. Use when the user wants an EOD update, end-of-day summary, standup post, daily wrap-up, or "what do I tell the team."
---

# EOD Summary

Produce a short, team-facing end-of-day update from what's in the work log for today.
The output is a broadcast — 3–6 lines someone skims in Slack — not a log. Bias hard
toward brevity; detail lives in the linked notes.

This skill is designed for an Obsidian-style work vault. Expected folders:
`daily_obs/`, `meetings_obs/`, `decisions_obs/`, and `memory/` for project state.

## When to use

The user asks for an EOD / end-of-day update, standup post, daily wrap-up, or
something to send the team.

## Procedure

1. **Set the day.** Default to today; confirm only if ambiguous.
2. **Gather today's inputs:**
   - `daily_obs/YYYY-MM-DD.md` — Progress, Blockers, Tomorrow (the main source)
   - `meetings_obs/` notes dated today — decisions + action items
   - `decisions_obs/` + `memory/decisions.md` entries dated today
   - `memory/projects.md` — any status change touched today
3. **If the daily note is missing or thin,** say so and ask the user for 2–3
   highlights rather than inventing activity.
4. **Synthesize** into the format below. Lead with the most important outcome.
5. **Output in chat** as a copy-pasteable block. Offer to append it to today's
   daily note under an `## EOD` section.
6. **Run `/commit-check`** (always, as the last step). EOD is the natural checkpoint
   for committing the day's vault changes, so before any push, scan staged/unstaged/
   untracked changes for anything that must not hit the remote. Report its result
   inline after the summary. If it flags nothing, note "commit-check: clean." If it
   flags something, surface it and do **not** proceed to commit until the user resolves
   it. This step never commits or pushes on its own.

## Output format

```
*EOD — YYYY-MM-DD*
Done:
• <outcome, not activity — what moved>
• <…>
Decisions: <only if any — one line each, link/name them>
Blockers / need: <what's blocking or where you need input — omit if none>
Next: <tomorrow's focus, 1–2 items>
```

Keep it to ~3–6 "Done" bullets. Drop any empty section rather than writing "none".

## Rules

- **Team audience.** Frame for colleagues: outcomes and status, not a personal diary.
- **Strip private/personal detail.** Health, mood, and the like don't go in a team
  update — frame an absence neutrally ("out part of the morning"), not with the reason.
- **Outcomes over activity.** "FAQ approach decided: leaning RAG, eval in progress"
  beats "read about X all day."
- **Surface blockers and asks explicitly** — that's the part teammates act on. If
  you're waiting on someone, name what and from whom.
- **Don't dump the timesheet.** Hours/time-log detail stay in the daily note unless
  the user asks to include them.
- **Don't invent work.** Only summarize what's in the notes; if the day is thin, ask.
- **Concise over complete.** When in doubt, cut it and let the linked note carry the
  detail.
- **Always finish with `/commit-check`.** The EOD run is also the vault's end-of-day
  git checkpoint; the safety scan runs every time, even if the summary itself is thin.
