---
name: parallelize
description: Give a concise recommendation on how to run the current task or set of tasks more efficiently as parallel agents with minimal extra token cost. Invoked as /parallelize [task or task list]. Recommends only; launches nothing until the user says go.
---

# /parallelize

Produce a short recommendation (under 250 words) on which parts of the current work should run as parallel agents, which should stay in this session, and what it will cost. Stop after the recommendation. Launch agents only when the user then asks for it.

## Inputs (read as little as possible)

The task or list in the user's message; otherwise the open tasks already in this conversation. Only if neither names the work, read the newest daily note's `## Next steps` and `## Open`. Do not read project files to size the work; use what is already in context and label any estimate as an estimate.

## Decision rules

A track is worth its own agent only if all of these hold:
- It writes files no other track writes (single writer per file), or writes nothing.
- It has an observable done condition and its result fits in a report of about 300 words.
- It is read-heavy or a bounded edit, so keeping its reads out of this session's context saves more than the launch costs.
- It needs no decision from the user mid-run.

Keep a track in this session if any of these hold:
- It takes fewer than about three tool calls. Delegating adds a brief and the agent's own context load.
- Its output is needed immediately by the next step and there is nothing else to do meanwhile.
- It needs a command a headless pane agent cannot run under your permission policy: anything outside its allowlist (e.g. interpreters, installs, `rm`, `mv`, `cp`, git writes), multiplexer commands, or any irreversible action or one that needs the user's credentials. Headless agents usually run with a restricted `PATH` and tool set (file read/edit/write plus allowlisted reads), and every permission "ask" becomes a deny.
- It touches auth, billing or metering boundaries, or needs judgement the user has not delegated.

## Choosing the vehicle

| Vehicle | Use for | Cost note |
|---|---|---|
| This session | Short steps, anything needing approval prompts or non-allowlisted commands | No handoff loss |
| Subagent | Read-heavy digestion that returns a conclusion (audits, searches, summaries) | Brief plus its reads; returns only the summary |
| Pane agent (terminal multiplexer) | Independent edits or writes you want visible and running side by side | Own full context (project instruction files plus reads), plus a brief |

Two to four parallel agents is the practical range: each carries its own context, and more than four makes panes unreadably small.

## Keeping token cost down

- Brief by reference: point at file paths and line ranges, never paste file contents. State the goal, constraints, files allowed to change and the done condition.
- Cap the report: ask for a final reply under a stated word limit; detail goes in the file the agent edits.
- One writer per file; split by file or folder, not by step within a file.
- Tell agents which tools they lack so they do not burn turns on denied commands.
- Prefer bounded reads (offset and limit, Grep with line numbers) over whole-file reads in the brief.
- Do not parallelize to save wall-clock time on a path that waits on a human decision; close the decision first.

## Layout (standing preference)

This session stays in the left half or the top half. Agents split the remaining space equally. Use your multiplexer's layout query to read the current pane size, then:
- Pane wider than twice its height in cells (terminal cells are about twice as tall as wide): main stays left. Split the main pane right at ratio 0.5, then stack the agents as equal rows in the right half.
- Otherwise: main stays on top. Split down at ratio 0.5, then place the agents as equal columns in the bottom half.
- For N agents in the remaining half, split the first agent pane with ratio 1/N, then split the remainder with 1/(N-1), and so on. After splitting, check the resulting layout and fix sizes with the multiplexer's resize command.
- Open panes without stealing focus and with a literal working directory. An explicit layout from the user overrides this.

## Launch mechanics (only after the user says go)

Source of truth: your setup's own documentation for headless pane agents, if it has one; follow it over this outline. Needs the agent session running inside a scriptable terminal multiplexer.

1. Write a per-run scratch directory `<scratch>/pane-runs/<run-id>/` containing `task.md` (the brief) and a `cwd` file with one absolute path. Run ids use letters, digits, `_` and `-`.
2. Split panes per the layout rule and record each new pane id.
3. Start your agent runner in each pane with its run id, using exactly the form your permission policy allows.
4. Wait for the pane to print a done marker (e.g. `PANE_AGENT_DONE <run-id>`) with a timeout, then read the run's `out.md` and `exit_code`. Verify the result before reporting it as done.
5. Close the pane once the run has ended.

## Output format

1. Verdict in one line: parallelize N tracks, or do not.
2. A table: track, vehicle, files it owns, why it qualifies (or why it stays here).
3. Layout line for the chosen split.
4. Cost line: extra context loads versus what stays out of this session, labelled as an estimate.
5. Risks and anything that blocks a track, one line each.
6. End with the question of which tracks to launch, or that none are worth it.
