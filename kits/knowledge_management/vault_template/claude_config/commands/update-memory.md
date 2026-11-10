# Persisting Context

Update memory the moment something is finalised — don't wait for end of session.

## Quick Template

```
Update memory. Decided: [X]. Status change: [Y]. Open / owed: [Z].
```

## What Gets Updated

| What happened | File to update |
|---|---|
| Decision made | `memory/decisions.md` (summary) + a record in `decisions_obs/` |
| Project status changed | `memory/projects.md` + the project file in `projects_obs/` |
| Tool evaluation concluded | `memory/tools.md` + write-up in `research_obs/` |
| New person enters the work | `memory/people.md` (+ `people_obs/` if recurring) |
| Meeting held | dated note in `meetings_obs/`; route action items to their project |
| New convention or folder | `memory/conventions.md` + `CLAUDE.md` |
| Significant content added to an area | `memory/vault-map.md` (periodically, not every session) |

## Decision Entry Format

```markdown
### [Decision title]
**Date:** YYYY-MM-DD
**Status:** Accepted
**Decision:** What was chosen.
**Context:** What forced it.
**Alternatives considered:** What was rejected and why.
**Consequences / open questions:** Tradeoffs accepted, what's still open.
```

## When NOT to Update Memory

- In-progress thinking — that belongs in the project note, not memory
- Session output (a draft, a plan) — the file itself is the record
- Temporary context — if it won't matter next session, don't write it
- Things already captured elsewhere in the vault — memory supplements, it doesn't duplicate
