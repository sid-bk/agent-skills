---
name: checkpoint
description: Log learning progress at the end (or middle) of a coding practice session — what the learner solved unaided, the load-bearing concept, what's still open, and the next bug/step. Updates the current task file and the project's fluency tracker. Use at session end, when the learner says "checkpoint", "let's stop", "update progress", or "what did I learn."
---

# /checkpoint — log the learning, not just the task

This is a learning project; the checkpoint captures **fluency gained**, not features
shipped. Keep it short — it's a 30-second re-entry point for next session.

## Do

1. **Update the current task file** (e.g. `docs/current_task.md`):
   - *In Progress* — the current problem/part and its state.
   - *Stuck on / next thing to surface* — the precise next step for next session.
   - *Next up*, *Completed* (move finished problems here), *Last Session Notes*
     (1–2 lines, dated, what happened — and confirm no solution code was provided).

2. **Update the fluency tracker** in the project config: bump any concept the learner
   demonstrated this session — `not yet → shaky → solid` (solid = written unaided).
   Add a one-line note where useful.

3. **Log learning debt:** add concepts to revisit to a *Concepts To Revisit* list,
   each with a search term or the problem it came up in.

## Tone

- Honest metric: only mark **solid** what the learner genuinely wrote without hints.
  Over-crediting defeats the project.
- Briefly name the single most load-bearing thing learned this session.
- No code, no solutions — this is bookkeeping.
