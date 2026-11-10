# Session: Architecture

> Load alongside CLAUDE.md + memory/decisions.md for system design, ADRs, and
> infrastructure decisions.

---

## How to reason here

- Start on **High** model for non-trivial design (see CLAUDE.md model table).
- Name the simplest viable option first, then justify any added complexity against it.
- Make tradeoffs explicit: latency, cost, operational burden, failure modes, lock-in.
- Separate reversible from irreversible decisions; spend rigor on the irreversible.
- Respect closed decisions in `memory/decisions.md` — don't silently reopen them.

## Output of a design discussion

When a decision closes, write it to `memory/decisions.md` with:
- **Decision** — what was chosen.
- **Rationale** — why, in 2–4 sentences.
- **Eliminated options** — what was rejected and why (prevents re-litigation).
- **Status / date.**

Also update `projects/[project].md` (Current Focus) and `memory/changelog.md`.

## ADR format (optional)

`## ADR-N: [title]` → Context · Decision · Consequences · Status.
