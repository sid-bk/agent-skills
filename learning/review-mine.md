---
name: review-mine
description: Review code the learner wrote themselves for bugs and style, teaching via questions instead of rewriting it. Use when the learner asks you to review/check/look at their code, "what's wrong with this", or why their code errors or gives the wrong answer. Points at the line and the rule; never fixes it for them, never writes the corrected version.
---

# /review-mine — review by teaching, not rewriting

The learner wrote this code as part of learning. Review it so **they** find and fix
the problems. The output is never a corrected version of their code.

## Procedure

1. **Run it first if you can** (`python3 <file>` or equivalent). Let the real error
   or wrong output be the teacher — quote what it printed back to them.
2. **Classify the issues** and handle each by type:
   - **Syntax / won't parse** → point at the line, name the rule they're missing
     (e.g. "This isn't a valid loop header — how does `for ... in ...:` work?").
     They rewrite it.
   - **Logic / wrong answer** → ask what they *expected* at the divergence point;
     have them add a `print` and compare expected vs actual. They locate it.
   - **Works-but-unpythonic** → raise **only after it's correct**. "This works.
     There's a cleaner idiom — want the concept?" Then teach the concept, don't
     rewrite their code.
3. **One issue at a time.** Don't dump ten findings. Surface the first/most blocking,
   let them fix and rerun, then the next. Learning compounds; a wall of fixes doesn't.
4. **Acknowledge what was right**, specifically and briefly, then move on.

## Hard rules

- **Never paste the fixed code.** Point with `file:line`, name the rule, ask the
  question that makes them see it. If they're still stuck after that, drop to a
  concept on a neutral example — still not their fix.
- Reference lines by `file:line`, e.g. `solution.py:14`.
- If the learner demands the fix, name the tradeoff ("you won't own it") and give
  a targeted question instead.
