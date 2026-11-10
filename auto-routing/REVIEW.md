# Review: `auto-routing-draft.md`

> **Status:** addressed. `auto-routing-draft.md` rev 2 (2026-09-07) is a rewrite against these
> findings. This file is kept as the record of what rev 1 claimed, what was verified, and why it
> changed — the verification details behind rev 2's assertions live here, not there.

Reviewed 2026-09-07 against Claude Code **v2.1.236**
and the current model catalog. Findings marked **[verified]** were checked against the CLI's own
hook schemas / alias tables, not recalled.

**Verdict:** the subagent half of this spec is buildable and useful. The main-session half —
which is the headline feature — is not implementable as described. Two of the four hook
lifecycle points cannot do the job assigned to them, and `apply_mode: auto-write` has no
mechanism. Recommend splitting the document in two and rebuilding §"Hook-Based Implementation
Architecture" around `PreToolUse` + `updatedInput`, which is the one lever that actually works.

---

## Blocking

### B1. `UserPromptSubmit` cannot change the model **[verified]**

§Hook Lifecycle Points assigns this hook "makes initial model recommendation." A recommendation
is all it can make. The hook's output schema in v2.1.236 accepts exactly three fields:

```
hookEventName: "UserPromptSubmit"
  additionalContext        string, optional
  sessionTitle             string, optional
  suppressOriginalPrompt   bool,   optional   (only when decision == "block")
```

There is no model field, no effort field. The hook can inject text and it can block the prompt.
That is the entire surface. Everything in the spec that depends on classifying a prompt and
*acting* on it before the turn runs has to be re-scoped to "inject a sentence of advice."

### B2. `apply_mode: "auto-write"` cannot affect the running session **[verified]**

The config offers `auto-write`: "Automatically apply routing decision." The only writable
target is `settings.json`'s `model` key, and that key is read at startup. Observed directly in
this session — switching model while a settings pin was present printed:

> `.claude/settings.json` pins **Sonnet** — that applies on restart

So `auto-write` routes the *next* session, not this prompt. Either delete the mode, or rename
it and document the restart semantics honestly (`pin-next-session`). As written it promises the
central feature of the document and cannot deliver it.

### B3. `PreToolUse` + `updatedInput` is the one real mechanism — build on it **[verified]**

```
hookEventName: "PreToolUse"
  permissionDecision, permissionDecisionReason
  updatedInput             map<string, any>, optional
  additionalContext        string, optional
```

`updatedInput` lets the hook rewrite the tool's arguments, which means it can set `model` on an
`Agent` tool call before it spawns. This is real subagent routing and it works today. Three
corrections needed:

- The tool is **`Agent`**. The spec says "Agent and Task sub-agents" — `Task` is the old name and
  matching on it will silently no-op.
- **`subagent_type: "fork"` ignores a model override.** Forks always inherit the parent's model.
  The router must skip forks or it will log routing decisions that never took effect.
- **There is a no-hook alternative the spec should evaluate first:** agent definitions carry a
  `model:` (and effort) field in their `.claude/agents/*.md` frontmatter. For a fixed roster —
  Explore on Haiku, code-reviewer on Sonnet, tech-lead on Opus — that is declarative,
  version-controlled, reviewable in a PR, and has no failure mode. A hook is only justified if
  routing must vary by *prompt content* rather than by agent type. The spec should say why it
  needs the dynamic version.

### B4. `SubagentStart` exists and is a trap **[verified]**

v2.1.236 fires a `SubagentStart` hook (`agent_id`, `agent_type`). It looks like the natural
routing point and it is not — its output schema is `additionalContext` only. By the time it
fires the model is already bound. Worth an explicit "do not use this" note, because anyone
implementing from this spec will find it and try.

### B5. `PostToolUse` cannot "log actual model usage" **[verified]**

The base hook input carries `session_id`, `transcript_path`, `cwd`, `prompt_id`,
`permission_mode`, `agent_id`, `agent_type`, and `effort` — **no `model` field.** The telemetry
plan in §Metrics has no source.

Two working paths, both worth naming in the spec:
- Read the transcript at `transcript_path`.
- Join on `prompt_id` — the schema documents it as "the same value emitted on OpenTelemetry
  events as the `prompt.id` attribute, so hook output can be joined to OTel events at prompt
  grain." That is the intended route for exactly this use case.

---

## Factually wrong

### C1. The effort ladder is missing a rung, and the default is wrong **[verified]**

Actual levels: `low | medium | high | xhigh | max` (`claude --effort`). The spec omits **`xhigh`**.

That is not a trivia gap. `xhigh` sits between `high` and `max`, it is **the default in Claude
Code**, and it is the recommended setting for most coding and agentic work. The spec's
"**Medium:** Recommended default for balanced performance" and "⚠️ Avoid high/max for routine
work" both invert current guidance — the API default is `high`, and `high` is generally the
quality/token sweet spot rather than an extravagance. §Pattern 3 needs rewriting from scratch.

### C2. Haiku 4.5 does not support effort at all **[verified]**

`effort` errors on Haiku 4.5. Claude Code absorbs this silently — the hook schema describes its
`effort` field as the level "**after any silent downgrade for the selected model**."

Consequence: every `Haiku | Low` row in §Decision Framework is a no-op that will nonetheless
appear in logs as a successful routing decision. Any Haiku + effort pairing in the table is
decoration.

### C3. The cost argument is weaker than the spec assumes

Current list pricing, per MTok in/out:

| Model | Input | Output | Context |
|---|---|---|---|
| Opus 5 | $5 | $25 | 1M |
| Sonnet 5 | $3 | $15 | 1M |
| Haiku 4.5 | $1 | $5 | **200K** |

Opus is **1.67×** Sonnet, not an order of magnitude. A perfectly-tuned Opus→Sonnet router caps
out around 40% savings on the subset it moves, before the classifier's own cost. Haiku→Sonnet is
the 3× jump, and that's the tier where misrouting hurts capability most.

This doesn't kill the idea, but the spec currently leans on an implied cost cliff that isn't
there. State the real multiples, and note that **effort level and context size are the larger
levers** — a `max`-effort Sonnet turn can cost more than a `low`-effort Opus turn.

### C4. Haiku's 200K context is a correctness hazard, unmentioned

Opus 5 and Sonnet 5 are 1M; Haiku 4.5 is 200K. Routing a long-running session to Haiku for a
"quick lookup" (§Pattern 1's exact example) can put it over the window. The router needs a
context-size guard before any Haiku recommendation. Relatedly, the spec omits the `[1m]` alias
variants (`opus[1m]`, `sonnet[1m]`, `fable[1m]`) — relevant if context is a routing input.

### C5. Fable 5 and `best` are missing from the tier table **[verified]**

Valid aliases in v2.1.236: `sonnet, opus, haiku, fable, best, sonnet[1m], opus[1m], fable[1m],
opusplan`.

The spec's three-tier model predates Fable 5. §Task Classification's "**Extreme** — platform-scale
rewrites, migrations → Opus" is exactly the class where Fable 5 (or `best`, which resolves to the
most capable available family — currently `fable`, falling back to `opus`) is the honest answer.
Either add a fourth tier or say explicitly that Fable is out of scope and why.

### C6. "Opus: Slowest" ignores fast mode

Fast mode (`/fast`) runs Opus 5 at up to ~2.5× output tokens/sec at premium pricing. Latency is a
purchasable axis, not a fixed property of the tier. §Three Model Tiers presents speed as
inherent; a routing spec should treat it as a third dimension alongside model and effort.

### C7. Pin aliases, not model IDs **[verified]**

The CLI ships a versioned model catalog with `latest_per_family` and an `alias_migration` map,
and resolves `opus`/`sonnet`/`haiku` through it. A router config that stores concrete IDs
(`claude-opus-5`) silently rots on the next model release. The config schema should mandate
aliases. §Pattern 5 claims env-var pinning gives "prevention of silent failures on new model
releases" — pinning an *ID* produces the opposite.

### C8. Org model restrictions can silently override the router **[verified]**

The CLI has a `modelRestrictedWarning` path: orgs can restrict models via an `availableModels`
allowlist or `model_access` entitlement, and the CLI substitutes rather than fails (for
`opusplan` it warns and "planning uses the newest permitted Opus instead"). A router that
recommends a disallowed model gets quietly downgraded, and its logs will be wrong. Needs a
reconciliation rule and a "requested vs. actually resolved" check — §Safety Features claims to
log this, so make that claim load-bearing.

`opusplan` itself is still valid, so §Pattern 2 is fine — just note the restriction fallback.

---

## Internal contradictions

### D1. Three tables give three different answers for Implementation and Debugging

| Section | Implementation | Debugging |
|---|---|---|
| §Three Model Tiers | Sonnet ("daily coding, feature implementation, test writing") | Sonnet ("general debugging") |
| §Task Classification | **Opus** | **Opus** |
| §Decision Framework | **Sonnet** ("write function") | **Sonnet** ("debug test failure") |
| §Usage Examples | **Sonnet** (ex. 2) | Sonnet→Opus (ex. 4) |

Sonnet appears in **zero rows** of the six-class table — yet §Metrics lists "balanced
Sonnet/Opus split" as a success indicator, which that table makes impossible. Implementation and
debugging are also the two highest-volume classes, so this is where the whole routing policy
lives.

Pick one. §Task Classification is the table a classifier actually implements, so it's the one
that has to be correct, and the other three should be derived from it rather than restated.

### D2. Example 4 describes a mechanism that doesn't exist

"Sonnet→Opus (if complexity increases)" is mid-turn escalation. Nothing in the hook surface
supports it (see B1/B2). Either specify it concretely or delete the example — as written it sets
an expectation the implementation can't meet.

---

## Underspecified

- **E1. The classifier is the product, and it has no design.** "Uses local heuristics" is the
  entire specification of the thing this document exists to build. Needed before implementation:
  the signal list (keywords, prompt length, file counts, cwd, git state?), precedence when
  signals conflict, tie-breaking, the Abstain threshold, and a worked confusion matrix over ~30
  real prompts. Everything else here is scaffolding around this gap.

- **E2. The CLI fallback needs a latency and cost budget.** Spawning a Claude call to classify
  ambiguous prompts puts a model call on the hot path of every such prompt — and hooks block the
  turn. Against a ceiling of ~40% savings on a subset (C3), a classifier that fires often is
  plausibly net-negative on both cost and wall-clock. Specify: which fraction of prompts hit it,
  the timeout, what happens on timeout, and which model does the classifying (Haiku, presumably —
  say so).

- **E3. The `~` / `<` escape prefixes are poorly chosen.** `<` collides with redirect-shaped and
  XML/HTML-shaped prompts, both common. Pick a token unlikely to lead a real prompt, and specify
  whether the prefix is stripped before the model sees the text.

- **E4. "40-50% of tasks running on Haiku" is an invented target that rewards misrouting.** A
  router optimizing for that number will push work down-tier. Replace with an outcome metric:
  **escalation rate** — the fraction of down-routed turns the user manually re-ran on a larger
  model. That number is observable, it's the actual failure signal, and it can't be gamed by
  routing more aggressively.

- **E5. Config precedence is undefined.** `~/.claude/model-router.json` vs
  `.claude/model-router.json`: merge or override? Per-key or whole-file? And how does either
  interact with `ANTHROPIC_MODEL` / `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL`, which
  §Pattern 5 recommends for team pinning? Pattern 5 and the router are in direct tension —
  Pattern 5 exists to make model choice uniform and reproducible; the router exists to make it
  vary per prompt. The spec needs to say which wins and when.

---

## Suggested restructure

Split into two documents, because they have different feasibility:

**1. Subagent routing — buildable today.**
Start with the declarative version: `model:` in `.claude/agents/*.md` frontmatter, one line per
agent. Add the `PreToolUse` + `updatedInput` hook only for content-dependent routing, and only
after stating what the frontmatter version can't do. Skip `subagent_type: "fork"`. This is the
part of the spec that survives review intact, and it's also where the cost case is strongest —
subagents are high-volume, short-lived, and mostly mechanical.

**2. Main-session advice — advisory only, and say so on line one.**
`UserPromptSubmit` → `additionalContext` carrying the classification, so the model sees the
suggestion and can act on it or ignore it. Optionally a statusline nudge. No `auto-write`. Frame
it as "the router tells you what it would pick," which is honest and still useful.

Then rewrite the model/effort reference sections against current facts: five effort levels with
`xhigh` as the Claude Code default, Fable 5 and `best` in the tier table, real price multiples,
Haiku's 200K ceiling and its lack of effort support, and fast mode as a separate axis.
