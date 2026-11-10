# Auto-Routing for Claude Code: Model & Effort Selection

> Getting the right model and the right amount of reasoning onto each task — automatically where
> the harness supports it, declaratively where it doesn't, and advisory where neither works.

**Revision 2 (2026-09-07).** Rewritten after verifying rev 1's claims against Claude Code
**v2.1.236** and the current model catalog. See `REVIEW.md` for what was wrong and why. The
short version: rev 1 was built on a hook that cannot change models, and it ignored the
mechanisms that already do this job. Most of what it wanted already ships.

---

## The goal, restated

Minimize token spend without giving up output quality.

Rev 1 assumed the way to do that was to classify each prompt and pick a model. That is the
*least* reliable approach available, for a reason worth stating plainly:

**Task difficulty is not knowable from the prompt text.** "Fix the flaky test" is either a
two-minute fix or a two-day concurrency bug, and the prompt is identical in both cases. Any
keyword classifier accepts a misroute rate, and the cost of a misroute is asymmetric — routing
down when you should have routed up burns a whole session on a bad answer, which costs far more
than the tokens it saved.

So the ordering principle for this document is: **route on structure, not on prose.** Phase,
agent type, and command identity are known with certainty at routing time. Prompt semantics are
not. Every mechanism below is ranked by that criterion, and the highest-leverage ones require no
classifier at all.

---

## Corrected reference

### Models

| Model | Alias | Input $/MTok | Output $/MTok | Context | Effort support |
|---|---|---|---|---|---|
| Fable 5 | `fable` | $10 | $50 | 1M | `low`–`max` |
| Opus 5 | `opus` | $5 | $25 | 1M | `low`–`max` |
| Sonnet 5 | `sonnet` | $3 | $15 | 1M | `low`–`max` |
| Haiku 4.5 | `haiku` | $1 | $5 | **200K** | **none — errors, silently downgraded** |

Also valid: `best` (resolves to the most capable available family — currently Fable),
`opusplan`, and the 1M-context variants `opus[1m]`, `sonnet[1m]`, `fable[1m]`.

Three things rev 1 got wrong here, all load-bearing:

- **Opus is 1.67× Sonnet, not an order of magnitude.** A perfect Opus→Sonnet router saves ~40%
  on the subset it moves. Haiku→Sonnet is the 3× jump — and also the jump with real capability
  risk. The cost cliff rev 1 implicitly assumed does not exist.
- **Haiku's context window is 200K, not 1M.** Routing a long session down to Haiku for a "quick
  lookup" can overflow it. Any Haiku recommendation needs a context-size guard.
- **Haiku 4.5 does not accept an effort parameter.** Every `Haiku | Low` pairing is a no-op that
  still logs as a successful routing decision.

**Pin aliases, not model IDs.** The CLI carries a versioned model catalog with `latest_per_family`
and an `alias_migration` map. Config that stores `claude-opus-5` rots on the next release; config
that stores `opus` does not.

### Effort

`low | medium | high | xhigh | max`. Rev 1 omitted `xhigh` and named `medium` the recommended
default; both are wrong. The API default is `high`, **Claude Code's default is `xhigh`**, and
`xhigh` is the recommended setting for most coding and agentic work. `high` is generally the
quality-per-token sweet spot. Reserve `max` for correctness-critical work, `low` for subagents
and mechanical tasks.

Rev 1's "⚠️ avoid high/max for routine work" is inverted and should not survive into
implementation.

---

## What is already automatic

These four ship today. Together they cover most of what rev 1 set out to build, and the first
three need no code.

### 1. Adaptive thinking + effort — the actual token router

This is the mechanism rev 1 never mentioned and it is the largest lever in the document.

Adaptive thinking already varies reasoning tokens per turn according to how hard the turn is.
Effort sets the ceiling on that. The CLI's own model catalog carries an `effort_cost_index` —
a per-model, per-level cost multiplier — which is as direct an admission as you could want that
this is the intended cost dial.

Why it dominates model routing on the quality-risk axis: it varies spend **inside one model**.
The failure mode of dropping effort is "thought less about it." The failure mode of dropping
model is "is less capable." Those are not comparable risks, and the spend swing from `low` to
`max` within a single model is larger than the swing from Sonnet to Opus.

**Action:** before building any router, set effort deliberately and stop there for a week.
`high` for normal work, `xhigh` for hard agentic work, `low` for mechanical turns. Measure. Most
of the available savings are here.

### 2. Phase routing via `opusplan` and `haiku` — built-in, verified

Both of these aliases already auto-switch model by phase:

| Alias | Plan mode | Execution |
|---|---|---|
| `opusplan` | Opus | Sonnet |
| `haiku` | **Sonnet** | Haiku |

The `haiku` alias having a plan-mode upgrade is undocumented in most write-ups and is the more
interesting of the two: `/model haiku` is not a flat pin, it is a router that puts the design
decisions on Sonnet and the mechanical execution on Haiku.

This is complexity-based routing that already works, and it routes on the single best available
proxy for difficulty — **phase**. Planning is where the hard reasoning lives; execution is where
the token volume lives. That correlation is structural and doesn't depend on guessing anything
from prompt text.

Caveat: org model restrictions (`availableModels` allowlist / `model_access` entitlement) can
block the upgrade model, in which case the CLI warns and substitutes the newest permitted model
in that family rather than failing.

### 3. Declarative per-agent routing — `model:` + `effort:` frontmatter

Agent definitions (`.claude/agents/*.md`) accept both:

```yaml
---
name: explore
model: haiku          # haiku | sonnet | opus | fable | <full ID> | inherit
effort: low           # low | medium | high | max | <integer>
---
```

Slash commands accept `model:` in their frontmatter too.

This is where the volume is. Subagents are numerous, short-lived, and mostly mechanical, and
their type is known with certainty before they spawn — no classification required. A sensible
default roster:

| Agent | Model | Effort | Why |
|---|---|---|---|
| Explore / search | `haiku` | — | Pattern matching over files; no reasoning to lose |
| general-purpose | `sonnet` | `medium` | Bounded, well-specified work |
| code-reviewer, qa | `sonnet` | `high` | Judgment, but scoped to a diff |
| tech-lead, architect | `opus` | `high` | System-wide tradeoffs |

Versioned, reviewable in a PR, no runtime failure mode, no hook. **Start here.** Rev 1's
subagent section proposed a hook to do what frontmatter already does declaratively.

Note the frontmatter `effort` field documents `low|medium|high|max|<integer>` — it does not list
`xhigh`, unlike the session-level enum. Verify before relying on `xhigh` in an agent file.

### 4. `--fallback-model` — availability routing

`--fallback-model <a,b,c>` switches automatically when the primary is overloaded or unavailable,
tries each in order, and **re-tries the primary at the start of each user turn**. Fallback events
surface as `model_fallback` system messages with a `trigger` of `model_not_found`,
`permission_denied`, `overloaded`, `server_error`, `last_resort`, or `model_blocked`.

This is availability-driven, not complexity-driven — but it's automatic model assignment, it's
observable, and any router you build has to reconcile with it or its logs will be wrong.

---

## What can be built

### 5. Dynamic subagent routing — `PreToolUse` + `updatedInput`

The one hook mechanism that genuinely changes a model. `PreToolUse` output accepts:

```
permissionDecision, permissionDecisionReason
updatedInput        map<string, any>   ← rewrite the tool's arguments
additionalContext
```

Matching on the **`Agent`** tool, the hook can rewrite the spawn's `model` before it runs.

Constraints:
- The tool is **`Agent`**. `Task` is the old name; matching it silently no-ops.
- **`subagent_type: "fork"` ignores model overrides** — forks always inherit the parent. Skip
  them or you'll log routing that never happened.
- Only worth building if routing must vary by *prompt content* rather than by agent type. If it
  varies by agent type, use frontmatter (§3) — it's strictly better.

### 6. True per-prompt routing — external supervisor via `set_model`

The only way to get real prompt-level automatic model assignment. It is not a hook; it's a
parent process driving Claude Code in stream-json mode and issuing control requests:

| Control request | Effect |
|---|---|
| `set_model` | "Sets the model to use for **subsequent conversation turns**." Omit / `null` / `"default"` resets to the session default. |
| `list_models` | Enumerate available models programmatically |
| `set_max_thinking_tokens` | Thinking budget + `thinking_display` |
| `get_settings` | Effective merged settings, per source, plus `applied.model` / `applied.effort` |

Loop: read the user's turn → classify → `set_model` → forward the turn.

Honest assessment: this is a real architecture and it is the only thing that delivers rev 1's
headline promise. It is also a whole harness to own, it moves you off the normal Claude Code
entry point, and it buys you a routing axis worth ~40% on a subset — after §1–§3 have already
taken most of the savings. **Build it last, if at all.**

`set_model` applies from the *next* turn, so a supervisor must classify before forwarding, never
mid-turn.

### 7. Main-session advice — `UserPromptSubmit`, advisory only

`UserPromptSubmit` output accepts exactly `additionalContext`, `sessionTitle`, and
`suppressOriginalPrompt`. No model field, no effort field. It can inject text or block the
prompt. That's all.

Used honestly, that's still useful: inject the classification as context so the assistant sees
"this looks mechanical; consider `/model haiku`" and can act or ignore. Pair with a statusline
indicator. **No `auto-write`.**

---

## What is not possible

State these up front in any implementation, because each one looks buildable until you try:

| Attempt | Why it fails |
|---|---|
| `UserPromptSubmit` switches the model for this turn | Output schema has no model field |
| Hook writes `settings.json` to route the live session | The `model` key is read at startup — it applies on restart |
| `SubagentStart` routes the subagent | Fires *after* the model is bound; output is `additionalContext` only |
| `PostToolUse` logs which model ran | Hook input carries no `model` field (see Measurement) |
| Mid-turn escalation Sonnet→Opus when it gets hard | No mechanism at any lifecycle point |

---

## Configuration

**Precedence is defined by the harness**, low to high:

```
userSettings  <  projectSettings  <  localSettings  <  flagSettings  <  policySettings
```

`get_settings` reports both the merged result and each source, plus `applied.effort` — the level
that will actually be sent "after env overrides, session state, org caps and model-support
downgrades." That last clause is how you detect the Haiku effort downgrade rather than guessing.

Any router config should follow the same five-layer precedence rather than inventing its own
user-vs-project merge rule.

**Reconcile with env pinning.** `ANTHROPIC_MODEL` and
`ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL` pin models for team consistency; org
restrictions can override anything. A router and a team pin want opposite things — the pin wants
uniformity, the router wants variance. Decide which wins and write it down; don't leave it to
whichever runs last.

---

## Measurement

Hook input carries `session_id`, `transcript_path`, `cwd`, `prompt_id`, `permission_mode`,
`agent_id`, `agent_type`, and `effort` — **but not `model`.** Two working sources:

- Read the transcript at `transcript_path`.
- Join on `prompt_id`, documented as "the same value emitted on OpenTelemetry events as the
  `prompt.id` attribute, so hook output can be joined to OTel events at prompt grain." This is
  the intended path.

**Track escalation rate, not tier distribution.** Rev 1's "40–50% of tasks on Haiku" is an
invented target that a router can satisfy by misrouting more aggressively. The metric that
matters is the fraction of down-routed turns the user manually re-ran on a larger model — it's
observable, it's the actual failure signal, and it cannot be gamed by routing harder.

Secondary: requested vs. actually-resolved model (catches org restrictions and
`model_fallback`), and tokens per completed task rather than per turn.

---

## Rollout

Ordered by leverage per unit of risk. Each step is independently useful; stop whenever the
savings stop justifying the work.

1. **Set effort deliberately** — `high` default, `xhigh` for hard agentic work, `low` for
   mechanical. Zero build. Largest single lever.
2. **Adopt a phase-routing alias** — `opusplan`, or `haiku` for mechanical-heavy sessions. Zero
   build, already automatic, routes on a structural signal.
3. **Set `model:` and `effort:` in agent frontmatter** — one line per agent, version-controlled.
   This is where the subagent volume is. Zero runtime risk.
4. **Measure for two weeks** — escalation rate and tokens per completed task, before and after.
   If steps 1–3 got you most of the way, the rest of this document is not worth building.
5. **Advisory `UserPromptSubmit` hook** — if you still want per-prompt intelligence, get the
   classifier's judgment in front of you as text first. It costs nothing to ignore a suggestion,
   and a few weeks of watching it be wrong is the cheapest possible classifier evaluation.
6. **`PreToolUse` dynamic subagent routing** — only if routing must vary by content, not by agent
   type.
7. **External supervisor with `set_model`** — only if steps 1–6 left real money on the table and
   you're willing to own a harness.

---

## If a classifier does get built

Rev 1 left the classifier — the actual product — specified as "uses local heuristics." Minimum
before implementation:

- **Signals**, explicitly: keywords, prompt length, referenced file count, cwd, git state.
- **Precedence** when signals conflict, and tie-breaking.
- **Abstain threshold** — and abstain should be the *common* case, not the exception. A router
  that abstains 60% of the time and is right the other 40% beats one that always fires.
- **A confusion matrix over ~30 real prompts** from your own history, hand-labeled. Build this
  first; if the heuristics can't clear it on prompts you've actually written, the hook is moot.
- **A latency and cost budget for the CLI fallback.** Hooks block the turn, so a model call on
  the classification path adds latency to every ambiguous prompt and cost against a ceiling of
  ~40% savings on a subset. Specify the classifying model (Haiku), the timeout, what happens on
  timeout, and what fraction of prompts are expected to hit it. It is entirely possible for this
  to be net-negative on both axes.
- **A skip prefix that isn't `<`** — it collides with redirect-shaped and XML-shaped prompts,
  both common. Specify whether the prefix is stripped before the model sees the text.
- **Errors fail open.** Rev 1 got this right; keep it.

---

## References

- `REVIEW.md` — the rev 1 findings this revision is based on, with verification details
- Model Selection Guide: https://dev.to/klement_gunndu/pick-the-right-claude-code-model-for-every-task-1p6a
- Model Router Hook reference: https://github.com/tzachbon/claude-model-router-hook
  *(third-party; verify its hook assumptions against the schemas above before adopting)*
