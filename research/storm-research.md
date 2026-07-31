---
name: storm-research
description: Deep, multi-source research on a topic using the STORM method (perspective-guided simulated Q&A → outline → cited synthesis). Use when the user wants a thorough, well-sourced knowledge note on a topic from scratch — not a quick lookup. Produces a knowledge note with inline citations, confidence flags, and connections to existing notes. Invoke for "research X properly", "write me a deep dive on X", "STORM this topic", or building a literature map. For a single paper breakdown use a paper template instead.
---

# STORM Research

Adapts the **STORM** method (Synthesis of Topic Outlines through Retrieval and Multi-perspective question asking) to a personal knowledge vault. STORM writes long, grounded, encyclopedia-grade articles by (1) curating knowledge through *perspective-guided simulated conversations* between a writer and a source-grounded expert, then (2) turning that into an outline and a cited article. This skill runs that loop with real web retrieval and writes the result as a vault note.

Honour the vault's own guidelines and research conventions throughout: cite empirical claims, flag confidence (**established / contested / speculative**), surface contradictions with existing notes, connect to adjacent domains, and challenge weak reasoning in the sources. Final prose, not bullet soup.

---

## Arguments

Parse from the invocation; ask only if genuinely ambiguous, otherwise use defaults.

- **topic** (required) — what to research.
- **depth** — `quick` (3 perspectives, 2 Q&A turns each), `standard` (default: 5 perspectives, 3 turns), `deep` (7+ perspectives, 4+ turns, broader retrieval).
- **mode** — `auto` (default: run end-to-end, report at the end) or `co` (Co-STORM: pause at each phase for the user to steer — see §Co-STORM).
- **output** — target folder. Default: a research folder indexed by a research-index note. For a topic that clearly belongs to a domain, use a subfolder per domain. Split a multi-part topic into several linked notes rather than one sprawling note. Promoting settled takeaways into a distilled-knowledge layer or an essay is a separate, later step.

---

## Phase 0 — Scope & vault grounding

STORM surveys existing articles on similar topics to seed perspectives. Here the vault is the first corpus.

1. Restate the topic as a one-line research question. If it rests on a false premise or category error, fix the framing before proceeding.
2. Search the vault first: grep/glob across the knowledge, archive, and reference folders for what already exists on the topic and adjacent domains. Read the closest hits.
3. Note three things explicitly: what the vault already says, what it's missing, and any contradictions or unresolved questions living across notes. This becomes the gap map the research is meant to close — don't just re-derive what's already there.

## Phase 1 — Perspective discovery

Breadth comes from asking as different readers, not one.

1. Generate `N` distinct **perspectives** on the topic (N per depth). Each is a lens with a stake — e.g. for "solid-state batteries": a materials scientist, a grid-storage economist, an EV manufacturer, a safety regulator, a skeptic of the hype.
2. Seed at least one perspective from the Phase 0 gap map (the angle the vault is weakest on) and, for `deep`, one from a quick web survey of how the topic is typically structured (web-search the topic + "overview"/"controversies").
3. List the perspectives and the sub-questions each will pursue. In `co` mode, show these and let the user add/cut/reweight before continuing.

## Phase 2 — Knowledge curation (simulated conversation)

The core STORM loop. For **each perspective**, run a multi-turn dialogue where you play both roles:

- **Writer** (that perspective) asks a pointed question.
- **Expert** answers *only* from retrieved sources: run a web search, then fetch the most credible results to extract specifics. Never answer the expert turn from memory — if retrieval finds nothing, say so and move on.
- The writer asks a **follow-up** grounded in the previous answer (turns per depth). Follow-ups should dig into mechanism, evidence, numbers, and disagreement — not restate.

Maintain a running **source pool**: every claim you'll use, tagged with its URL and a confidence marker. Prefer primary sources, peer-reviewed work, and named authors over aggregators; note when a claim traces only to a weak source. Deduplicate overlapping findings across perspectives as you go.

Stop a perspective early when follow-ups stop yielding new information (saturation).

## Phase 3 — Outline

Organise the curated findings into a hierarchical outline (H2/H3) that covers the perspectives without redundancy. Order sections so the argument builds. In `co` mode, show the outline and take edits before writing. This outline is the note's spine.

## Phase 4 — Synthesis (cited write-up)

Write the note into the vault using the research deep-dive template (not the distilled knowledge-note template, which is for the settled-knowledge layer):

- Frontmatter: `tags: [research, deep-dive]`, today's `date`, `title`, `topic`, `status`, `confidence`, `perspectives` (the lenses used).
- **Core Idea** — 2–3 sentences, plain language.
- **Outline** — the spine the Detail follows (from Phase 3).
- **Detail** — the body, following the outline as prose. Every empirical claim carries an inline citation `[n]` mapping to the Sources list. Mark contested claims and note who disagrees; label speculation as such.
- **Confidence summary** — established / contested / speculative split.
- **Open Questions** — what the research didn't settle, including anything from the Phase 0 gap map still unanswered.
- **Contradicts / revises** — any existing vault note this finding conflicts with.
- **Sources** — numbered, matching inline `[n]`, with title + URL + a one-line note on credibility.
- **Connects to** — `[[wikilinks]]` to the existing vault notes found in Phase 0 and the adjacent domains (robotics ↔ space debris, AI ↔ synthetic-telepathy, etc.).

The template backlinks the research-index note, so the note appears on the research hub's dataview automatically.

Match the vault's voice: dense, analytical, prose over bullets, no filler preamble.

## Phase 5 — Polish & report

1. Dedup and tighten; ensure every citation resolves and every source is actually used.
2. Re-check confidence labels are present on empirical claims.
3. Explicitly surface any **contradiction** between the new findings and existing vault notes — that's high-value, don't bury it.
4. Report to the user: where the note was written, the confidence split (how much is solid vs contested vs speculative), and the 1–2 most important open questions.

---

## Co-STORM mode (`mode: co`)

Human-in-the-loop variant. Same pipeline, but collaborative:

- **Pause points**: after Phase 1 (perspectives), Phase 3 (outline), and before Phase 5. Present the state compactly and ask the user to steer, inject angles, or approve.
- **Moderator turn**: once per run, surface a *thought-provoking angle the retrieval turned up but no perspective pursued* — the overlooked thread. Ask if it's worth a detour.
- **Running mind map**: keep a live hierarchical outline of what's been learned and show the delta at each pause, so the user shares the conceptual map rather than just the output.

---

## Guardrails

- Retrieval-grounded, not memory-grounded: expert turns cite real fetched sources.
- One topic per run. If the topic is really several, say so and propose a split.
- Don't fabricate citations or inflate confidence. "Couldn't verify" beats a clean-looking false claim.
- The vault is a knowledge system, not a task manager — the deliverable is a durable, linked note, not a chat answer.

---

**Reference (source method):** STORM — Stanford OVAL. Paper: "Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models" (NAACL 2024). Project: <https://storm.genie.stanford.edu/>.
