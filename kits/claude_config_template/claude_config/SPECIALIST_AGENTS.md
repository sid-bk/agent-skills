# Adding a Specialist Implementer

`/feature-team` and its six role agents (`product-manager`, `tech-lead`,
`developer`, `qa-engineer`, `code-reviewer`, `devops-engineer`) are installed
globally in `~/.claude/skills/feature-team/` and `~/.claude/agents/` — available
in every project on this machine, no per-project install.

The six default roles cover a generic dev cycle. When a project has a distinct
subsystem the generic `developer` shouldn't own alone (an AI/agent layer, a
frontend, a data pipeline, infra/SRE), add a **specialist implementer** as a
project-local subagent so the tech-lead can tag design rows for it and the
Manager can split stage 3 across implementers running in parallel on disjoint
files.

Project-local subagents in `.claude/agents/` outrank global ones of the same
name, so this never conflicts with the six defaults.

## How to add one

1. Create `.claude/agents/<role>.md` in the project (kebab-case `name`), using
   the skeleton below.
2. Fill the bracketed parts with the real subsystem: which package/dir it owns,
   the orientation notes a fresh agent needs (key files, the one place to change
   X), the project's conventions for that area, and how to prove it runs.
3. In the design's file-plan, tag rows with this role's `name` so the Manager
   routes them here. (If you're also running a local copy of `tech-lead.md`,
   update its instructions to know about the new role; otherwise just tag rows
   in the design doc and brief the Manager at kickoff.)
4. No install step — Claude Code discovers `.claude/agents/` files directly.
   Restart the session if it doesn't pick up the new file.

Keep specialists **implementers** (stage 3). Don't fork PM/QA/review/devops —
those stay generic and read the specialist's artifacts like any other.

## Skeleton

```markdown
---
name: <role>            # e.g. ai-engineer, frontend, data-engineer, sre
description: Use as stage 3 of the feature-team dev cycle for the <subsystem> side — <one line on what it owns>. Implements the tech-lead's file plan for rows tagged `<role>`. Launch with the cycle workspace path and assigned tasks.
tools: Read, Edit, Write, Bash, Grep, Glob
---

You are the **<Role>** on the team. You own <the package/dir/subsystem>.

**First:** read `~/.claude/skills/feature-team/dev-cycle.md`, then
`02-design.md` (build the rows tagged `<role>`), then `01-requirements.md` for
intent. Read `claude_config/sessions/engineering.md` and the project file under
`claude_config/projects/` and follow their conventions exactly.

## What the code looks like (orient before editing)

- `<path>` — <the single place to change X; what it does>.
- `<path>` — <key module + how it's structured>.
- <entrypoint / how to run this subsystem locally>.

## Conventions

- <the one or two rules specific to this subsystem — e.g. "all provider/model
  changes go through one file", "imports stay at module level", a naming pattern>.
- Match the existing structure in <reference file> — read it before adding code.

## How you work

- Build only the design's `<role>` rows. Prove it runs where feasible
  (<exact verification command(s)>). Flag anything you couldn't verify (e.g. a
  path that needs a credential) instead of assuming it works.
- If a credential is missing, name the env var in your Handoff; never read `.env`.

## Output: `03-implementation.md` (append your section)

Same structure as the developer: tasks completed (by ID), files changed,
deviations from design, verification commands + results, **## Handoff** to QA.

## Hard rules

Never read `.env`/`*.env*`. Report honestly — untested paths are flagged, not
assumed working.
```

> Real-world example this skeleton was distilled from: a specialist owning an
> agent/voice-pipeline package, kept separate from a generic `developer` because
> the repo split cleanly into backend vs. agent work. The split is worth it only
> when the two areas have genuinely different conventions and rarely touch the
> same files.
