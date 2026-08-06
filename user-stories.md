---
name: user-stories
description: Generate user stories and tickets for a project — either from an existing codebase (derive features and issues from code) or from a fresh use case description. Produces business-language user stories in Area/Value/Status/Description/Tasks/Acceptance Criteria format and bug/feature tickets with plain-language explanations and consequences. Invoke with "/user-stories" or when asked to "create user stories", "write tickets", or "create stories and tickets".
---

# user-stories — Generate user stories and tickets

## Trigger

Invoke when the user says: "create user stories", "write tickets", "generate stories and tickets for [project]", or "/user-stories".

## Modes

**Mode A — Codebase:** Given a directory, explore the code to derive what the system does, who uses it, what's implemented, and what's broken.

**Mode B — Fresh use case:** Given a written description of a system or feature set, create stories and tickets from that description without exploring code.

## Procedure

### Step 0 — Load existing context

1. Check if a codebase reference doc exists (e.g. `codebase.md` or a similarly named architecture reference). If it does, read it first — it maps the system's modules, routes, settings, and known issues. Skip re-exploring anything the reference already covers.
2. Check if `user_stories.md` or `tickets.md` already exist in the output location. If so, read them — update or extend rather than recreate from scratch.
3. Check if an issues doc exists. If so, read it — use it as the primary source list for ticket creation.
4. Determine the mode: if the user names a codebase directory, use Mode A. If the user provides a description only, use Mode B.

### Step 1 — Explore the codebase (Mode A only; skip if reference doc covers it)

Explore in this order — stop each section when you have enough to write stories:

1. **Entry points:** app factory, router mounts, middleware. Reveals what the system exposes.
2. **Models:** all model definition files. Reveals the data model and multi-tenancy structure.
3. **Routes / controllers:** all route/controller files. Every route = a feature or operation.
4. **Services / business logic:** skim service files for logic not visible from routes.
5. **Config / settings:** the configuration file. Reveals flags, integrations, and dangerous defaults.
6. **Issues:** any existing issues doc, known-debt sections in config files, or TODO comments.

Capture: personas (who can do what), feature map (what the system does), issue list (what's broken or missing).

### Step 2 — Derive personas

From the code (or use case description), identify the distinct user types. Common patterns:

- **Platform admin** — manages the whole platform across all tenants
- **Org / tenant admin** — manages one organization: members, billing, settings
- **End user / practitioner** — uses the core product day-to-day
- **Machine client / API integrator** — API-only, no human behind it; holds service credentials

Name personas in plain business language ("a clinic admin", "a clinician", "an API client") — not code identifiers or class names.

### Step 3 — Write user stories

Target 10–20 stories. Group by user goal, not by API endpoint or code module. If two endpoints serve the same user need, merge them into one story.

**Format for each story:**

```
## User Story N — [Title]
Area: [Feature area in plain language]
Value: Business
Status: Implemented | Partial | Planned

### Description
As a [persona], I need to [action] so that [outcome].

Tasks:
1. [Implementation task — may include technical, code-level detail]
2. ...

### Acceptance Criteria
1. [Verifiable outcome in plain language — non-developer readable]
2. ...
```

**Rules:**
- Description and Acceptance Criteria: plain business language — no class names, endpoint paths, or function references
- Tasks: may include technical references (files, endpoints, DB fields)
- "As a [persona]" — name a real human or system actor
- Acceptance criteria must be verifiable by a non-developer reading the product
- Status values:
  - `Implemented` — feature is live and working in the codebase
  - `Partial` — some implementation exists but acceptance criteria are not fully met
  - `Planned` — identified as needed but not yet in the code

**Count target:** Aim for ~15 stories. Too few hides real coverage; too many fragments into endpoint-level granularity. Merge ruthlessly — one story per user goal, not one per API call.

### Step 4 — Write tickets

**Bug tickets** — one ticket per confirmed defect, security risk, or broken behavior. Source from the issues doc or codebase review; never invent bugs.

```
### [PREFIX]-B## — [Short title]
Priority: P0 | P1 | P2 | P3
Type: Bug
Story: [User Story N reference, or N/A]

**What the problem is:** [1–2 sentences in plain English — what is wrong or missing, no jargon]
**Consequence if not fixed:** [what happens to users or the business if this is ignored]
**Technical detail:** [where the bug is, why it happens, what the fix looks like — technical detail]
Files: [path/to/file:line_number]
```

Priority guide:
- **P0** — data loss, active security breach, system completely down
- **P1** — major feature broken, compliance risk, significant data integrity issue
- **P2** — noticeable degradation, workaround exists
- **P3** — minor, cosmetic, low-frequency edge case

**Feature tickets** — one ticket per identified gap (capability needed but not yet implemented).

```
### [PREFIX]-F## — [Short title]
Priority: P1 | P2
Type: Feature
Story: [User Story N reference]

**What it is:** [plain-language description of the missing capability]
**Why it matters:** [business or user impact of the gap]
**Technical detail:** [what needs to be built or changed]
```

Numbering: use a short project prefix (e.g. `APP-B01`, `APP-B02` for bugs; `APP-F01` for features). Choose a prefix that matches the project's naming convention.

### Step 5 — Save output

- User stories → output directory as `user_stories.md`
- Tickets → output directory as `tickets.md`

If no codebase reference doc exists and the codebase is non-trivial, offer to create one as a fast re-entry file (architecture overview, route map, settings table, known issues summary). This prevents re-exploring the codebase on every future session.

Report: count of stories written, count of bug tickets and feature tickets, and any areas where story status was marked Partial or Planned.

## Rules

- Business language in stories and consequence fields; technical detail in tasks and ticket technical sections only
- Never invent features — stories must be derivable from code or the provided description
- Never invent bugs — tickets must reference observed code, not hypothetical issues
- Always include "What the problem is" and "Consequence if not fixed" in every bug ticket — these are for non-technical stakeholders who need to understand business impact
- Merge stories: 10–20 is the target range; never write one story per endpoint
- Do not re-explore codebase sections already covered by an existing reference doc — trust it and read source only for detail not covered there
- Mark Status accurately: do not mark Implemented if the code has missing fields, broken paths, or unmet acceptance criteria
- If updating existing files, preserve existing content and numbering — only add or revise, do not renumber unless explicitly asked
