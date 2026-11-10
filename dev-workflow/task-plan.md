---
name: task-plan
description: Enforce a project's task workflow conventions (branch naming) end-to-end, with a mandatory design-review pass before implementation. Invoked as `/task-plan #<task_id> <short-title>` when starting work on a ticket — bug or feature — or proactively whenever the user says they're fixing a bug/ticket/issue or picking up a task. Reads the project's recorded conventions from CLAUDE.md or a project config file before proceeding.
---

# Task Plan

Enforces the task workflow conventions recorded in the project's CLAUDE.md or config file
so they're applied consistently instead of re-derived or forgotten each session. This
is a workflow skill, not a design skill — it governs branch mechanics and a mandatory
review pass around whatever change is being implemented, not the change itself. It stops
at implementation — committing and opening a PR are separate, not owned by this skill.

## Trigger

- Explicit: `/task-plan #<task_id> <short-title>`
- Implicit: the user says something like "fix bug 101", "let's work on #101",
  "QA found X, let's fix it", "let's plan out ticket Y".

If `task_id` is missing, ask for it before creating a branch — it's load-bearing
for the branch name.

**Default output is the brief only.** On invocation, produce the brief — issue
description, consequences if not fixed, planned fix (including the branch name
per step 3), **and the Review Checklist pass from step 3.5, run against the
planned fix** — and stop there. Do not run `git status`, create the branch, or
write code unless the user explicitly asks you to proceed with that step. Don't
volunteer to do so either — state what's next and wait.

## Procedure

1. **Read the project conventions.** Read the project's CLAUDE.md or convention file
   to determine: branch naming pattern and main branch name. If no conventions are
   recorded, ask the user to specify them before proceeding.

2. **Check working tree state.** Run `git status`. If there are uncommitted changes
   unrelated to this task, stop and flag it — don't branch off a dirty tree silently.

3. **Create the branch** off the project's main branch:
   ```
   git checkout <main-branch> && git pull && git checkout -b task/#<task_id>-<slug>
   ```
   `<slug>` is a short kebab-case description of the task. State the exact branch
   name in your reply before running the checkout command — don't create it silently.

3.5. **Review the plan.** Before implementing, run the planned fix through the
   project's own Review Checklist if one is recorded (e.g. in the project's
   engineering conventions file). If no project
   checklist is recorded, apply this list directly:
   1. YAGNI-compliant? Scoped to what's actually asked, no speculative generality.
   2. Latency/resource impact? Cost on the hot path — extra queries, allocations,
      blocking calls, memory growth. Verify claims against the actual code path,
      don't assume.
   3. Edge cases? Inputs/states that break it or fall outside the happy path.
   4. Pros and cons, named explicitly — not just the upside.
   5. Is there a better alternative? Name it even if the current plan is still
      the pick — don't silently discard options.

   Surface findings before writing code. A finding that changes scope is a
   scoping question back to the user, not a silent design change.

4. **Implement the fix.** Smallest correct change — touch the task's actual scope,
   not surrounding code.

   **Do not write or run a test suite unless the user specifically asks for one.**
   Default verification is manual: give the user a short, concrete guide (exact
   commands/URLs/clicks, expected before/after behavior).

   This is the last step this skill owns. Committing and opening a PR are
   separate actions — use the project's own commit/PR conventions or another
   skill for those; don't fold them into this one.

## Rules

- Never skip the step 3.5 review pass silently, even under time pressure — a plan
  that hasn't been run through it isn't ready to implement.
- This skill only governs branch/review mechanics. For the actual fix design, use
  normal engineering process (explore → plan → implement → verify). For
  committing and PRs, use the project's own workflow, not this skill.
