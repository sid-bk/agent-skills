---
name: onboard
description: >-
  Investigates an unfamiliar codebase the way a staff engineer joining the project would, and produces a structured onboarding brief covering tech stack, architecture, services, entry points, one fully-traced request, external integrations, config/secrets handling, design patterns, conventions, a top-10-files-to-read list, and risk/debt flags — plus a one-page summary. Read-only: never edits or writes source code. Use when the user asks to onboard to, get oriented in, understand, or get an architecture walkthrough of a codebase or repo, or wants a new-engineer orientation doc.
---

# Onboard

Produce a staff-engineer-quality orientation to a codebase — understanding, not code changes.

## Scope

If it's not already obvious which repo/subproject to onboard onto (the user is in a
monorepo, or named more than one project), ask before starting. Default to the current
working directory's project if there's exactly one reasonable target.

## Step 1 — Cheap signal first

Before crawling source, check for and skim any of: `README.md`, `CLAUDE.md` /
`AGENTS.md`, `docs/architecture*`, `docs/overview*`, ADRs. These often answer stack,
architecture, and conventions directly and should seed (not replace) the investigation
below — verify their claims spot-check against actual code rather than trusting them
blind, since docs drift.

## Step 2 — Delegate the crawl

Spawn a read-only exploration subagent (its tool set excludes file-editing tools — the
right guardrail here, not just an instruction to be careful) with a single prompt
covering all of the following. Give it any doc findings from Step 1 as a head start.
For a large monorepo, spawn one exploration agent per major subproject/service in parallel
instead of one agent for everything.

Investigation prompt to give the subagent:

```
Investigate this codebase (or subproject at <path>) read-only and report back on:

1. Tech stack — languages, frameworks, and their versions (check lockfiles/manifests,
   not just imports).
2. System architecture — the overall shape (monolith / services / modules), how the
   pieces communicate.
3. Major services/apps/packages — one line each on what it does.
4. Entry points — where a process or request actually starts (main(), app factory,
   route table root, CLI entrypoint, worker loop).
5. One full representative request traced end-to-end — pick a realistic, non-trivial
   one (not health-check) and follow it from entry point through business logic to the
   database or terminal effect, citing file:line at each hop.
6. External integrations — every queue, cache, datastore, third-party API, message
   broker. Name the library/client used and where it's configured.
7. Config & secrets — how config is loaded (env vars, files, vault/KMS), where secrets
   are expected to live, what's git-ignored.
8. Dominant design patterns actually in use (not textbook patterns that don't appear).
9. Coding conventions and directory structure — the organizing logic, naming, where
   tests live.
10. Candidate "read first" files — the ones that unlock understanding of the rest,
    with one line each on why.
11. Technical debt / risk areas — TODO/FIXME/HACK density in load-bearing code, missing
    tests around critical paths, deprecated dependencies, anything the docs admit is
    debt, anything that looks fragile.

Cite file:line for concrete claims. Prefer reading targeted excerpts over whole files.
Do not modify anything — read-only investigation only.
```

## Step 3 — Synthesize

Combine subagent findings (merge per-service reports if you spawned more than one) into
one report using this structure, in this order:

1. **Tech stack** — table: component / language / framework / version.
2. **Architecture** — short prose + the shape (monolith/services/etc).
3. **Services / major components** — bullet list, one line each.
4. **Entry points** — file:line list.
5. **Traced request** — numbered hop-by-hop walkthrough with file:line at each step.
6. **External integrations** — table: system / client library / where configured.
7. **Config & secrets** — short prose.
8. **Design patterns** — bullet list, pattern name + where it shows up.
9. **Conventions & directory structure** — short prose + a directory tree sketch if it
   clarifies more than words would.
10. **Top 10 files to read first** — numbered, one line each on why.
11. **Debt / risk flags** — bullet list, most concerning first, each with a concrete
    location, not a vague impression.
12. **One-page onboarding summary** — a genuinely condensed standalone version of the
    above (stack, architecture in 2-3 sentences, the top-5 not top-10 files, the single
    biggest risk) that could be handed to a new hire on its own.

Keep the full report skimmable — headers, tables, short bullets over paragraphs. Cite
file:line wherever a claim is checkable.

## Step 4 — Deliver

Present the report inline. Offer (don't assume) to also save the one-page summary as a
file in the target repo (e.g. `docs/onboarding.md`) or publish it as a shareable page — do
either only if the user says yes.

## Constraint

No source file is edited or written during this skill, at any step. The exploration
subagent enforces this mechanically; do not work around it by making the edits yourself
after the subagent reports back.
