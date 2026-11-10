---
name: draft-commit
description: Group the pending (uncommitted) git changes into coherent commits and draft a commit message for each group, at file granularity — no file is ever split across groups. Drafts and prints ready-to-run commands only; never stages, commits, or pushes. Invoke when the user wants help organizing a messy working tree into reviewable commits ("draft my commits", "group these changes", "/draft-commit").
---

# draft-commit

Turn an uncommitted working tree into a set of coherent, reviewable commit **drafts**. You group the pending files, write one message per group, and print the exact commands the user can run. You do **not** stage, commit, or push.

## Hard rules

1. **Draft only.** Never run `git add`, `git commit`, `git push`, `git stash`, or anything that mutates the index or working tree. Output is text + commands for the user to run.
2. **File granularity — no file split across groups.** Every pending file goes into exactly **one** group, whole. You may not propose `git add -p` / partial hunks. If a single file genuinely mixes concerns, it still goes in one group — pick the group matching its dominant concern and flag the mix (see §4).
3. **Completeness.** Every path from `git status --porcelain` must land in exactly one group (or be explicitly excluded as junk, §5). No path appears twice, none is dropped. State this invariant holds before you finish.

## 1. Gather state

Run (read-only):
- `git status --porcelain=v1` — the full set of pending paths (modified, added, deleted, renamed, untracked). This is the universe of files to assign.
- `git diff --numstat` and `git diff --staged --numstat` — change sizes, to gauge scope and spot large/entangled files.
- `git log -5 --format='%s'` — detect the repo's actual message convention before drafting, and match it. (Conventional Commits — `type(scope): subject` — is a common default if the history shows no clear convention.)

## 2. Decide whether to delegate (use a subagent if needed)

- **Small/clear tree** (≲8 files, obvious subsystems): do it inline.
- **Large or entangled tree** (many files, big diffs, or unclear concerns): launch **one** general-purpose subagent to read the actual `git diff` content and return a proposed grouping + per-group draft messages. This keeps large diffs out of the main context. Give the subagent: the `git status` paths, this skill's grouping + style rules (§3–§4, §6), and the Hard rules. The subagent reads and proposes; **you** review its output and present it. The subagent must not stage or commit either.

## 3. Group the pending files

Group by **concern / subsystem**, so each commit is independently reviewable and its message is a single coherent statement. Heuristics, in order:

1. **Same subsystem** — e.g. all files in one module + their tests; all graph nodes; all docs/config.
2. **Same change intent** — a feature, a fix, a refactor, a hygiene/lint pass, dependency bumps (a manifest + its lockfile belong together).
3. **Dependency order** — order the groups so prerequisites come first (data layer → runtime → callers); note when an intermediate group may not build in isolation because a file-level split forced it.

Keep groups small but not trivial. Tests travel with the code they cover unless they form their own coherent suite-wide change.

## 4. Be honest about entanglement

If a single file carries multiple concerns, you **cannot** split it (Hard rule 2). Put it in the group matching its dominant concern and add a one-line flag:
`Warning: <file> also contains <other concern> — can't isolate without git add -p (your call).`
Likewise flag when grouping by file forces an intermediate commit that won't import/build cleanly on its own.

## 5. Exclusions

- Recommend `git rm --cached <path>` for junk that shouldn't be tracked (e.g. `.DS_Store`) — do not silently fold it into a group.
- Gitignored paths won't appear in `git status` and won't be committed; if the user expected a gitignored file in a commit, say it's ignored.

## 6. Message style

- **Match the repo** (per the convention detected in §1). If it uses Conventional Commits: a `type(scope): subject` line (`feat`/`fix`/`refactor`/`chore`/`test`/`docs`), blank line, then a `-` bullet body. Otherwise follow whatever the history shows.
- Subject in imperative mood, ≤ ~72 chars, no trailing period.
- **Body is a terse bullet list, not prose.** One line per bullet, stating *what* changed — not why, not background, not rationale. Skip a bullet's justification unless the subject line would be genuinely misleading without it (rare — most changes don't need it).
- **2-4 bullets per commit, regardless of how many files or concerns are folded in.** Combine related changes into one bullet rather than writing one bullet per file. No sub-bullets, no multi-sentence bullets, no bullet that reads like a paragraph.
- If the project's git rules define a global commit trailer (e.g. a `Co-Authored-By:` line), end **every** drafted message with it. If none is defined, omit it.

Target shape:
```
fix: AB#1234 token leak in export event + settings-panel sizing

- Drop `session_token` from the export `done` event; update test + docs
- Settings: `.side-panel` min-height matches iframe, no more collapse/snap
- Settings: export-mode control switched from radio buttons to a switch
```
Not this (too long, explains why, one bullet per file):
```
- Drop `session_token` from the export `done` JSON event — the server
  already stores it and the shipped client never reads it back from
  that field. Test assertion and the public API doc updated
  to match.
- Settings page: `.side-panel` gets `min-height: 640px` matching the
  iframe's fixed height, so it doesn't render collapsed then snap
  taller once `app:export-ready` fires; also converts the
  export-mode control from radio buttons to a toggle switch.
```

## 7. Output

For each group, in dependency order, print:

```
### Group N — <one-line intent>
git add <space-separated paths>     # whole files only

<commit message, including any required trailer>
```

Then close with:
- a **coverage line** confirming every `git status` path is assigned to exactly one group (list any junk excluded under §5);
- any entanglement / build-in-isolation flags from §4;
- a reminder that nothing has been staged or committed — the user runs the commands, and per the project's git rules should branch first if on the default branch.
