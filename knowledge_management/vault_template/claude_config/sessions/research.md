# Research Mode

Use when: evaluating tools, libraries, services, vendors, or technical approaches.

---

## Operating Mode

You are helping make a sound build / buy / adopt decision. The output is usually a tool evaluation, a comparison, or a recommendation with rationale — captured in `research_obs/` and, once concluded, summarised in `memory/tools.md`.

## Priorities

- Check `memory/tools.md` first — has this, or a close alternative, already been evaluated?
- Compare on the axes that matter: fit for the use case, cost, maturity, lock-in, performance/latency, developer experience, maintenance burden
- Separate marketing claims from verified behaviour — test it or cite a source, don't assume
- Flag what's well-established vs. contested vs. unknown, and state your confidence
- End with a recommendation **and** the conditions under which it would change
- When the choice is real and lasting, route it to decision mode → `decisions_obs/`

## Evaluation Format

```markdown
# [Tool / approach] — evaluation
**Use case:** what it's being considered for
**Verdict:** Adopt | Trial | Hold | Avoid
**Cost:** pricing / licensing / hidden costs
**Strengths:** ...
**Weaknesses / risks:** ...
**Alternatives:** ...
**Notes / benchmarks:** ...
```

Concluded verdicts go to `memory/tools.md` (full write-up stays in `research_obs/`).

**Template:** `template_md/research.md`
