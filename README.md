# agent-skills
A collection of skills that I've created, sourced, referenced and outright forked. May it help you as much as it has me.

These are task-oriented agent skills, rewritten to be **model- and agent-agnostic**: branding, host-specific URLs, personal names, and machine-specific paths have been removed, while references to the genuine underlying tools and sources are kept. Each file is a standalone skill — YAML frontmatter (`name`, `description`) followed by the instructions an agent should follow when the skill activates.

## Index

### Development workflow

| Skill | What it does |
|-------|--------------|
| [draft-commit](dev-workflow/draft-commit.md) | Group a messy working tree into coherent, reviewable commit drafts (drafts commands only — never stages/commits). |
| [feature-team](dev-workflow/feature-team.md) | Run a feature end-to-end through a manager-orchestrated team of role subagents with gates and a bounded review loop. |
| [feature-team-support/](dev-workflow/feature-team-support/) | The six role definitions (`product-manager`, `tech-lead`, `developer`, `qa-engineer`, `code-reviewer`, `devops-engineer`) and the shared `dev-cycle.md` protocol that `feature-team` orchestrates. Not skills — install these as subagents. |
| [bug-fix](work-vault/bug-fix.md) | Enforce a project's bug-fix conventions end-to-end — branch name, commit message format, PR description. |
| [security-review](security-review.md) | Menu-driven security review: scan a codebase, scan a diff, or generate verified patch files to apply by choice. |
| [user-stories](user-stories.md) | Generate user stories and tickets — derived from an existing codebase or from a fresh use case description. |

### MCP

| Skill | What it does |
|-------|--------------|
| [build-mcp-server](mcp/build-mcp-server.md) | Design & build a Model Context Protocol server — deployment model, tool-design pattern, framework, auth. |
| [build-mcp-app](mcp/build-mcp-app.md) | Add interactive UI widgets (forms, pickers, dashboards) to an MCP server. |
| [build-mcpb](mcp/build-mcpb.md) | Package an MCP server with its runtime as a bundled, installable local server. |

### UI & artifacts

| Skill | What it does |
|-------|--------------|
| [frontend-design](ui/frontend-design.md) | Distinctive, intentional visual design for new or reshaped UI — palette, typography, layout, copy. |
| [playground](ui/playground.md) | Build self-contained single-file interactive HTML playgrounds (controls → live preview → copyable prompt). |
| [project-artifact](project-artifact.md) | Generate & publish an opinionated tabbed project status page, refreshable as a delta against the previous render. |

### Research & learning

| Skill | What it does |
|-------|--------------|
| [storm-research](research/storm-research.md) | Deep, multi-source research using the STORM method (perspective-guided Q&A → outline → cited synthesis). |
| [math-olympiad](research/math-olympiad.md) | Solve competition math (IMO/Putnam/USAMO/AIME) with fresh-context adversarial verification and calibrated abstention. |
| [workshop](workshop.md) | Time-boxed crash course — make the user *functional* at a topic within a fixed number of hours. |
| [hint](coding-practice/hint.md) | One graduated hint toward the problem the learner is stuck on — stops before any code. |
| [review-mine](coding-practice/review-mine.md) | Review the learner's own code by teaching through questions; never writes the corrected version. |
| [checkpoint](coding-practice/checkpoint.md) | Log fluency gained at the end of a coding-practice session, not features shipped. |

### Work vault

Obsidian-style vault skills. Path-bound to a vault's folder conventions (`daily_obs/`, `memory/`, …) — adapt the paths before use.

| Skill | What it does |
|-------|--------------|
| [tracking](work-vault/tracking.md) | Quick-log an activity into today's daily note; escalate to memory only when it carries a settled fact. |
| [eod-summary](work-vault/eod-summary.md) | Tight end-of-day update for standup or Slack, drawn from the day's notes. |
| [weekly-review](work-vault/weekly-review.md) | Weekly roll-up — aggregate logs, total time by project, surface what stalled, set next week's priorities. |
| [timesheet](work-vault/timesheet.md) | Hours summary over any custom date range. Reporting only. |
| [inbox-sort](work-vault/inbox-sort.md) | Triage and clear the capture inbox, routing each note to its folder and updating memory. |
| [commit-check](work-vault/commit-check.md) | Pre-push safety scan — secrets, credentials, PHI, confidential or machine-local material. |

### Domain

| Skill | What it does |
|-------|--------------|
| [livekit-agents](livekit-agents.md) | Build voice AI agents with LiveKit Cloud and the Agents SDK (handoffs, tasks, mandatory tests). |

## Maintaining this collection

This repo holds **sanitized copies only**. Operational copies — the ones that actually run — live in `~/.claude/skills/` (personal, available across every project) or a project's `.claude/skills/`. The two tiers are deliberately different, and the difference is the point:

| | Sanitized (here) | Operational (`~/.claude/`) |
|---|---|---|
| Paths | Generic — "the project's conventions file" | Concrete — the real path |
| Tooling | "your task-tracking tools" | The actual tool names |
| Names, hosts, orgs | Removed | Whatever is true locally |

**Sanitize on export; never sync.** A new skill is written where it will run, then a genericized copy is added here. Copying back the other way would drag host-specific paths into a public repo; symlinking the two would collapse the distinction entirely.

Before committing a new skill, check that it names no person, employer, client, internal hostname, absolute home path, or private repo, and that any file paths it references are either generic or clearly flagged as an example.

## Notes on adaptation

- **Agnostic wording.** Assistant/model names, product branding, and host-specific narrative were replaced with neutral terms ("the agent", "the model", "an MCP host", "the web-publish tool", etc.).
- **Sources kept.** Genuine external references are retained where they're needed to do the task — e.g. the MCP spec (modelcontextprotocol.io), LiveKit (docs.livekit.io), and the STORM method (Stanford OVAL).
- **Functional tool/package names.** Where a specific package or CLI is required to actually perform the task (MCP SDKs, the `mcpb` packaging CLI), the name is kept as a tool reference rather than removed.
- **Sensitive data removed.** Usernames in paths, personal names, emails, repo URLs tied to a specific account, and any credentials/tokens were stripped or genericized.
