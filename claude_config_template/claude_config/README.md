# claude_config

A folder-based context system for Claude. Instead of re-explaining context every
session, you maintain structured markdown files and load the relevant ones at the
start of a session.

**Just files.** The functional pieces — `/feature-team`, `/draft-commit`, and the
six role agents — live globally in `~/.claude/`, available in every project on
this machine. This folder holds context, not agent definitions.

---

## Structure

```
claude_config/
├── CLAUDE.md                   # Global profile — load in every session
│
├── sessions/                   # Session-scoped context — load one per session
│   ├── engineering.md
│   ├── architecture.md
│   ├── research.md
│   ├── planning.md
│   └── agent.md                # agent-mode session (the dev team)
│
├── projects/                   # One file per project
│   └── _TEMPLATE.md            # copy → projects/<your-project>.md
│
├── memory/                     # Persistent facts
│   ├── decisions.md            # decisions + rationale + eliminated options
│   ├── stack.md                # tools: role, version, cost, latency
│   └── changelog.md            # append-only per-session log
│
├── commands/                   # How-to prompts
│   ├── new-session.md
│   └── update-memory.md
│
├── SPECIALIST_AGENTS.md        # on-demand: adding a project-specific implementer agent
│
├── TUTOR.md                    # on-demand: Socratic codebase-teaching system prompt
├── ai_assisted_dev/            # on-demand: guides for working with AI assistants
│   ├── guide_junior_dev.md     # spec-driven workflow; avoiding comprehension debt
│   └── guide_llm_project_config.md  # fill-in LLM project-config doc
│
└── README.md
```

---

## Starting a session

Pick a type and a focus; load four things — global profile, the session file, the
project file, and `docs/current_task.md`:

```
Load claude_config/CLAUDE.md + claude_config/sessions/[type].md + claude_config/projects/[project].md + docs/current_task.md.
Focus: [what you're working on]
```

(Architecture sessions swap the project file for `memory/decisions.md`.)

## Ending a session

```
Update memory. Decided: [X]. Findings: [Y]. Open: [Z].
```

## On-demand extras

Not loaded every session — pull them in when relevant:

- **`TUTOR.md`** — a Socratic codebase-teaching system prompt. Load it (`Load
  claude_config/TUTOR.md`) when you want Claude to help you *understand* a codebase
  rather than change it: it surfaces structure and asks questions instead of
  pasting code. Mutually exclusive with normal engineering mode — it deliberately
  won't write code for you.
- **`ai_assisted_dev/`** — two human-facing guides: `guide_junior_dev.md` (the
  spec-driven workflow and how to avoid comprehension debt) and
  `guide_llm_project_config.md` (a fill-in project-config doc to feed an assistant
  at the start of a project). Reference material, not session context.
- **`/draft-commit`** — group an uncommitted working tree into reviewable commit
  drafts. Installed globally at `~/.claude/skills/draft-commit/`, along with
  `/feature-team` and the six role agents in `~/.claude/agents/`. See
  `SPECIALIST_AGENTS.md` for adding a project-specific implementer on top of them.

## Design principles

- **Context over conversation.** Invest in the files, not re-explaining each session.
- **Memory is stable decisions.** In-progress thinking doesn't go in memory.
- **One session type per session.** Don't mix engineering and architecture.
- **Files are ground truth.** If it isn't in a file, Claude doesn't know it next session.
