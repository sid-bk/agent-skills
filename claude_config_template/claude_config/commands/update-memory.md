# Command: /update-memory

> Run when a fact is finalised, or at the end of a session, to persist context.

---

## Usage

```
Update memory. Decided: [X]. Findings: [Y]. Open: [Z].
```

## What Claude should update

| What happened | File |
|---|---|
| Decision closed | `memory/decisions.md` + `projects/[project].md` + `memory/changelog.md` |
| Tool added / removed / evaluated | `memory/stack.md` + `memory/changelog.md` |
| Code unit completed | `projects/[project].md` + `memory/changelog.md` + `docs/current_task.md` |
| Session ends | `docs/current_task.md` — write Last Session Notes for fast re-entry |

**Finalised** = won't be revisited / confirmed / works. Not iterative edits or open
questions. Keep `docs/current_task.md` short and current — it answers "where did we
leave off?" in 30 seconds.
