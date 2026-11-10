# Context

All Claude configuration for this project lives in `claude_config/`. This file is
auto-loaded into every session.

---

## First-Run Bootstrap (runs once, on the first `load CLAUDE.md`)

Before anything else, check whether `claude_config/.initialized` exists.

**If it does NOT exist**, this is a fresh drop-in of the template. Run the
bootstrap, in order, then stop and hand back to the user:

1. Check whether `/feature-team` and the six role agents are discoverable
   (`~/.claude/skills/feature-team/`, `~/.claude/agents/`). If this is a new
   machine and they're missing, tell the user — agent mode needs that global
   install first; it's no longer bundled per-project. See `SPECIALIST_AGENTS.md`
   for adding project-specific specialist agents once the global set is in place.
2. Open `claude_config/CLAUDE.md` and resolve every `<<placeholder>>` by asking
   the user (identity, preferences, default tech context). Write their answers in.
3. Create `claude_config/projects/<project-slug>.md` from
   `claude_config/projects/_TEMPLATE.md` by interviewing the user about this
   project — what it is, stack, structure, key files, decisions, risks.
4. Create `docs/current_task.md` from the template if it's missing or empty.
5. Ask whether the config should stay local; if yes, append `claude_config/` and
   `CLAUDE.md` to `.gitignore`.
6. Write today's date into `claude_config/.initialized`.
7. Tell the user setup is complete and show the Session Start menu below.

**If `.initialized` exists**, skip the bootstrap and do a normal Session Start.

---

## Load at session start

- `claude_config/CLAUDE.md` — global profile (always)
- `claude_config/sessions/[type].md` — one per session; `[type]` ∈ {engineering, architecture, research, planning, agent}
- `claude_config/projects/[project].md` — this project's full context
- `docs/current_task.md` — what was active last session (always)

Quick reference: `claude_config/README.md`
Agent mode (simulated dev team via `/feature-team`): installed globally at
`~/.claude/skills/feature-team/` with the six role agents in `~/.claude/agents/`.
Available in every project on this machine — no per-project install. Adding a
project-specific specialist implementer: `claude_config/SPECIALIST_AGENTS.md`.

On-demand (not auto-loaded — pull in when relevant):
- `claude_config/TUTOR.md` — Socratic codebase-teaching mode (understand code, don't change it).
- `claude_config/ai_assisted_dev/` — guides for working with AI assistants.
- `/draft-commit` — group an uncommitted tree into reviewable commit drafts.
- `/workshop <topic>` — time-boxed crash course to get *functional* in a topic fast (the inverse of TUTOR: spends a fixed budget to make you operational now).

## Session Start

**Engineering:**
```
Load claude_config/CLAUDE.md + claude_config/sessions/engineering.md + claude_config/projects/[project].md + docs/current_task.md.
Focus: [what you're working on today]
```

**Architecture:**
```
Load claude_config/CLAUDE.md + claude_config/sessions/architecture.md + claude_config/memory/decisions.md + docs/current_task.md.
Focus: [design question or decision]
```

**Research:**
```
Load claude_config/CLAUDE.md + claude_config/sessions/research.md + docs/current_task.md.
Focus: [tool or question being evaluated]
```

**Planning:**
```
Load claude_config/CLAUDE.md + claude_config/sessions/planning.md + claude_config/projects/[project].md + docs/current_task.md.
Focus: [sprint or roadmap item]
```

**Agent mode** (run a feature end-to-end with the simulated dev team):
```
Load claude_config/CLAUDE.md + claude_config/sessions/agent.md + claude_config/projects/[project].md + docs/current_task.md.
Focus: /feature-team [feature description]
```
No install step — `/feature-team` and its role agents live in `~/.claude/` and
are available in every project. If they aren't discoverable, this machine hasn't
had the global agent-skills install done yet; restart the session once it has.

## End of Session

```
Update memory. Decided: [X]. Findings: [Y]. Open: [Z].
```

Claude updates `claude_config/memory/decisions.md`, `claude_config/memory/stack.md`,
and `docs/current_task.md`.
