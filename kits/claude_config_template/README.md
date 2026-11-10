# claude_config — drop-in template

A portable, project-agnostic version of the folder-based context system. Drop it
into any project, type `load CLAUDE.md` once, and it bootstraps itself.

Agent mode (`/feature-team` and the six role agents) is a separate, one-time
**global** install — `~/.claude/skills/` and `~/.claude/agents/` — not something
this template carries per project. On a new machine, set that up first (from
wherever you keep your sanitized agent/skill exports); every project on that
machine then gets it for free. See `claude_config/SPECIALIST_AGENTS.md` for
adding a project-specific specialist implementer on top of the global six.

---

## Install into a project

**One command:**
```bash
~/Desktop/claude_config_template/install-into.sh /path/to/your/project
```
This copies `claude_config/` and `CLAUDE.md` into the project (never clobbering an
existing `CLAUDE.md` — it lands as `CLAUDE.md.from-template`) and seeds
`docs/current_task.md`.

**Or by hand:**
```bash
cp -R claude_config /path/to/project/
cp CLAUDE.md /path/to/project/        # skip if the project already has one
```

## First run

Open the project in Claude Code and type:
```
load CLAUDE.md
```
Because `claude_config/.initialized` doesn't exist yet, the root `CLAUDE.md`
bootstrap section runs: it checks whether the global agent-mode install is
present, interviews you to fill the `<<placeholders>>` in the global profile,
creates a project context file from `projects/_TEMPLATE.md`, and marks itself
initialized. Every session after that is a normal session start.

## What's inside

```
claude_config_template/
├── README.md            # this file
├── CLAUDE.md             # root file copied to the project (has the bootstrap block)
├── install-into.sh      # copy into a target project
├── docs/
│   └── current_task.md  # fast re-entry point (seeded blank)
└── claude_config/
    ├── CLAUDE.md               # global profile — personal prefs + <<placeholders>>
    ├── README.md
    ├── SPECIALIST_AGENTS.md    # on-demand: adding a project-specific implementer agent
    ├── sessions/               # engineering / architecture / research / planning / agent
    ├── projects/_TEMPLATE.md
    ├── memory/                 # decisions / stack / changelog (blank)
    ├── commands/               # new-session / update-memory
    ├── TUTOR.md                # on-demand: Socratic codebase-teaching system prompt
    └── ai_assisted_dev/        # on-demand: guides for working with AI assistants
```

## Notes

- The global profile (`claude_config/CLAUDE.md`) ships with every personal
  preference blanked out as an `<<placeholder>>` — the bootstrap fills them in by
  asking. Nothing identifying is pre-filled.
- `claude_config/` is meant to be **gitignored** (local context). The bootstrap
  offers to add the ignore lines.
- Agent mode (`/feature-team`, its six role agents, `/draft-commit`) is **not**
  bundled here — it's a one-time global install at `~/.claude/skills/` and
  `~/.claude/agents/`, shared by every project on the machine. Set it up once per
  machine; this template only documents how to extend it per-project (see
  `claude_config/SPECIALIST_AGENTS.md`).
