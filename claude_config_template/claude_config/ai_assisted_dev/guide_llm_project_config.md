---
tags: [ai, dev, guide, llm-config]
---

# LLM Project Configuration Document

> Feed this file to an AI assistant at the start of every project session. Fill in every section. Sections left blank will cause the AI to guess — and it will guess wrong.

---

## 1. Project Identity

**Project name:** [name]
**Description:** [One sentence. What does this system do and for whom?]
**Stage:** [Prototype / Alpha / Beta / Production]
**Primary language:** [e.g. Python 3.11, TypeScript 5.x]
**Runtime / platform:** [e.g. Node 20, Bun 1.x, browser-only, embedded Linux]

---

## 2. Tech Stack

List every dependency that affects how code should be written. Do not omit versions.

| Layer | Technology | Version |
|---|---|---|
| Language | | |
| Framework | | |
| Database | | |
| ORM / Query layer | | |
| Auth | | |
| Testing | | |
| Build tool | | |
| Linter / formatter | | |
| Deployment target | | |

**Constraints:**
- [e.g. "No external API calls — this runs fully offline"]
- [e.g. "No new dependencies without explicit approval"]
- [e.g. "Must run on Python 3.9 minimum"]

---

## 3. Architecture

**Pattern:** [e.g. MVC, layered, event-driven, serverless functions]

**Module structure:**
```
[paste your directory tree here]
```

**Key architectural rules:**
- [e.g. "All database access goes through repository classes. Never query the DB directly in a route handler."]
- [e.g. "Business logic lives in service/ only. Routes are thin — they validate input and call services."]
- [e.g. "All API responses use the standard envelope: { data, error, meta }"]

**What the AI must never change without explicit instruction:**
- [e.g. "The authentication middleware in src/middleware/auth.ts"]
- [e.g. "The database schema — no migration changes unless the task explicitly calls for it"]
- [e.g. "The public API contract — existing endpoint signatures are frozen"]

---

## 4. Ubiquitous Language

Define domain-specific terms. The AI should use these terms consistently and not invent synonyms.

| Term | Definition |
|---|---|
| [Term] | [What it means in this system specifically] |
| [Term] | [What it means in this system specifically] |

---

## 5. Coding Standards

**Naming conventions:**
- Variables: [e.g. camelCase]
- Files: [e.g. kebab-case]
- Classes: [e.g. PascalCase]
- Database tables/columns: [e.g. snake_case]
- Test files: [e.g. `*.test.ts` co-located with source]

**Code style rules:**
- [e.g. "Functions must not exceed 40 lines. Extract to helpers if they do."]
- [e.g. "No magic numbers. Use named constants."]
- [e.g. "Prefer explicit error handling over exceptions. Return Result types."]
- [e.g. "Comments only where the 'why' is non-obvious. No 'what' comments."]

**Module design:**
- Prefer deep modules: large blocks of functionality behind simple, clean interfaces. Avoid shallow modules (tiny functions with thin wrappers) — they fragment the codebase and make AI-assisted navigation harder.

---

## 6. Testing Protocol

**Framework:** [e.g. pytest, Jest, Vitest]
**Test location:** [e.g. `tests/` at root, co-located with source]

**Verification commands — run these before presenting code as complete:**
```bash
[e.g. bun run tsc --noEmit]
[e.g. bun run lint]
[e.g. pytest tests/ -v]
[e.g. bun test]
```

**Testing expectations:**
- [e.g. "Every new function must have at least one unit test"]
- [e.g. "Integration tests must hit a real database — no mocking the DB layer"]
- [e.g. "Test files must be runnable independently without side effects"]

---

## 7. Git and Branch Conventions

**Branch naming:** [e.g. `feat/`, `fix/`, `chore/`]
**Commit format:** [e.g. Conventional Commits: `feat(auth): add JWT refresh`]
**PR policy:** [e.g. "No direct commits to main. All changes via PR."]

---

## 8. Current Task Context

> Update this section at the start of each session. Do not leave stale context here.

**What we are building right now:** [describe the feature or fix in one paragraph]

**Files most relevant to the current task:**
- [path/to/file.ts — what it does]
- [path/to/file.ts — what it does]

**Decisions already made — do not revisit:**
- [e.g. "We chose X over Y because Z. This is settled."]

**Open questions — flag but do not resolve without discussion:**
- [e.g. "Unclear whether the retry logic should live in the service or the client layer"]

---

## 9. Operating Instructions for the AI

You are a collaborative engineering partner, not an autonomous agent. Follow these rules:

1. **Plan before you code.** When given a new task, draft a step-by-step implementation plan first. Do not write code until the plan is reviewed and approved.

2. **Stay in scope.** Only modify files and logic directly related to the current task. If you identify a problem in an adjacent module, flag it — do not fix it without instruction.

3. **Verify your output.** After writing code, run the verification commands listed in Section 6. Fix all errors before presenting the result.

4. **Respect the "do not touch" list.** Modules listed in Section 3 are off-limits unless the task explicitly overrides this.

5. **Explain non-obvious choices.** If you select a pattern, library, or approach that isn't specified above, state why. Do not silently introduce new dependencies.

6. **Flag contradictions.** If this document contradicts itself, or if the task conflicts with a stated architectural rule, surface that conflict before proceeding.

7. **Use the ubiquitous language.** Use the terms defined in Section 4 consistently. Do not introduce synonyms.

8. **Ask before assuming.** If the task is ambiguous or requires a decision not covered by this document, ask a clarifying question rather than guessing.
