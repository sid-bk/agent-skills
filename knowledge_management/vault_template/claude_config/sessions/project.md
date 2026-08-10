# Project Mode

Use when: executing or tracking a specific project or initiative.

---

## Operating Mode

You hold the full state of the project: goal, status, what's in flight, what's blocked, who owns what, and what was last decided. The output of a project session is usually progress made, an updated status, or an unblocked path forward.

## Priorities

- Start from the project's current state in `projects_obs/` and `memory/projects.md` — don't re-derive it from scratch
- Surface blockers, dependencies, and dropped threads before starting new work
- Flag action items with no owner or no due date
- Connect related meetings (`meetings_obs/`) and decisions (`decisions_obs/`) to the project
- Name it when scope creeps, or when a "project" is really an open-ended area with no end state
- Keep status honest: what's actually done vs. in progress vs. not started

## Relevant Areas

| Area | Location |
|---|---|
| Project file | `projects_obs/[project].md` |
| Meetings affecting it | `meetings_obs/` |
| Decisions made | `decisions_obs/` |
| People involved | `people_obs/` |
| Roadmap / priorities | `planning_obs/` |

## On Update

When something is finalised, update `memory/projects.md` (current state) and the project file. Log any decision in `decisions_obs/` + `memory/decisions.md`. Route new action items to the project with an owner.

**Template:** `template_md/project.md`
