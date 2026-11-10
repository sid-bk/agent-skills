# Session: Engineering

> Load alongside CLAUDE.md when writing, debugging, or reviewing code.
> Stack versions and costs: memory/stack.md · project conventions: projects/[project].md

---

## Code Conventions

> Fill these from the project's actual conventions on first setup. Defaults:

- Match the surrounding code's style, naming, and comment density.
- No blocking calls in async/event-loop code.
- Config loaded once and injected, not read ad hoc.
- Typed request/response models at boundaries.
- Structured logging with fields, not string interpolation.
- <<project-specific conventions>>

---

## Engineering Defaults

- Show the failure mode before the solution.
- If there's a simpler approach I haven't considered, name it before the complex one.
- Flag when a pattern I'm using has a known limitation (races, blocking, N+1, etc.).
- Note when a change is untested and what the risk is.

---

## Session Start Protocol

After loading context, produce a numbered task breakdown before asking what to
work on:

```
**N. [Action verb] [what]**
Review [specific file(s)] first — [one-line reason].
[Blockers or prerequisites inline.]
```

Rules: order by dependency; reference the specific file(s) to review before each
step; flag blocked steps inline; 3–4 lines per step; end with one line on what can
start now vs. what's blocked.

## Changelog Protocol

Update `memory/changelog.md` automatically — don't wait to be asked. One entry per
session, append-only. Format: `## Session N — YYYY-MM-DD — [title]`. Append under
**Done** as code units complete; finalize **Done** + **Pending** when the session ends.
