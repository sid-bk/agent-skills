---
name: bug-fix
description: Enforce a project's bug-fix workflow conventions (branch name, commit message format, PR description) end-to-end. Invoked as `/bug-fix #<task_id> <short-title>` when starting work on a bug ticket, or proactively whenever the user says they're fixing a bug/ticket/issue. Reads the project's recorded conventions from CLAUDE.md or a project config file before proceeding.
---

# Bug Fix

Enforces the bug-fix conventions recorded in the project's CLAUDE.md or config file
so they're applied consistently instead of re-derived or forgotten each session. This
is a workflow skill, not a design skill — it governs branch/commit/PR mechanics around
whatever fix is being implemented, not the fix itself.

## Trigger

- Explicit: `/bug-fix #<task_id> <short-title>`
- Implicit: the user says something like "fix bug 101", "let's work on #101",
  "QA found X, let's fix it".

If `task_id` is missing, ask for it before creating a branch — it's load-bearing
for both the branch name and every commit subject.

**Default output is the brief only.** On invocation, produce the brief (issue
description + planned fix, including the branch name per step 3) and stop there.
Do not run `git status`, create the branch, write code, commit, or open a PR unless
the user explicitly asks you to proceed with that step. Don't volunteer to do so
either — state what's next and wait.

## Procedure

1. **Read the project conventions.** Read the project's CLAUDE.md or convention file
   to determine: branch naming pattern, commit message format, main branch name, and
   PR requirements. If no conventions are recorded, ask the user to specify them before
   proceeding.

2. **Check working tree state.** Run `git status`. If there are uncommitted changes
   unrelated to this bug, stop and flag it — don't branch off a dirty tree silently.

3. **Create the branch** off the project's main branch:
   ```
   git checkout <main-branch> && git pull && git checkout -b bug/#<task_id>-<slug>
   ```
   `<slug>` is a short kebab-case description of the bug. State the exact branch
   name in your reply before running the checkout command — don't create it silently.

4. **Implement the fix.** Smallest correct change — touch the bug, not surrounding
   code.

   **Do not write or run a test suite unless the user specifically asks for one.**
   Default verification is manual: give the user a short, concrete guide (exact
   commands/URLs/clicks, expected before/after behavior).

5. **Commit message format** — apply the project's recorded commit conventions exactly.
   Common pattern:
   ```
   fix/#<task_id>: <short imperative summary>

   <terse technical body: where the change lives and what it does mechanically>
   ```
   If the project has a different convention, use that. Don't conflate the branch
   naming prefix with the commit-subject prefix — they often differ.

6. **Open the PR.** Title short; description must include:
   - Brief issue description (what was wrong)
   - Fix implemented (what changed, mechanically)
   - Screenshot or test output showing the corrected behavior
   Do not open the PR without evidence of the fix — ask the user for one or to confirm
   how to capture it if the fix has no visual surface.

## Rules

- Branch-type in the branch name and commit subject may differ — read the project
  conventions rather than assuming they match.
- Never skip the PR evidence requirement silently — surface it if you can't produce one.
- This skill only governs workflow mechanics. For the actual fix design, use normal
  engineering process (explore → plan → implement → verify).
