---
name: inbox-sort
description: Triage and clear the work vault's inbox_obs/ — read each captured note, classify it, route it to the right folder (projects/meetings/decisions/people/research/references), and update the memory files (projects.md, decisions.md, people.md, tools.md, vault-map.md) so the whole system stays current. Use when the user wants to sort, triage, process, clear, or "do" the inbox.
---

# Inbox Sort

Process every raw capture in `inbox_obs/` and propagate it across the vault: distill it, file it in the correct folder, update the relevant memory file, and leave the inbox empty. The end state is **nothing left in `inbox_obs/`** except the `_placeholder.md`, and every captured item either filed or explicitly discarded with the user's OK.

This implements the Capture → Triage workflow in `claude_config/memory/conventions.md`. Read that file and the relevant `claude_config/memory/*.md` files before classifying, so routing matches existing projects, people, and conventions.

## When to use

The user asks to sort / triage / process / clear / empty the inbox, or it's the weekly maintenance pass.

## Procedure

1. **Load context.** Read `claude_config/memory/conventions.md`, `projects.md`, `people.md`, `decisions.md`, and `tools.md`. These are what you route *into* — you need the current project names, people, and existing decisions/tools to avoid duplicates and route correctly.

2. **Enumerate the inbox.** List every note in `inbox_obs/` except `_placeholder.md`. If the only file is the placeholder, report "inbox empty" and stop.

3. **Classify each item.** Read it and assign exactly one primary type:

   | Type | Signal | Routes to |
   |---|---|---|
   | **Action** | A task / to-do / follow-up | The relevant project's open items (`projects_obs/` + `memory/projects.md`); or `daily_obs/` if not tied to a project. Must get an **owner**. |
   | **Meeting** | Notes from a conversation/call | A dated note in `meetings_obs/`; split out its decisions and action items and route those too |
   | **Decision** | A choice made or to be made | `decisions_obs/` (`DNNN — Title`) + a summary line in `memory/decisions.md` |
   | **Person** | Info about someone in the work | `people_obs/` (if recurring) + `memory/people.md` |
   | **Tool / research** | A tool, library, or approach being evaluated | `research_obs/` + a row in `memory/tools.md` if it has a verdict |
   | **Project** | A new initiative | A note in `projects_obs/` + an entry in `memory/projects.md` |
   | **Reference** | A runbook, how-to, link, doc | `references_obs/` |
   | **Noise** | No lasting value | Discard — **only after confirming with the user** |

   An item can spawn several outputs (a meeting note yields a decision + two action items). Classify by the primary artifact, then route the spawned pieces.

4. **Present the triage plan first.** Before changing anything, show a table: each inbox item → its type → its destination(s) → the memory file(s) it will touch. Flag anything ambiguous, anything you'd discard, and anything that needs an owner you don't know. **Wait for confirmation.** This pass touches the whole vault and may delete notes — do not apply blind.

5. **Apply, item by item.** For each confirmed item:
   - **Distill, don't dump.** Rewrite the raw capture into the destination's format (decision record, person note, tool evaluation, meeting note) — don't just move raw text. Preserve every fact; drop only filler.
   - Create or append to the destination note. When appending an action item, give it an owner and a due date if known; mark unknowns explicitly (e.g. `(owner: ?)`).
   - Update the corresponding memory file in the same step (a decision isn't done until it's in `memory/decisions.md`).
   - Add `[[links]]` connecting the new note to its project and the people involved.
   - Remove the item from `inbox_obs/` once it's filed.

6. **Reconcile memory.** After filing, make sure memory reflects reality: new projects in `projects.md`, status changes applied, new people in `people.md`, tool verdicts in `tools.md`. If a folder gained meaningful content, update `memory/vault-map.md`. Bump the `Last updated` date on any memory file you changed.

7. **Report.** End with a summary: how many items processed, where each went, what was discarded, and — importantly — every **open thread left behind**: action items with no owner, decisions that are only "Proposed", ambiguous items you parked. These are what the user needs to resolve next.

## Rules

- **Never discard without explicit confirmation.** When unsure whether something is noise, keep it and ask.
- **Never lose information.** If you can't confidently classify an item, leave it in `inbox_obs/` and list it as unresolved rather than forcing a destination.
- **Every action item gets an owner**, even if the owner is "me" or "?". Unowned work is a dropped thread.
- **No duplicates.** Check existing projects/people/decisions/tools before creating new ones — append to or update the existing note instead.
- **Don't touch the `_placeholder.md` files**, and don't delete a folder's placeholder when you add the first real note unless the user asks.
- Match the vault's naming and tag conventions from `conventions.md`.
