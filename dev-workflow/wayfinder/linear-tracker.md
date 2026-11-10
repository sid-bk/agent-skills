# Wayfinder tracker: Linear

How this installation of `/wayfinder` expresses the map, tickets, blocking, and frontier queries described in `SKILL.md`, using Linear as the issue tracker. Read this alongside `SKILL.md`, not instead of it — this file only fills in the "tracker-specific" gaps that skill deliberately leaves open.

**Default workspace/team:** set your own Linear workspace and team here (written below as `<your-team>`), accessed via the Linear MCP tools. If a repo's own tracker doc names a different Linear team (or a different tracker entirely), that doc wins — this is the fallback, not an override.

**Project scope is per-map, not fixed.** A map can float at team level (no project) if it's scoping work that doesn't have a home yet, or attach to an existing Linear Project (`project:` param on `save_issue`/`save_project`) if the effort is bounded to one. Decide this once, when charting — don't move a map between projects mid-effort.

---

## Wayfinding operations

### The map

A Linear **issue**, `save_issue(title: <destination name>, team: "<your-team>", labels: ["wayfinder:map"])`. Its `description` field **is** the map body — the template from `SKILL.md`'s "The map body" section, written directly into the issue description and kept current there (via `patch`, not full rewrites, once it's non-trivial in size).

The map is discoverable later by `list_issues(label: "wayfinder:map", team: "<your-team>")` or by URL/number if the user names it.

### Tickets

Child issues: `save_issue(title: <question, action-oriented>, team: "<your-team>", parentId: <map issue id>, labels: ["wayfinder:<type>"])`, where `<type>` is one of the four labels below (provision them in the workspace once, before first use):

| Skill's ticket type | Linear label |
|---|---|
| Research | `wayfinder:research` |
| Prototype | `wayfinder:prototype` |
| Grilling | `wayfinder:grilling` |
| Task | `wayfinder:task` |

A ticket's `description` is the `## Question` body from `SKILL.md`'s "Tickets" section — the question, not the answer.

List a map's tickets: `list_issues(parentId: <map issue id>, includeArchived: false)`.

### Claiming

`save_issue(id: <ticket>, assignee: "me")`, done **before** any other work on the ticket — this is the skill's own claim mechanism, and Linear's native `assignee` field is exactly it. An open ticket with `assignee: null` is unclaimed.

### Blocking

Linear's **native** issue relations — exactly what the skill asks for ("essential because it renders the frontier visually in the tracker's own UI"):

- `save_issue(id: <blocked ticket>, blockedBy: [<blocking ticket ids>])`
- Equivalently from the other side: `save_issue(id: <blocking ticket>, blocks: [<blocked ticket ids>])`

Both are append-only per the tool schema — removing a relation needs `removeBlockedBy`/`removeBlocks` explicitly. Wire these in the **second pass** the skill describes (create every ticket first so ids exist, then wire).

### Frontier query

The frontier is: open, unblocked, unassigned children of the map. No single list call returns exactly this, so compose it:

1. `list_issues(parentId: <map issue id>, state: <not Done/Canceled>)` — open children.
2. Drop any with a non-null `assignee`.
3. For what's left, call `get_issue(id: <ticket>, includeRelations: true)` and drop any whose `blockedBy` relations aren't all in a Done/Canceled state.

What survives is the frontier. In practice, the Linear UI's own blocked-issue indicator (visible on the map's sub-issues panel or a filtered view) shows this at a glance without re-running the query every session — use the API path when driving this headlessly, the UI when a human's looking at the same board.

### Recording a resolution

On resolving a ticket:

1. `save_comment(issueId: <ticket>, body: <the resolution — the answer, not a summary of the discussion>)` — this is the skill's "resolution comment."
2. `save_issue(id: <ticket>, state: "Done")`.
3. Patch the map issue's description, appending one line under `## Decisions so far`: `- [<ticket title>](<ticket url>) — <one-line gist>`. Use `save_issue(id: <map>, patch: [{op: "insert_after", anchor: "## Decisions so far", text: "\n- [...](...) — ..."}])` (or the nearest existing bullet as the anchor once the section is non-empty) rather than resending the whole description.

### Assets

Link, don't paste: `save_issue(id: <ticket>, links: [{url: <asset url>, title: <asset name>}])` for anything created while resolving a ticket (a doc, a prototype, a branch) — matches the skill's "Assets created while resolving a ticket are linked from the issue, not pasted in."

### Fog, scope, and everything else

Not tracker-specific — `## Not yet specified` and `## Out of scope` are just sections of the map issue's description, edited the same way as `## Decisions so far`. `SKILL.md` already covers when content moves between them; nothing about Linear changes that.
