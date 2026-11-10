# Intake routing table

The user edits this file to change routing. Rules are checked top to bottom; the first match wins. Matching is on the capture's text, case-insensitive.

## Fast path (rules, no judgement)

| # | If the capture... | Route | Launch |
|---|---|---|---|
| 1 | carries a tag `#research`, `#build`, `#feature`, `#issue`, `#note`, `#parallel` | the tagged route below | per that route |
| 2 | mentions auth, permissions, roles, billing, plan, seats, metering, usage limits, personal or regulated data | Build (single session), flagged sensitive | handoff only |
| 3 | names a repo folder under your code root (e.g. `~/code/`) or a file path with an extension | Build (single session) | handoff only |
| 4 | is a bug report or task list against a product (steps to reproduce, "doesn't", "no way to", "requires a refresh") | Issue notes | plan, then confirm |
| 5 | asks to compare, evaluate, research, "find out", "what's the best", or ends in a question about the outside world | Research swarm | auto-launch |
| 6 | is a meeting note, decision, person, tool verdict, reference or link | Note (inbox-sort types) | plan, then confirm |

## Routes

| Route | What intake does |
|---|---|
| Research swarm | Auto-launch a background session in the research workspace (e.g. `research-hub/`) running `/research-swarm <question>`; the brief carries the question only, nothing else from the inbox or the vault. |
| Build (single session) | Handoff: print the one-line command to open a session in the right repo with the task. Sensitive items say so in the handoff. |
| Feature | Show the routing, wait for yes, then hand off `/feature-team <brief>` to run in the repo session. |
| Parallel edits | Show the routing, wait for yes, then follow `/parallelize` launch mechanics. |
| Issue notes | One note per bug or task in the project's `issues/` (copy the issue template, e.g. `template_md/issue.md`), then regenerate the backlog index if the vault has a script for it, per the vault's agent instructions on work items. |
| Note | The `/inbox-sort` classification and destinations (meeting, decision, person, tool, project, reference). |

## Model pass

A capture that matches no fast-path rule is matched against your mode table (e.g. a `modes.md` in your agent config). If confidence is low, ask one question with 2 or 3 options.
