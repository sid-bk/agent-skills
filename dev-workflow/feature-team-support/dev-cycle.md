# Agent Mode — Shared Dev-Cycle Protocol

> Every agent in the team reads this file first. It defines the stages, the
> handoff format, the gates, and the hard rules. Role-specific behaviour lives
> in each agent's own definition under `agents/`.

---

## Topology (read this — it explains why the team is shaped this way)

Claude Code only lets the **main conversation thread** launch subagents (via the
Agent tool). A subagent **cannot** spawn further subagents. Therefore:

- The **Manager** is not an agent. It is the main thread running the
  `feature-team` skill. It decomposes the feature, launches each role agent,
  gates their output, loops, and integrates.
- Role agents are stateless workers. They start fresh with no memory of each
  other and **communicate only through artifacts on disk** — never assume another
  agent's context. Read the upstream artifacts; write yours.

---

## The cycle

| # | Stage | Owner | Produces |
|---|-------|-------|----------|
| 0 | Intake | Manager | `00-feature.md` (the brief + cycle metadata) |
| 1 | Requirements | `product-manager` | `01-requirements.md` |
| 2 | Design | `tech-lead` | `02-design.md` |
| 3 | Implementation | `developer` (+ specialists) | code + `03-implementation.md` |
| 4 | Test | `qa-engineer` | `04-test-report.md` |
| 5 | Review | `code-reviewer` | `05-review.md` |
| 6 | Deploy readiness | `devops-engineer` | `06-deploy-readiness.md` |

Stage 3 may split across multiple implementer agents on disjoint files, and 4↔5
may loop back to 3.

---

## Workspace & handoff artifacts

For a feature, the Manager creates:

```
docs/feature-cycles/<slug>/
├── 00-feature.md
├── 01-requirements.md
├── 02-design.md
├── 03-implementation.md
├── 04-test-report.md
├── 05-review.md
└── 06-deploy-readiness.md
```

`<slug>` is kebab-case from the feature title. Every artifact ends with a
**`## Handoff`** section: a 3–6 line summary of what the next stage needs to know
(decisions made, open questions, files touched). The next agent reads the whole
workspace but acts on the Handoff sections first.

---

## Gates (the Manager enforces these)

A stage is not "done" until its gate passes. If it fails, the Manager sends it back
with specific feedback — it does not paper over gaps.

- **Requirements gate:** acceptance criteria are testable; scope + non-goals
  explicit; edge cases named.
- **Design gate:** a simpler alternative was considered and named; file-level
  change plan exists; risks + test strategy stated.
- **Implementation gate:** matches the design's file plan; follows project
  conventions; no `.env` reads; builds/imports cleanly.
- **Test gate:** every acceptance criterion maps to a test; failures reported
  honestly with output, not hidden.
- **Review gate:** no unresolved **blocking** findings.
- **Deploy gate:** dependencies resolve; CI implications noted; no secret leakage.

---

## Review loop policy

`code-reviewer` classifies findings as **blocking** or **non-blocking**. On
blocking findings the Manager re-launches the relevant implementer with the review
attached. **Max 2 implement→review iterations.** If still blocked, stop and
escalate to the user with the disagreement stated plainly — do not loop forever or
silently accept a known defect.

---

## Hard rules (every agent, no exceptions)

- **Never read `.env` or any `*.env*` file** — not with Read, Bash, or anything. If
  a value is needed, state which env var and let the Manager ask the user.
- Follow the project's own conventions — `CLAUDE.md` at the repo root, or where the
  project keeps them: `claude_config/CLAUDE.md`,
  `claude_config/sessions/engineering.md`, and the project file under
  `claude_config/projects/`. Read them when relevant.
- Report status faithfully. Tests failing → say so with output. Step skipped → say
  so. Done and verified → say so plainly, no hedging.
- Stay in your lane. PM doesn't design APIs; reviewer doesn't fix code; devops
  doesn't redefine requirements. Flag cross-lane issues in your Handoff instead.
- Dense over verbose. No filler.
