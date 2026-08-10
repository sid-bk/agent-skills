# Meeting Mode

Use when: prepping for, capturing, or following up on a meeting.

---

## Operating Mode

Three phases — know which one you're in:

| Phase | Goal |
|---|---|
| **Prep** | Agenda, context, and the open items worth raising |
| **Capture** | Clean notes during/after, separating discussion from decisions from actions |
| **Follow-up** | Extract action items with owners, route outcomes |

The output is a clean dated meeting note with decisions and owned action items.

## Priorities

- **Prep:** pull open action items and recent decisions involving the attendees; surface what to raise before they forget
- **Capture:** keep discussion, decisions, and action items in separate sections — don't blur them
- Every action item needs an owner and, ideally, a due date. Flag the ones that don't.
- Route outcomes: decisions → `decisions_obs/` + `memory/decisions.md`; action items → the relevant project; new people → `people_obs/` + `memory/people.md`
- Link the note to the project(s) it affects

## Meeting Note Format

```markdown
# YYYY-MM-DD — [Meeting title]
**Attendees:** ...
**Project(s):** [[...]]

## Decisions
- ...

## Action items
- [ ] (owner) ... — due ...

## Notes
...
```

Stored dated in `meetings_obs/`.

**Template:** `template_md/meeting.md`
