---
name: intake
description: >-
  Single point of ingestion for the work inbox. Finds captures added to the vault's inbox.md since the last pass (below the intake marker) or takes one item given as an argument, routes each to the right workflow (research swarm, single build session, feature-team, parallel edits, issue notes, or note filing) using routing.md, launches the reversible ones and hands off or confirms the rest. Runs at session launch when new captures exist. Usage: /intake [item].
---

# /intake — the router

You sort and dispatch. You do not do the routed work yourself in this pass, apart from filing notes and issue notes once the user confirms the plan.

## 0. Preconditions

- Never run in the research workspace (e.g. `research-hub/`; its sessions must not see the inbox). If the working directory is inside it, stop and say so.
- Read `routing.md`, bundled alongside this skill, once.

## 1. Collect

- **With an argument:** that text is the one item.
- **Without one:** in the vault's `inbox.md`, search (with line numbers) for `<!-- intake: seen above this line -->`. The new captures are the non-blank lines after it. If there are none, say "no new inbox captures" and stop. If the marker is missing, everything below the last `---` divider is new; say the marker was missing.
- Split new text into captures: a blank line separates captures, and a heading or a numbered list with its sub-lines stays one capture. When the split is unclear, treat the block as one capture.

## 2. Route

For each capture apply the fast path in `routing.md`, then the model pass. Produce one table:

| # | Capture (first 60 chars) | Route | Why (rule # or reason) | Action |
|---|---|---|---|---|

## 3. Dispatch

- **Auto-launch (research swarm):** start a separate background agent session, working in the research workspace, whose whole task is `/research-swarm <question>` (or your equivalent research skill), giving it a run-id. Do not wait on it; tell the user the run-id and where results will land (e.g. `research-hub/runs/<run-id>/index.md`). If you cannot launch a background session, hand off instead: print the one-line command to open an agent session in the research workspace with `/research-swarm <question>`.
- **Handoff (build):** one line per item: the repo to open and the prompt to give, e.g. `cd ~/code/<repo> && <agent-cli> "<task>"`. Mark sensitive items.
- **Confirm first (feature, parallel edits, issue notes, notes):** show the table and wait for the user's yes per item or for all. Then apply: issue notes and notes follow the vault's agent instructions file (its work-item and context-maintenance sections) and the `/inbox-sort` procedure; feature work is handed off as `/feature-team <brief>` in the repo session; parallel edits follow `/parallelize` launch mechanics.
- **Parked:** anything the user defers stays in the inbox.

## 4. Update the inbox

- Delete each capture that was launched, handed off, or filed (its record is now in the daily note or its destination).
- Move the marker line to the end of the file, so parked captures sit above it and the next pass sees only newer ones.
- Never delete a capture the user has not routed or confirmed; never reword one.

## 5. Record

In today's `daily_obs/YYYY-MM-DD.md` (create from the daily note template, e.g. `template_md/daily_engineering.md`, if missing), under `## Open`, one line per routed capture: `intake: <capture summary> -> <route> (<run-id or destination>, <status>)`. A handoff stays open until the user does it.

## Rules

- Research briefs carry the question only; no inbox context, project names that are not in the question, or vault content.
- Discards need the user's explicit OK.
- Launch nothing irreversible (writes to shared state, installs, long-lived processes, anything sent to a third party) without a risk statement and the user's go-ahead.
