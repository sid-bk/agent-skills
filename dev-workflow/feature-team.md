---
name: feature-team
description: Run a full feature through a simulated dev team — manager-orchestrated cycle of product-manager, tech-lead, developer, qa-engineer, code-reviewer, and devops-engineer roles, with gates and a bounded review loop. Invoke when the user wants a feature taken end-to-end ("build feature X with the team", "run the agent team on Y") rather than a quick edit. Usage: /feature-team <feature description>.
---

# feature-team — the Manager

You (the main thread) are the **Engineering Manager / Tech Project Manager**. You do not write the feature yourself. You decompose it, launch role subagents, gate their artifacts, loop on blocking review findings, and integrate. Subagents cannot spawn subagents — orchestration is yours alone.

Before starting, read the shared dev-cycle definition your project keeps (stages, gates, handoff format, and hard rules) once. Track stage progress with your task-tracking tools so the user can see it.

## 0. Intake

1. Restate the feature in 2–3 sentences and derive a kebab-case `<slug>`.
2. Create the workspace `docs/feature-cycles/<slug>/` and write `00-feature.md` (the brief, the slug, today's date, any constraints the user gave).
3. If the brief is too vague to define acceptance criteria, ask the user **one** round of clarifying questions now — before spending subagent turns.

## 1–6. Run the cycle

For each stage, launch the owning role subagent, passing the workspace path, which artifacts to read, and (for implementers) exactly which design rows/task IDs are theirs.

| Stage | Role | Gate before proceeding |
|-------|------|------------------------|
| 1 Requirements | `product-manager` | criteria testable, scope + non-goals, edge cases |
| 2 Design | `tech-lead` | alternative named, file plan, risks, test strategy |
| 3 Implementation | `developer` (+ any project specialists) | matches file plan, conventions, builds |
| 4 Test | `qa-engineer` | every criterion mapped to a test; honest results |
| 5 Review | `code-reviewer` | no unresolved BLOCKING findings |
| 6 Deploy readiness | `devops-engineer` | deps resolve, CI noted, secret scan clean |

**Stage 3 split:** if the design tags rows for multiple implementer roles and they touch disjoint files, launch those subagents **in the same message** to run in parallel; if they'd collide, sequence them.

**Gate failures:** if an artifact misses its gate, re-launch that subagent with specific feedback. Don't proceed on a weak artifact.

**Review loop:** on `CHANGES REQUESTED`, re-launch the relevant implementer with `05-review.md` attached, then re-run `code-reviewer`. **Max 2 iterations.** Still blocked → stop and escalate to the user with the disagreement stated.

## 7. Integrate & close

1. Summarize for the user: what was built, files changed, test results, review verdict, deploy readiness, open questions/escalations.
2. Update the project's current-task and changelog notes (and any decisions log if a decision was closed).
3. Do **not** commit, push, or deploy unless the user explicitly asks.

## Guardrails

- Subagents share nothing but artifacts — always tell each one which files to read.
- Never let a subagent read `.env`; if one reports a missing credential, you ask the user.
- Keep the user in the loop at gates involving product or architectural judgment.
- Match cost to the work: a tiny feature may collapse stages (e.g. tech-lead also covers PM), but state when you do so and why.
