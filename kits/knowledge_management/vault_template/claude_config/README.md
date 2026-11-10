# claude_config

Context files that give Claude a standing understanding of this **work vault**. Replaces rebuilding context from scratch each session. Claude functions as a colleague with full context of the work — able to track projects, capture meetings, record and challenge decisions, evaluate tools, and hold who-owns-what across the whole vault.

---

## How It Works

You maintain structured markdown files. At the start of a session, tell Claude which files to load. Claude reads them and holds that context for the session.

**Mostly files, plus a few skills.** The base layer is plain markdown context. On top of that, a handful of `/skills` automate the recurring loops (logging, EOD/weekly roll-ups, inbox triage) — see `commands/skills.md`.

---

## Structure

```
<<vault-dir>>/
├── CLAUDE.md                     # Global profile — auto-loaded by Claude Code
│
claude_config/
├── sessions/                     # Session-scoped context — load one per session
│   ├── project.md                # Executing / tracking a project
│   ├── meeting.md                # Meeting prep, capture, follow-up
│   ├── decision.md               # Recording decisions (ADR-style)
│   ├── research.md               # Tool / tech evaluation and reviews
│   └── planning.md               # Roadmaps, priorities, task breakdown
│
├── memory/                       # Persistent context — updated as work changes
│   ├── projects.md               # Active projects + current state
│   ├── decisions.md              # Decisions + rationale + alternatives
│   ├── people.md                 # Who's who — roles, ownership, context
│   ├── tools.md                  # Evaluated tools — verdict, cost, use
│   ├── conventions.md            # Vault structure + note conventions
│   └── vault-map.md              # What's actually in the vault
│
├── commands/                     # Slash-commands + reusable prompt templates
│   ├── skills.md                 # Catalog of live /skills (tracking, eod-summary, …)
│   ├── new-session.md            # How to start a session
│   └── update-memory.md          # How to persist context
│
└── README.md                     # This file

<<vault-dir>>/template_md/         # Note templates — one per type (daily, meeting, decision, …)
```

---

## Starting a Session

**Project (execute / track a project):**
```
Load CLAUDE.md + sessions/project.md + memory/projects.md.
Focus: [project + what you're moving today]
```

**Meeting (prep, capture, or follow up):**
```
Load CLAUDE.md + sessions/meeting.md + memory/people.md.
Focus: [meeting — who, what it's about]
```

**Decision (make / record an ADR):**
```
Load CLAUDE.md + sessions/decision.md + memory/decisions.md.
Focus: [the decision in front of you]
```

**Research (evaluate a tool / approach):**
```
Load CLAUDE.md + sessions/research.md + memory/tools.md.
Focus: [tool or question being evaluated]
```

**Planning (roadmap, priorities, breakdown):**
```
Load CLAUDE.md + sessions/planning.md + memory/projects.md.
Focus: [horizon or project being planned]
```

---

## Ending a Session

```
Update memory. Decided: [X]. Status change: [Y]. Open / owed: [Z].
```

Claude updates the relevant memory files.

---

## Maintenance

| Trigger | Action |
|---|---|
| Project status changes | Update `memory/projects.md` + the project file |
| Decision made | Add to `memory/decisions.md` + a record in `decisions_obs/` |
| Tool evaluated | Update `memory/tools.md` + evaluation in `research_obs/` |
| New person in the work | Update `memory/people.md` |
| Vault structure / convention changes | Update `memory/conventions.md` + `CLAUDE.md` |
| Session type needed that doesn't exist | Create `sessions/[name].md` |

---

## Design Principles

- **Context over conversation.** Invest in the files, not re-explaining every session.
- **Memory is stable state.** In-progress thinking goes in notes; only settled state goes in memory.
- **One session type per session.** Don't mix modes in the same file load.
- **Files are ground truth.** If something isn't in a file, Claude doesn't know it next session.
- **Every action item has an owner.** Unowned work is a dropped thread.
- **Claude is a colleague, not a tool.** The config gives it standing context to push back, surface gaps, and hold the work as a coherent whole.
