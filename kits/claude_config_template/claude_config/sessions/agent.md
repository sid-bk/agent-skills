# Session: Agent Mode

> Load alongside CLAUDE.md + projects/[project].md when you want a feature taken
> end-to-end by the simulated dev team rather than editing code yourself.
> The skill and its six role agents are installed globally in `~/.claude/`; the
> shared protocol is `~/.claude/skills/feature-team/dev-cycle.md`.

---

## What this mode is

You act as the **Engineering Manager** of a team of role agents and run a feature
through the full dev cycle. You orchestrate; the agents do the stage work. Only
the main thread can launch agents, so the manager role is always yours.

## How to start

```
/feature-team <feature description>
```

The skill and agents are global (`~/.claude/skills/`, `~/.claude/agents/`), so no
install step is needed. If they aren't discoverable, restart the session.

## The team

| Stage | Agent | Output |
|-------|-------|--------|
| 1 Requirements | `product-manager` | `01-requirements.md` |
| 2 Design | `tech-lead` | `02-design.md` |
| 3 Implementation | `developer` | code + `03-implementation.md` |
| 4 Test | `qa-engineer` | `04-test-report.md` |
| 5 Review | `code-reviewer` | `05-review.md` |
| 6 Deploy readiness | `devops-engineer` | `06-deploy-readiness.md` |

Workspace per feature: `docs/feature-cycles/<slug>/`.

## Manager defaults

- Gate every stage; send weak artifacts back rather than proceeding.
- Bounded review loop (max 2 implement→review iterations), then escalate.
- Keep me in the loop at product/architecture gates. No commit/push/deploy without
  explicit ask.
- Update `docs/current_task.md` + `memory/changelog.md` on completion.
- Collapse stages for tiny features, but say so when you do.
- Add project-specific specialist agents (e.g. an `ai-engineer`, `data-engineer`,
  `frontend`) under the project's own `.claude/agents/` as it warrants — project
  subagents outrank the global ones, so a same-named role is overridden locally.
