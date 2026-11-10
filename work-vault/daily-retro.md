---
name: daily-retro
description: Backfill a missing daily_obs/YYYY-MM-DD.md note from git commit history, using only what a commit's real diff proves — no invented Focus, Open, or narrative content. Invoke directly ("backfill yesterday's note", "reconstruct the log for 2026-08-22") or let /eod-summary call it automatically when it finds no daily note for the day it's summarizing.
---

# Daily Retro

Reconstruct a daily note that was never written, from git history alone.
This is a narrow, honest substitute for a real daily log: it proves only what
commits prove (what changed, in which repo, per the actual diff) and invents
nothing else. It is not a replacement for writing daily notes — it's a
backfill for days that got missed.

This skill is designed for an Obsidian-style work vault, with daily notes at
`daily_obs/YYYY-MM-DD.md` and active project/repo metadata in
`memory/projects.md`.

## When to use

- Directly: the user asks to backfill, reconstruct, or fill in a daily note
  for a day that's missing one.
- Automatically: `/eod-summary` finds no `daily_obs/YYYY-MM-DD.md` for the day
  it's summarizing and invokes this skill before continuing.

## Procedure

1. **Confirm the target date.** Default to today if invoked standalone with no
   date given; if `/eod-summary` invoked this, use the date it's summarizing.
2. **Check the note doesn't already exist.** If `daily_obs/YYYY-MM-DD.md`
   already exists, stop and say so — never silently overwrite a real note.
   Ask the user before touching it.
3. **Find the candidate repos.** Pull "Active codebase" paths for
   currently-active projects from `memory/projects.md` (e.g.
   `~/code/example-service`). If it's unclear which
   repo(s) were touched that day, ask rather than guessing — don't silently
   scan every repo on disk.
4. **Get the user's git identity** in each candidate repo (`git config
   user.name` / `user.email` — read-only) and pull only their commits for the
   target date:
   ```
   git log --author="<name>" --since="YYYY-MM-DD 00:00" --until="YYYY-MM-DD 23:59" --date=local
   ```
   Don't attribute a co-worker's commit to the user.
5. **Verify each commit's real content before trusting its message** — run
   `git show --stat <hash>` (not just `git log`) and check the file list
   against what the message claims. A commit message that doesn't match its
   diff is a known failure mode (check the project notes for past
   instances) — don't repeat it. If a message and diff genuinely disagree,
   describe what the diff shows, not what the message claims.
6. **If no commits are found** for the user on that date in any candidate
   repo, say so plainly and stop — don't produce an empty or padded note.
   Ask the user whether to check a different repo, a different date, or skip
   reconstruction entirely.
7. **Write the note** with only a `## Done` section built from verified
   commits — see Output format. Do not populate `## Focus`, `## Open`, or any
   other narrative section: git has no record of intent, meetings, or
   unfinished thinking, so don't infer it.
8. **Save the note** to `daily_obs/YYYY-MM-DD.md`.
9. **Report back**: the file path, how many commits were used, which repos
   they came from, and explicitly what's still missing (Focus, Open, meetings,
   decisions) so the caller — whether that's the user directly or
   `/eod-summary` continuing its own flow — knows to ask for that rather than
   assume the day is fully captured.

## Output format

```markdown
---
date: YYYY-MM-DD
tags: [daily]
---
# YYYY-MM-DD

> Warning: Reconstructed from git commit history — no daily note was written this
> day. Content below is limited to what commits verify; Focus, Open, meetings,
> and decisions are not captured here.

## Done

### <commit summary, in the commit's own terms>
`<repo>` `<short hash>` — <files touched, from `git show --stat`, not the
message alone>. <One factual sentence of what the diff actually did, if it
adds meaningfully beyond the file list — no interpretation of intent or
impact beyond what's directly visible in the diff.>
```

One `###` entry per commit (or per tightly-related commit cluster, if several
commits obviously belong to one change). Order chronologically. Skip
merge/no-op commits unless they're the only activity that day.

## Rules

- **Verified-facts-only.** Every line in `## Done` must trace to a real diff
  you actually inspected via `git show --stat` — never to a commit message
  alone, and never to inference about what a change "probably" also did.
- **No narrative sections.** Never write `## Focus`, `## Open`, meeting notes,
  or decisions into a reconstructed note — those aren't in git and inventing
  them defeats the point of "verified content only."
- **Never overwrite an existing daily note.** If one exists, this skill does
  not run against it silently — confirm with the user first.
- **Say when there's nothing.** Zero commits for the user that day is a valid,
  reportable outcome — don't pad the note or widen the author/date filter to
  manufacture content.
- **The reconstruction banner is not optional.** It must be the first thing
  under the frontmatter, always — a reconstructed note must never be
  mistaken for a first-hand log later.
- **This is a backfill, not a habit.** If the user is reaching for this
  repeatedly, that's worth surfacing back to them (missing daily notes are a
  process gap this skill patches, not solves).
