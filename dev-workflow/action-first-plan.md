---
name: action-first-plan
description: Produce a concise, action-first plan for a new issue or task — goal, approach, next actions, first move, learning focus, done-when, watch-outs — balancing fast execution with first-principles understanding. Invoked as `/action-first-plan <task or issue>` or proactively when the user brings a new task, bug, ticket, or issue to scope. Stops at the plan; hands off to `/task-plan` only when the user prompts for it.
---

# Action-First Plan

Turn a new task into a short, actionable plan that favors rapid execution, first-principles
understanding, and curiosity-driven learning without analysis paralysis. This skill plans
only. It does not create branches, write code, or run anything, and it hands off to
`task-plan` when (and only when) the user asks.

## Trigger

- Explicit: `/action-first-plan <task or issue>`
- Implicit: the user brings a new issue, bug, ticket, or task and wants it scoped or broken down.

Scale to the task. A trivial task gets one direct next action, not the full template.

## Workflow

1. **DEFINE** — Desired outcome, acceptance criteria, constraints, highest-impact unknown.
   Separate essential requirements from optional improvements.
2. **TRIAGE** — Complexity, risk, reversibility, cost of failure.
   - Low risk / reversible: prototype immediately.
   - High uncertainty / costly rework: investigate critical assumptions first.
   - Security, safety, privacy, or financial correctness: validate rigorously before deployment.
3. **EXPLORE** — Minimum knowledge needed to begin. Research only what could materially
   change the next decision. Park tangential curiosities.
4. **ACT** — Small, concrete steps. Smallest experiment or implementation that yields
   useful evidence. Name the immediate next action.
5. **TEST** — How the result will be evaluated: acceptance criteria, inspect failures,
   separate observed facts from assumptions.
6. **UNDERSTAND** — Root causes and first principles when failures recur, results
   surprise, or deeper understanding materially improves later decisions.
7. **ITERATE** — Apply findings, retest, refine. Stop when acceptance criteria and
   necessary quality bars are met. Record reusable insights and open issues.

## Output format

For every new task, return exactly:

- **Goal:** what success looks like.
- **Approach:** recommended strategy and rationale.
- **Next actions:** three to five ordered, concrete steps.
- **First move:** the smallest useful action to take immediately.
- **Learning focus:** the key concept or unknown worth investigating, if any.
- **Done when:** explicit completion criteria.
- **Watch out for:** main risk, likely distraction, or scope-creep trap.

## Operating principles

- Explore → Build → Test → Understand → Improve.
- Prefer evidence over speculation, root causes over blind patches.
- Learn deeply where it creates transferable knowledge or reduces consequential risk.
- Time-box research and reversible decisions; never compromise necessary safety or correctness checks.
- Limit concurrent rabbit holes. Capture unrelated questions without pursuing them.
- Avoid unnecessary clarification: state reasonable assumptions and proceed when safe; ask
  only when missing information materially changes the plan.
- Do not confuse activity with progress. Every step produces a deliverable, evidence, or a decision.

## Handoff to task-plan

**Default: output the plan and stop.** End with one line saying `/task-plan #<task_id>
<short-title>` is the next step if the user wants to proceed to branch and review. Do not
invoke `task-plan` on your own.

**When the user prompts for it** ("go", "proceed", "task-plan it", "next", `/task-plan`,
or any clear ask to move on to the ticket workflow):

1. Invoke the `task-plan` skill.
2. Carry over the plan: pass the Goal as the issue description, the Approach as the planned
   fix, and the Watch-out as the consequences/risk input so `task-plan` does not re-derive them.
3. `task-plan` needs a `task_id` for the branch name. If the plan does not already have
   one, ask for it — do not invent one.
4. From there `task-plan` owns the flow (brief, step 3.5 Review Checklist, branch,
   implementation). This skill's Next actions become the implementation outline, not a
   replacement for that review pass.

## Rules

- Planning only: no `git`, no branch creation, no code, no test runs from this skill.
- Never skip or shortcut `task-plan`'s step 3.5 review because this skill already produced
  a plan. A plan from here is an input to that review, not a substitute.
- Never auto-chain. The handoff happens only on the user's prompt.
