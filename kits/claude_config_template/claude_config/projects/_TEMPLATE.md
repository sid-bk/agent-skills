# Project: <<project name>>

> Copy this file to `projects/<project-slug>.md` and fill it in.
> Load alongside CLAUDE.md + the relevant session file.

---

## Current Focus

> Update at the start or end of each session. Do not leave stale context here.

**What we are building right now:** <<...>>

**Blocked on:** <<...>>

**Decisions already made — do not revisit:**
- <<...>>

**Open — flag but do not resolve without discussion:**
- <<...>>

---

## What It Is

<<2–4 sentences: what the product/system does and for whom.>>

---

## Stack

| Component | Tool |
|---|---|
| Language / runtime | <<...>> |
| Framework | <<...>> |
| Data | <<...>> |
| Deployment | <<...>> |
| CI/CD | <<...>> |

---

## Project Structure

```
<<top-level dirs and what lives in each>>
```

---

## Commands

> Exact commands, run from the stated directory. Claude gives these to you to run and states the pass criteria; fill every line or write n/a.

| Purpose | Command | Pass means |
|---|---|---|
| Typecheck | <<e.g. `tsc --noEmit` / `uv run mypy src`>> | <<zero errors>> |
| Build | <<...>> | <<exit 0>> |
| Run all tests | <<...>> | <<all pass>> |
| Run one test | <<e.g. `uv run pytest path::name -q`>> | <<passes>> |
| Lint | <<...>> | <<zero findings beyond baseline>> |
| Format check | <<...>> | <<no diff>> |
| Format fix | <<...>> | <<files rewritten>> |

---

## Key Files

| File | Purpose |
|---|---|
| <<path>> | <<...>> |

---

## Known Patterns / Conventions

- <<recurring patterns, gotchas, things to always/never do>>

---

## Active Risks

| Risk | Severity | Mitigation |
|---|---|---|
| <<...>> | <<...>> | <<...>> |

---

## Open Decisions

| Decision | Status |
|---|---|
| <<...>> | Open / Closed (see memory/decisions.md) |

---

## Roadmap

<<target, task list location, critical path>>
