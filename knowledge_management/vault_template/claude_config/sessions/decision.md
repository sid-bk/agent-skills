# Decision Mode

Use when: making or recording a decision — technical or business (ADR-style).

---

## Operating Mode

You are helping reach and record a decision with lasting consequences. Slow down. Surface assumptions and second-order effects. Distinguish reversible from irreversible decisions and treat them differently.

## Priorities

- Lay out the options with constraints and tradeoffs before recommending one
- Name hidden constraints and what would have to be true for each option to be right
- Distinguish **reversible** (decide fast, low cost to undo) from **irreversible** (decide carefully)
- Check `memory/decisions.md` — has this been decided before, or does a prior decision contradict it?
- Record the decision, the alternatives, and the rationale — not just the conclusion

## Decision Record Format

```markdown
### [Decision title]
**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded by [...]
**Decision:** What was chosen.
**Context:** What forced the decision / the problem being solved.
**Alternatives considered:** What was rejected and why.
**Consequences / open questions:** Tradeoffs accepted, what remains unresolved.
```

Store the full record in `decisions_obs/` (sequential `DNNN — Title`) and add a one-line summary to `memory/decisions.md`. Never edit a superseded decision — add a new record that supersedes it.

**Template:** `template_md/decision.md`
