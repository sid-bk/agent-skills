# agent-skills
A collection of skills that I've created, sourced, referenced and outright forked. May it help you as much as it has me.

These are task-oriented agent skills, rewritten to be **model- and agent-agnostic**: branding, host-specific URLs, personal names, and machine-specific paths have been removed, while references to the genuine underlying tools and sources are kept. Each file is a standalone skill — YAML frontmatter (`name`, `description`) followed by the instructions an agent should follow when the skill activates.

## Index

| Skill | What it does |
|-------|--------------|
| [frontend-design](frontend-design.md) | Distinctive, intentional visual design for new or reshaped UI — palette, typography, layout, copy. |
| [playground](playground.md) | Build self-contained single-file interactive HTML playgrounds (controls → live preview → copyable prompt). |
| [workshop](workshop.md) | Time-boxed crash course — make the user *functional* at a topic within a fixed number of hours. |
| [math-olympiad](math-olympiad.md) | Solve competition math (IMO/Putnam/USAMO/AIME) with fresh-context adversarial verification and calibrated abstention. |
| [storm-research](storm-research.md) | Deep, multi-source research using the STORM method (perspective-guided Q&A → outline → cited synthesis). |
| [draft-commit](draft-commit.md) | Group a messy working tree into coherent, reviewable commit drafts (drafts commands only — never stages/commits). |
| [feature-team](feature-team.md) | Run a feature end-to-end through a manager-orchestrated team of role subagents with gates and a bounded review loop. |
| [security-review](security-review.md) | Menu-driven security review: scan a codebase, scan a diff, or generate verified patch files to apply by choice. |
| [build-mcp-server](build-mcp-server.md) | Design & build a Model Context Protocol server — deployment model, tool-design pattern, framework, auth. |
| [build-mcp-app](build-mcp-app.md) | Add interactive UI widgets (forms, pickers, dashboards) to an MCP server. |
| [build-mcpb](build-mcpb.md) | Package an MCP server with its runtime as a bundled, installable local server. |
| [livekit-agents](livekit-agents.md) | Build voice AI agents with LiveKit Cloud and the Agents SDK (handoffs, tasks, mandatory tests). |
| [m5-onboard](m5-onboard.md) | Provision an M5Stack ESP32 device end-to-end: detect on USB, flash UIFlow 2.0, install a MicroPython app bundle. |
| [cardputer-buddy](cardputer-buddy.md) | Iterate on the Cardputer-Adv MicroPython app bundle after provisioning (add apps, push, tail, REPL). |
| [project-artifact](project-artifact.md) | Generate & publish an opinionated tabbed project status page, refreshable as a delta against the previous render. |

## Notes on adaptation

- **Agnostic wording.** Assistant/model names, product branding, and host-specific narrative were replaced with neutral terms ("the agent", "the model", "an MCP host", "the web-publish tool", etc.).
- **Sources kept.** Genuine external references are retained where they're needed to do the task — e.g. the MCP spec (modelcontextprotocol.io), LiveKit (docs.livekit.io), the STORM method (Stanford OVAL), and M5Stack / UIFlow / esptool for the hardware skills.
- **Functional tool/package names.** Where a specific package or CLI is required to actually perform the task (MCP SDKs, the `mcpb` packaging CLI, esptool), the name is kept as a tool reference rather than removed.
- **Sensitive data removed.** Usernames in paths, personal names, emails, repo URLs tied to a specific account, and any credentials/tokens were stripped or genericized.
