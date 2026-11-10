---
name: research-swarm
description: >-
  Answer a research question by splitting it into 2 to 4 sub-questions, running one background research-worker per sub-question, and merging their cited findings into a run note in a research hub folder. The main session is the router: it decomposes, launches, checks and merges, and never searches itself. Use for multi-source research, tool or approach evaluation, or comparing sources. Usage: /research-swarm <question>.
---

# /research-swarm — the router

You are the router. You do not search, fetch or read sources yourself. You split the question, launch workers, check their results, and merge them. The hub's own conventions file (its isolation rules) applies throughout.

The worker is defined in `agents/research-worker.md`, bundled alongside this skill. It is not a skill — install it as a subagent definition so the router can launch it by name.

Never `cd`, and use absolute paths in every tool call. If a permission gate treats the session's current directory as the project folder, a `cd` into one run's folder makes every later run's files read as outside the project and triggers prompts.

## 0. Preconditions

1. The working directory must be the research hub's root folder. If not, stop and tell the user to start the session there (isolation depends on it).
2. Retention: use a file-search tool (not shell loops, which tend to trigger permission prompts) with pattern `^(created|promoted):` over `runs/*/index.md`, and list runs with `promoted: no` and a `created` date more than 30 days ago. If any, one line naming them as deletion candidates (deleting is irreversible; do not delete).

## 1. Decompose

Split the question into 2 to 4 independent sub-questions, each with a done condition (what an answer looks like). A question that does not split gets one worker; say so. If the question is ambiguous, give 2 or 3 readings with trade-offs and wait. Otherwise launch without asking.

Derive `run-id` = `YYYYMMDD-<kebab-slug>` and a short kebab `track` name per sub-question.

## 2. Write the run index

Create `runs/<run-id>/index.md`:

```markdown
---
run: <run-id>
question: <question as the user asked it>
created: YYYY-MM-DD
status: running
promoted: no
---
# <question>

## Tracks
- [[<run-id>__<track>]] - <sub-question> (done when: <condition>)

## Synthesis
(pending)

## Cost
(pending)
```

## 3. Launch

Launch one `research-worker` subagent per track in a single message, all running in the background. Each brief contains only:

- the sub-question and its done condition (never anything else from the conversation)
- the spill path `<hub-root>/runs/<run-id>/<run-id>__<track>.md` (absolute)
- the budget: at most 15 tool calls for a narrow sub-question (one fact, one comparison, one tool), at most 25 for a broad one (a century, a field's literature, several lenses). State which in the index line for that track. If a worker still ends `partial`, its gaps go under Gaps; do not relaunch
- the run-id and track name

## 4. Check each result (watchdog)

As each worker reports:

- **Drift:** the report does not answer its sub-question, or the spill file is missing. Mark the track `drifted` in the index and leave it out of the synthesis.
- **Suspicious sources:** any listed in the spill file are left out of the synthesis and named in it.
- **Stalled:** if one worker is still running well after the others have finished (about 15 minutes), stop it and mark the track `timed-out`.

Do not relaunch a failed track automatically; name it as a gap.

## 5. Merge

Replace the `## Synthesis` section in `index.md`:

- **Answer:** the direct answer in a short paragraph.
- **Findings:** one line per claim, each with its confidence, a `[[<run-id>__<track>]]` link and the source URL.
- **Conflicts:** where tracks or sources disagree.
- **Gaps:** what no track established, including drifted or timed-out tracks.

Read a full spill file only when a worker's report is not enough to merge, and then with a file-read tool, one file per call. Avoid shell commands (`cat`, globs) for spill files: they may trigger permission prompts, and a large combined output can be saved outside the hub, where reading it back prompts again. Then the check: every line under Findings must contain both `[[` and `http`. Do it with a file-search tool on `index.md` (not `awk` or `sed`); fix or drop any line that fails.

## 6. Close

1. Fill `## Cost`: `**Cost:** <N> workers, <total subagent tokens from the task notifications>, <tracks drifted or timed out>`.
2. Set `status: done` in the index frontmatter with a file-edit tool (not `sed -i`).
3. Reply in chat in under 200 words: the answer, confidence, the main gaps, and the path to `index.md`. Promotion to a long-term knowledge base is the user's call; do not offer to do it from here.
