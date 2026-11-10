---
name: eod-summary
description: Generate an end-of-day / meeting-recap update in two versions from the same facts — a Technical log (Done / Decisions / Blockers / Next, mechanism-level) saved to the daily note only, and a Recap (narrative Summary, Open questions, and Action items grouped Fixes / Features / Deliverables with an owner and ISO due date each) saved to the daily note AND shown in chat. Pulls from today's daily log, meetings, decisions, and project/action-item changes. Use when the user wants an EOD update, meeting recap, standup post, or "what do I tell the team."
---

# EOD Summary

Produce two paired versions of today's work or meeting, from the same facts:

- **Technical** — an internal engineering log (Done / Decisions / Blockers /
  Next), mechanism-level, saved to the vault only. Not shown in chat.
- **Recap** — a broadcast-ready block (Summary / Open questions / Action items)
  for the team or a stakeholder. Saved to the vault AND shown in chat.

Both cover the same day and the same outcomes — only the shape and audience
differ, never the facts. Each is a broadcast someone skims, not a log. Bias
hard toward brevity; detail lives in the linked notes.

This skill is designed for an Obsidian-style work vault.
Expected folders: `daily_obs/`, `meetings_obs/`, `decisions_obs/`, and
`memory/` for project state.

If today's daily note doesn't exist yet, this skill delegates to
`/daily-retro` to backfill it from git history before continuing — see step 3
below.

## When to use

The user asks for an EOD / end-of-day update, meeting recap, standup post, or
something to send the team or a client after a call.

## Procedure

1. **Set the day.** Default to today; confirm only if ambiguous.
2. **Gather today's inputs:**
   - `meetings_obs/` notes dated today — the primary source when the day centers
     on a call or demo: who attended, what they saw, what came up
   - `daily_obs/YYYY-MM-DD.md` — Progress, Blockers, Tomorrow
   - `decisions_obs/` + `memory/decisions.md` entries dated today
   - `memory/projects.md` — any status change touched today
3. **If `daily_obs/YYYY-MM-DD.md` doesn't exist at all,** invoke `/daily-retro`
   for that date to reconstruct it from git history before continuing, then
   proceed as if it had existed.
4. **If today's notes exist but are thin** (including a just-reconstructed one
   that's commit-only), say so and ask the user for a few highlights rather
   than inventing activity, attendees, or outcomes.
5. **Write Technical first** — it's the direct distillation of the notes:
   Done (outcomes with file/component/mechanism named), Decisions (if any),
   Blockers/need, Next.
6. **Derive the Recap from Technical**, not by re-reading the source
   separately:
   - **Summary** — 3–6 sentences of prose translating Technical's Done/Blockers
     into what happened, what worked, what didn't, what's unresolved. No file
     paths, code identifiers, or internal component names — translate what a
     bullet *means*, not its mechanism.
   - **Open questions** — anything flagged as unclear, TBD, or needing a
     decision that isn't yet an actionable task. Name who it's blocked on if
     known. Don't let these get buried only in the Summary prose.
   - **Action items** — determine the due date/time and the reason (e.g. "to
     prep for Monday's call"); ask the user if not stated, don't guess a
     deadline. Sort each item into exactly one bucket:
     - **Fixes** — closing a gap in something that already exists.
     - **Features** — net-new capability that doesn't exist yet.
     - **Deliverables** — a concrete artifact or output being produced or
       handed off. May restate a fix/feature's tangible output — fine to list
       in both places when that's specifically what gets handed over.
     Give every item an owner (`@name`). If not stated or obvious, ask — don't
     default to the user or guess.
7. **Save both to today's daily note** under `## EOD`, as `### Technical` and
   `### Recap` subsections (matching existing daily notes' structure), in
   `daily_obs/YYYY-MM-DD.md`.
8. **Display only the Recap in chat** — the whole Summary / Open questions /
   Action items block, as one copy-pasteable section. Do not print Technical in
   chat; it lives in the file only.
9. **Run `/commit-check`** (always, as the last step). EOD is the natural
   checkpoint for committing the day's vault changes, so before any push, scan
   staged/unstaged/untracked changes for anything that must not hit the remote.
   Report its result inline after the Recap. If it flags nothing, note
   "commit-check: clean." If it flags something, surface it and do **not**
   proceed to commit until the user resolves it. This step never commits or
   pushes on its own.

## Output format

**Technical** (saved only, never shown in chat):
```
*EOD — YYYY-MM-DD*
Done:
• <outcome, not activity — what moved, with the file/component/mechanism named>
• <…>
Decisions: <only if any — one line each, link/name them>
Blockers / need: <what's blocking or where you need input — omit if none>
Next: <tomorrow's focus, 1–2 items>
```

**Recap** (saved AND shown in chat):
```
*EOD — YYYY-MM-DD*

Summary:
<3–6 sentences, prose. What happened, what worked, what didn't, what's
unresolved. Lead with the most important outcome. No file paths, code
identifiers, or internal component names.>

Open questions:
- <thing still unclear / needs a decision — name who it's blocked on if known>
- <…>

Action items (due YYYY-MM-DD, HH:MM — <reason, e.g. "to prep for Monday's call">):

Fixes:
- <item> — @owner

Features:
- <item> — @owner

Deliverables:
- <item> — @owner
```

Drop `Decisions` (Technical) or `Open questions` (Recap) entirely if there are
none — don't write "none." Drop any of Fixes/Features/Deliverables that's empty
rather than leaving an empty sub-header. Keep Technical's Done to ~3–6 bullets;
keep the Recap Summary to 3–6 sentences; keep each Action-items bucket to
what's actually actionable, not a running task list.

## Rules

- **Same facts, same order, both versions.** Recap is a translation of
  Technical's content, not a separate summary — never include an outcome in
  one and not the other (blockers/open questions especially).
- **Technical is internal, mechanism-level; Recap is external-facing, outcome-
  level.** Technical names files/components/root causes. Recap never does —
  translate mechanism into effect/impact ("the report preview now shows real
  column names instead of a placeholder," not "wired `GET /schemas` into
  `renderHeader`").
- **Due date is always ISO (`YYYY-MM-DD`), never locale-ambiguous.** Don't write
  `22-08` or `8/22` — write `2026-08-22`. Applies to any date in either version.
- **Every action item has an owner** (`@name`), assigned explicitly from the
  notes — never inferred or defaulted to "me." If genuinely unassigned, write
  `@unassigned` rather than omitting the tag or guessing.
- **Fixes vs. Features vs. Deliverables is about kind, not size.** Fixes repair
  something that exists; Features add something that doesn't; Deliverables are
  the tangible thing being produced or handed over. When in doubt: does the
  broken/missing thing already exist in some form? If yes, Fix; if wholly new,
  Feature.
- **Open questions are not action items.** An action item has an owner and a
  next step; an open question is still waiting on a decision or clarity before
  it can become one. Don't force a TBD into a bucket just to give it a home.
- **Outcomes over activity, in both.** "FAQ approach decided: leaning RAG, eval
  in progress" (Technical) / "Decided how the FAQ feature will work; now
  testing it" (Recap) — both beat "read about X all day."
- **Strip private/personal detail from both.** Health, mood, and the like don't
  go in either version — frame an absence neutrally, not with the reason.
- **Don't dump the timesheet.** Hours/time-log detail stay in the daily note
  unless the user asks to include them.
- **Don't invent work, attendees, or deadlines.** Only summarize what's in the
  notes or what the user just told you; if the day or meeting note is thin, ask
  — and say so plainly rather than padding either version or guessing a due
  date.
- **A note built by `/daily-retro` is verified-facts-only, treat it as thin.**
  It carries only a git-backed `## Done` section and a reconstruction flag —
  everything else (meetings, decisions, blockers, next) still needs to come
  from asking the user, never from inference.
- **Concise over complete.** When in doubt, cut it and let the linked note carry
  the detail.
- **Technical never appears in chat.** Save it to the file and move on — the
  chat reply is Recap-only.
- **Always finish with `/commit-check`.** The EOD run is also the vault's
  end-of-day git checkpoint; the safety scan runs every time, even if the
  update itself is thin.
