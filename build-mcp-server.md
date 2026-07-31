---
name: build-mcp-server
description: Use when the user asks to "build an MCP server", "create an MCP", "make an MCP integration", "wrap an API for an agent", "expose tools to an assistant", "make an MCP app", or discusses building something with the Model Context Protocol. Entry point for MCP server development — interrogates the use case, determines the right deployment model (remote HTTP, bundled local, local stdio), picks a tool-design pattern, and hands off to specialized skills.
---

# Build an MCP Server

You are guiding a developer through designing and building an MCP server that works with any MCP-compatible host (AI assistants, agent runtimes, IDEs). MCP servers come in many forms — picking the wrong shape early causes painful rewrites later. Your first job is **discovery, not code**.

> **Verify against the spec.** The MCP specification evolves. Confirm details of auth types, transports, and capability negotiation against the live spec at <https://modelcontextprotocol.io> and your target host's connector documentation before scaffolding. Different hosts add their own auth types, review criteria, and limits on top of the generic spec.

Do not start scaffolding until you have answers to the Phase 1 questions. If the user's opening message already answers them, acknowledge that and skip to the recommendation.

---

## Phase 1 — Interrogate the use case

Ask these conversationally (batch them into one message). Adapt to what the user already told you.

### 1. What does it connect to?

| If it connects to… | Likely direction |
|---|---|
| A cloud API (SaaS, REST, GraphQL) | Remote HTTP server |
| A local process, filesystem, or desktop app | Bundled local or local stdio |
| Hardware, OS-level APIs, or user-specific state | Bundled local |
| Nothing external — pure logic / computation | Either — default to remote |

### 2. Who will use it?

- **Just me / my team, on our machines** → Local stdio is acceptable (easiest to prototype)
- **Anyone who installs it** → Remote HTTP (strongly preferred) or bundled local (if it *must* be local)
- **Users who want UI widgets** → MCP app (remote or bundled local)

### 3. How many distinct actions does it expose?

This determines the tool-design pattern — see Phase 3.

- **Under ~15 actions** → one tool per action
- **Dozens to hundreds of actions** (wrapping a large API surface) → search + execute pattern

### 4. Does a tool need mid-call user input or rich display?

- **Simple structured input** (pick from list, enter a value, confirm) → **Elicitation** — spec-native, zero UI code. Host support is uneven — always pair with a capability check and fallback.
- **Rich/visual UI** (charts, custom pickers with search, live dashboards) → **MCP app widgets** — iframe-based. See the `build-mcp-app` skill.
- **Neither** → plain tool returning text/JSON.

### 5. What auth does the upstream service use?

- None / API key → straightforward
- OAuth 2.0 → you'll need a remote server with dynamic client registration (or an equivalent client-metadata flow)

---

## Phase 2 — Recommend a deployment model

Recommend **one** path. Be opinionated.

### ⭐ Remote streamable-HTTP MCP server (default recommendation)

A hosted service speaking MCP over streamable HTTP. Recommended for anything wrapping a cloud API.

**Why it wins:** zero install friction (users add a URL); one deployment serves all users; OAuth flows work properly (the server handles redirects, registration, token storage); works across any MCP host.

**Choose this unless** the server *must* touch the user's local machine.

- **Fastest deploy:** a serverless edge platform (e.g. Cloudflare Workers) — zero to live URL in a couple of commands.
- **Portable Node/Python:** an Express or FastMCP scaffold that runs on any host.

### Elicitation (structured input, no UI build)

If a tool just needs the user to confirm, pick an option, or fill a short form, elicitation does it with zero UI code. The server sends a flat JSON schema; the host renders a native form.

**Caveat:** host support is uneven. The SDK throws if the client doesn't advertise the capability — always check for `elicitation` in client capabilities first and have a fallback. Escalate to widgets when you need nested data, scrollable/searchable lists, visual previews, or live updates.

### MCP app (remote HTTP + interactive UI)

Same as remote, plus **UI resources** — interactive widgets rendered in the chat surface. Rich pickers, charts, live dashboards. Built once, renders in any host that implements the apps surface.

**Choose this when** elicitation's flat-form constraints don't fit. → Hand off to the **`build-mcp-app`** skill.

### Bundled local server

A local MCP server **packaged with its runtime** so users don't need Node/Python installed. The sanctioned way to ship local servers.

**Choose this when** the server *must* run on the user's machine. → Hand off to the **`build-mcpb`** skill.

### Local stdio (npx / uvx) — *not recommended for distribution*

A script launched via `npx` / `uvx`. Fine for **personal tools and prototypes**. Painful to distribute: users need the right runtime and you can't push updates. Recommend only as a stepping stone; note the bundled-local upgrade path.

---

## Phase 3 — Pick a tool-design pattern

How you carve tools matters more than most expect — tool schemas land directly in the model's context window.

### Pattern A: One tool per action (small surface)

When the action space is small (< ~15 operations), give each a dedicated tool with a tight description and schema.

```
create_issue    — Create a new issue. Params: title, body, labels[]
update_issue    — Update an existing issue. Params: id, title?, body?, state?
search_issues   — Search issues by query string. Params: query, limit?
add_comment     — Add a comment to an issue. Params: issue_id, body
```

**Why it works:** the model reads the tool list once and knows exactly what's possible. No discovery round-trips.

### Pattern B: Search + execute (large surface)

When wrapping a large API (dozens to hundreds of endpoints), listing every operation floods the context window and degrades model performance. Expose **two** tools:

```
search_actions  — Given a natural-language intent, return matching actions
                  with their IDs, descriptions, and parameter schemas.
execute_action  — Run an action by ID with a params object.
```

The server holds the full catalog internally. The model searches, picks, executes. **Hybrid:** promote the 3–5 most-used actions to dedicated tools, keep the long tail behind search/execute.

---

## Phase 4 — Pick a framework

| Framework | Language | Use when |
|---|---|---|
| **Official TypeScript SDK** (`@modelcontextprotocol/sdk`) | TS/JS | Default choice. Best spec coverage, first to get new features. |
| **FastMCP** (`fastmcp` on PyPI) | Python | User prefers Python, or wrapping a Python library. Decorator-based, low boilerplate. |

Both produce identical wire protocol — if the user already has a stack in mind, go with it.

---

## Phase 5 — Scaffold and hand off

Once the four decisions are settled (deployment model, tool pattern, framework, auth), do **one** of:

1. **Remote HTTP, no UI** → scaffold inline (portable Express/FastMCP or the fastest-deploy edge scaffold).
2. **MCP app (UI widgets)** → summarize the decisions, then load the **`build-mcp-app`** skill.
3. **Bundled local** → summarize the decisions, then load the **`build-mcpb`** skill.
4. **Local stdio prototype** → scaffold inline, flag the bundled-local upgrade path.

When handing off, restate the design brief in one paragraph so the next skill doesn't re-ask.

---

## Beyond tools — the other primitives

Tools are one of several server primitives. Most servers start with tools and never need the others:

| Primitive | Who triggers it | Use when |
|---|---|---|
| **Resources** | Host app | Exposing docs/files/data as browsable context |
| **Prompts** | User (slash command) | Canned workflows ("/summarize-thread") |
| **Elicitation** | Server, mid-tool | Asking user for input without building UI |
| **Sampling** | Server, mid-tool | Need LLM inference in your tool logic |

---

## Phase 6 — Test and publish

1. **Test against a real host** by adding the server URL as a custom connector (use a tunnel for local servers). Confirm capability negotiation and tool calls work end-to-end.
2. **Run a pre-submission checklist** — read/write tool split, required annotations, name limits, prompt-injection rules — per your target host's review criteria.
3. **Submit to your target host's connector directory** if it has one.
4. Consider shipping a **plugin/extension** that wraps this MCP with skills — many integrations ship both.

---

## Quick reference: decision matrix

| Scenario | Deployment | Tool pattern |
|---|---|---|
| Wrap a small SaaS API | Remote HTTP | One-per-action |
| Wrap a large SaaS API (50+ endpoints) | Remote HTTP | Search + execute |
| SaaS API with rich forms / pickers | MCP app (remote) | One-per-action |
| Drive a local desktop app | Bundled local | One-per-action |
| Local desktop app with in-chat UI | MCP app (bundled local) | One-per-action |
| Read/write local filesystem | Bundled local | Depends on surface |
| Personal prototype | Local stdio | Whatever's fastest |

---

**References (sources):** Model Context Protocol spec — <https://modelcontextprotocol.io>; `@modelcontextprotocol/sdk`; FastMCP (PyPI).
