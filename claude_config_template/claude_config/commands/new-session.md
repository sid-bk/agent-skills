# Command: /new-session

> Run at the start of any work session to load the right context.

---

## Usage

```
Load claude_config/CLAUDE.md + claude_config/sessions/[type].md + claude_config/projects/[project].md + docs/current_task.md.
Focus: [what you're working on]
```

### Session types

| Type | File | When |
|---|---|---|
| Engineering | sessions/engineering.md | Writing/debugging/reviewing code |
| Architecture | sessions/architecture.md | System design, ADRs, infrastructure |
| Research | sessions/research.md | Tool evaluation, cost analysis, benchmarks |
| Planning | sessions/planning.md | Sprint planning, task breakdown |
| Agent | sessions/agent.md | Run a feature end-to-end with the dev team (`/feature-team`) |

(Architecture swaps `projects/[project].md` for `memory/decisions.md`.)

## What Claude should do on session start

1. Acknowledge which files were loaded.
2. State what it knows about today's focus.
3. Flag any open decisions in memory/decisions.md relevant to today's work.
4. Recommend a model for the session type (CLAUDE.md model table).
5. Begin — no further preamble.
