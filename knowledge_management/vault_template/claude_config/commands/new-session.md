# Starting a Session

## Template

```
Load CLAUDE.md + sessions/[type].md.
Focus: [specific project, meeting, decision, or question]
```

## Session Types

| Type | File | Use when |
|---|---|---|
| Project | sessions/project.md | Executing or tracking a specific project |
| Meeting | sessions/meeting.md | Prepping for, capturing, or following up a meeting |
| Decision | sessions/decision.md | Making or recording a decision (ADR) |
| Research | sessions/research.md | Evaluating a tool, tech, vendor, or approach |
| Planning | sessions/planning.md | Roadmaps, priorities, task breakdown |

## Optional Additions

- Add `memory/projects.md` when you need current project state in context
- Add `memory/decisions.md` when prior decisions are relevant
- Add `memory/people.md` for meetings or anything stakeholder-heavy
- Add `memory/tools.md` when evaluating something that may already be reviewed
- Add `memory/vault-map.md` when navigating existing vault content

## Examples

**Move a project forward:**
```
Load CLAUDE.md + sessions/project.md + memory/projects.md.
Focus: [project] — clear the current blocker and update status
```

**Prep for a meeting:**
```
Load CLAUDE.md + sessions/meeting.md + memory/people.md.
Focus: [meeting] — pull open action items for the attendees and set an agenda
```

**Record a decision:**
```
Load CLAUDE.md + sessions/decision.md + memory/decisions.md.
Focus: [the decision] — options, tradeoffs, and a recommendation
```

**Evaluate a tool:**
```
Load CLAUDE.md + sessions/research.md + memory/tools.md.
Focus: [tool] for [use case] — verdict with rationale
```
