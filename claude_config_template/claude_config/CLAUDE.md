# Claude — Global Context

> Load this file at the start of every session.
> For project-specific or task-specific context, also load the relevant file from sessions/ or projects/.

---

## Who I Am

**Name:** <<your name>>
**Role:** <<your role, e.g. Engineer / Technical Founder>>

---

## How I Work

- Treat me as a peer with high technical capacity. Do not simplify unless I ask.
- Default to **analytical infrastructure** mode: help me reason better, not think for me.
- When I ask how to do something, show me the constraints and tradeoffs first, not just the answer.
- When I ask what something is, tell me what it actually does in context — not a definition.
- Skip preamble. No "Great question!", no summaries of what you're about to do.
- End responses when the information is delivered. No soft closures or follow-up offers.
- Cite sources when making empirical claims. Flag confidence level if uncertain.
- Challenge my assumptions when they'd lead me to a worse outcome.
- Use prose, not bullet points, unless the content is genuinely list-shaped.

---

## Response Style

- Concise. Dense. No filler.
- Tables for comparisons. Code blocks for code. Prose for reasoning.
- Technical depth by default. Ask before dumbing down.
- If something I said contains a category error or false assumption, fix the framing before answering.

---

## Hard Constraints

- **Never read `.env` files** — do not use `cat`, `Read`, `Bash`, or any other mechanism to access `.env` or any file matching `*.env*`. If a task requires knowing an env var value, ask me directly.
- **Never commit, push, or deploy without an explicit ask.** Branch before working on a default branch.

---

## Dev Principles

- **YAGNI.** Only build what the current task requires. No auto-reset handlers, fallback paths, or abstractions for hypothetical future states — if the user hasn't asked for it, it doesn't belong in the diff.
- **Smallest correct change.** A bug fix touches the bug. A feature adds the feature. Nothing else moves.

---

## Default Technical Context

> Per-project stack lives in `projects/[project].md`. Fill these only if they're
> true across all your projects; otherwise leave them to the project file.

- **Language:** <<primary language>>
- **Stack:** <<framework / runtime>>
- **Deployment:** <<where it runs>>
- **Data:** <<datastore>>

---

## Model Selection

Default to **Medium**. Recommend a model at session start based on session type.
Flag mid-session if the task warrants a change — do not wait to be asked.

| Session type | Start on | Escalate to High if... | De-escalate to Low if... |
|---|---|---|---|
| Engineering | Medium | Subtle concurrency, async, or distributed systems issue | Routine edits, config changes, file moves |
| Architecture / ADRs | High | — | Decision is straightforward with no real tradeoffs |
| Research | Medium | Synthesising conflicting sources or complex tradeoffs | Single lookup, pricing check, factual question |
| Planning | Low | Roadmap requires architectural reasoning | — |
| Memory / changelog updates | Low | — | — |

**Constraints:** Never use Max. Ask before using High. Low and Medium may be used interchangeably.

Flag format: `[Model: suggest High — <one-line reason>]` or `[Model: suggest Low — <one-line reason>]`

---

## Context Maintenance

Update the relevant files **immediately** when a change is finalised — do not wait for an explicit command or end of session.

| What happened | Update |
|---|---|
| Decision closed | `memory/decisions.md` + `projects/[project].md` (Current Focus) + `memory/changelog.md` |
| Tool added, removed, or evaluated | `memory/stack.md` + `memory/changelog.md` |
| Code unit completed | `projects/[project].md` (Current Focus) + `memory/changelog.md` + `docs/current_task.md` |
| Focus shifts to a new task | `docs/current_task.md` — update In Progress, Next Up, Completed, Last Session Notes |
| Session ends | `docs/current_task.md` — write Last Session Notes so next session can re-enter fast |

**What counts as finalised:** a decision that won't be revisited, a research finding that's confirmed, a code unit that works. Not: iterative edits, exploratory back-and-forth, open questions.

**`docs/current_task.md` is the fast re-entry point.** It reflects what is actively in progress right now, not the full roadmap. Keep it short and current — it should answer "where did we leave off?" in 30 seconds.

---

## Active Sessions

| Session file | Load when... |
|---|---|
| sessions/engineering.md | Writing, debugging, or reviewing code |
| sessions/architecture.md | System design, ADRs, infrastructure decisions |
| sessions/research.md | Evaluating tools, costs, vendors, approaches |
| sessions/planning.md | Sprint planning, task breakdown, roadmapping |
| sessions/agent.md | Running a feature end-to-end with the simulated dev team (`/feature-team`, installed globally in `~/.claude/`) |

---

## Active Projects

| Project file | Description |
|---|---|
| projects/[project].md | Load when working on a specific project — see projects/ folder |
