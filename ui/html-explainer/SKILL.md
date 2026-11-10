---
name: html-explainer
description: >-
  Turn a codebase, feature, flow, pipeline, schema, document, paper or the current session into a single self-contained, well-designed interactive HTML explainer, with a blocking fact-check before delivery. The default output for anything with a flow is a stage walkthrough: a vertical flowchart with one row per step, real code excerpts with file:line, a (?) pop-up of deeper detail per step, an interactive playground that reruns a core computation on real fixtures, and a "where things stand" section. Use when the user asks to explain, walk through, trace, visualize or summarize something as a shareable HTML page, or says "walkthrough", "explainer", "explain this flow", "explain the architecture", "explain the schema", "turn this into an HTML page". Not for plain-text answers, slide decks or dashboards of live data.
---

# HTML Explainer

Produce one standalone `.html` file that gives a reader a correct mental model fast: concepts and connections first, real code as evidence, deeper detail one click away, and an honest account of what is built and what is not.

**Reference implementation:** `reference/stage-walkthrough.html` in this skill's folder. It is the target look and structure for the default mode. Read it in full before building a stage walkthrough, reuse its CSS tokens, layout classes and JavaScript (stage observer, stepper, dialog, playground pattern), and replace every piece of content. Never copy its project-specific text, numbers or paths into a new page.

## Step 0: Pick the mode

Choose from the request, and ask one question only if it is genuinely ambiguous.

| Mode | Use when | Output shape |
|------|----------|--------------|
| Stage walkthrough (default) | How does X work, trace a flow, a pipeline, architecture, a request path, a batch job, any system with an order of steps | Vertical flowchart, one row per stage with brief, node and Reads / Code / Hands on / Watch cards, a (?) pop-up per stage, a playground, a status section |
| Schema | A database schema or data model with no meaningful order | Same page shell and theme; the flowchart column becomes entity rows (one row per entity or table group), with the (?) pop-up per entity |
| Article | Paper, blog post, transcript, research topic, or a deep-dive on one idea | Distill-style long-form page, sticky two-column layout, hand-built figures |
| Summary | Session history or a markdown doc to share with stakeholders | Top-down structured page (meeting, RFP, API spec, status update) |

A bare "walkthrough" or "explainer" with no topic means a stage walkthrough of the whole project's main flow.

## Step 1: Intake (never skip, never invent)

- **Pin the source.** For a repo, record the branch and `git log -1 --oneline` at the start. Check it again before delivery: if it moved, diff the files the page cites and update the page. The commit goes in the footer and the design record.
- **Codebase:** do one or two quick searches, then launch 2-4 parallel read-only explore subagents, each owning a slice of the flow (for example: contract and loading; evaluation and branches; output, persistence and tests). Each returns node reports: purpose, inputs and outputs, a camelCase id, a plain-English label, file paths with line numbers, and a 1-5 line verbatim snippet with its exact `path:line` range. Ask them to mark anything inferred, and to report surprises (things not built, docs that disagree with code, config that is never read).
- **Subagent reports are leads, not facts.** Before a claim goes on the page, the main agent opens the cited lines itself. Subagents miscount (templates, tests, rule totals) and read files that have since changed.
- **Fixtures:** find the real test fixtures, golden cases or worked examples for the core computation. They feed the playground.
- **Documents or papers:** read the actual files. Research topics: gather sources with search and fetch, and open each source. Session summary: work from the conversation history, and leave the original source untouched.
- Never fabricate code paths, snippets, quotes or numbers. If it was not read, it is not in the page.

## Step 2: Synthesize (stage walkthrough)

- **Stages:** 6-12 rows in run order, numbered `01`, `02`, … Each stage is one concept a newcomer can hold ("A ruleset version becomes effective", "Hard stops first"), not one file.
- **One fork at most:** where parallel paths share an input and rejoin, use a three-lane fork (`06a`, `06b`, `06c`); two lanes is fine too. A path that exists in the contract but carries nothing today gets a dashed lane and a dashed node.
- **Side rails:** up to two vertical rails beside the spine for cross-cutting paths. Typical: a solid red rail on the left for a bypass (a hard-stop path that skips scoring), a dashed grey rail on the right for something every stage reads (frozen config) or a loop back to the start. Each rail has a short vertical label.
- **Per stage:**
  - Brief (left): big mono stage number, a 3-7 word heading, 2-4 sentences in plain language, an optional small muted note.
  - Node (centre): a clickable box with a bold name, a one-line role and the main file in mono. Colour by role: data blue, checks violet, score accent, use green, bypass red, gap dashed grey.
  - Cards (right), each with a coloured left border and a small mono label:
    - **Reads** (blue): inputs and the config it uses.
    - **Code** (violet): 1-2 verbatim excerpts, trimmed with `...` where needed, each followed by a mono `path:line` reference.
    - **Hands on** or **Writes** (green): what it produces and where it goes.
    - **Watch** or **Not wired** (orange), only when true: gaps, surprises, doc-versus-code drift.
- **(?) detail per stage:** a pop-up written like a staff engineer explaining one file to a colleague. Use these headings, skipping any that would be empty:
  - **Usage:** commands or the call signature, if the step has an entry point.
  - **What `function()` does (`path:line`):** numbered steps, each opening with a bold verb phrase, with nested bullets for branches.
  - **Other pieces:** helpers and how they connect.
  - **Things to know:** gotchas, error behaviour, exit codes, side effects.
  - **Why it is built this way:** the design reasons. Mark interpretation as interpretation.

  Answer the questions a reader will ask next (for example "what does immutable mean here?") inside the relevant pop-up rather than leaving them for a follow-up.
- **Playground:** pick the one computation the system exists to do (a scorer, a combiner, a router, a pricing rule) and reimplement its steps in page JavaScript, faithful to the real code and fed by real fixtures (golden cases, test cases, worked examples). It should provide:
  - A preset switcher, toggles to remove inputs, and switches for the real config levers.
  - Outputs: the result, a per-component breakdown, the fate of each input (counted, dropped and why), and a trace in the code's own trace wording.
  - A self-check line that says whether the untouched preset matches the fixture's expected result.
  - Label hypotheticals as hypothetical. If there is no such computation, skip the playground rather than invent one.
- **Status section:** three status cards (built and running / running in shadow or partial / not wired), then collapsible tables for: open engine-level work, docs versus code disagreements, and the tests that guard the system.

## Step 3: Build the page

Output rules for every mode:

- One self-contained file. No build step, no API keys. External requests limited to Google Fonts and, only if truly needed, pinned CDN scripts. Inline all CSS and JS. Vanilla HTML, CSS and JS: no React, Tailwind or Mermaid for the stage walkthrough.
- File name and place: use the name and folder the user gives. Otherwise put it next to existing explainers (a `resources/` or `docs/` folder that already holds HTML pages), else the project root, as `walkthrough-{topic}.html` or `explainer-{topic}.html`. Always produce the file, never just text.

### Stage walkthrough page anatomy (match the reference)

1. **Header:** mono uppercase eyebrow in the accent colour, an `h1` that states the flow ("One engine run, from ruleset version to ranked pick list"), a one-paragraph lede, then a four-item TL;DR strip, each item a coloured top border, a bold line and a muted sentence.
2. **Stage section:** a section intro saying how to read the rails and cards, then the stage rows.
   - Grid: `minmax(0,1fr) 320px minmax(0,1.45fr)`, rows `min-height: ~64vh`.
   - A spine line through the middle column, half-height on the first and last rows; fork lanes at 70, 160 and 250px; rails with stubs into the node they start or end at.
   - The row crossing the viewport centre is active (IntersectionObserver with `rootMargin: -50% 0px -50% 0px`): full opacity and an accent ring on its node, other rows dimmed to 0.45.
   - Clicking a node scrolls its row to the centre.
3. **Stepper:** fixed on the right, visible only while the stages are on screen. It has Back, a `03 · 3 of 11` counter and Next, which becomes Continue on the last row and jumps to the playground.
4. **(?) pop-ups:**
   - Each brief ends with a `<details class="qmore">` whose `<summary>` reads "Details: <topic>" behind a small circled "?". The inline body is hidden.
   - JavaScript prevents the details element from opening, clones its body into one shared native `<dialog>` and calls `showModal()`.
   - The dialog is centred, up to 760px wide and 86vh tall, with a dimmed backdrop, a header (the stage number as eyebrow, the topic as title) and a 44px close button. The body scrolls.
   - It closes on Esc, the button, or a backdrop click. Never expand detail inline: it shifts the flowchart.
5. **Playground section:** two panels, controls on the left and results on the right (big mono total, band or status pill, ladder of cut-offs, breakdown table, per-input results list, trace, self-check note).
6. **Status section** as above, then a footer naming the repo, branch, commit, date and "line numbers drift" when the repo is active.
7. **Design record** comment at the top of `<style>`: direction, dials, fonts, tokens, sources with the commit.

### Article and Summary specifics

- Article: vanilla HTML, CSS and JS; sticky two-column layout; 3-5 hand-coded Canvas or SVG figures (stepped simulation, parameter explorer, execution-trace stepper, annotated code walkthrough, data-flow diagram). Voice: concrete opening scene, second person, paragraphs of roughly 80-180 words, no bullet lists in body prose, captions say what to look for. Outline the spine first and pause for the user's approval before building.
- Summary: conclusion first, then structure, then detail, full width. For external audiences, redact internal paths, hostnames, ticket IDs, secrets, patient data and jargon, and state what was redacted.

## Design rules

The default theme is the reference's: light and warm, one violet accent, nothing dark unless asked.

- **Tokens on `:root`, used everywhere:**
  - Background, surfaces and line: `--bg #faf9f6`, `--surface #fff`, `--surface-2 #f2f0eb`, `--line #e2dfd8`.
  - Text and accent: `--text #1c1b22`, `--muted #5e5c68`, `--accent #6d3fd6`, `--accent-soft #f2eefb`.
  - Role colours: `--st-data #5b84b8`, `--st-checks #7a5cd0`, `--st-use #3f8f66`.
  - Severity: `--urgent #b4372f`, `--high #c06a1b`, `--medium #8a7a12`, `--low #6b6977`.
  - Scales: spacing `--s1..--s8` (4, 8, 12, 16, 24, 32, 48, 64px); type `--t-xs..--t-2xl` (12, 14, 16, 20, 28, 40px); radius 8px.
- **Fonts:** Instrument Sans for UI and prose, JetBrains Mono for labels, numbers, code and eyebrows, from Google Fonts with system fallbacks. No Inter, Roboto, Arial or Space Grotesk as the main face.
- **Dials for a stage walkthrough:** layout variance low, motion low to medium (only stage focus, a card highlight, a value changing), density medium to high.
- **Mono uppercase micro-labels** (12px, letter-spacing .08em) for eyebrows, card labels and stage tags; balanced headings (`text-wrap: balance`).
- **Avoid the tells:** gradient heroes, emoji as icons, glassmorphism, identical three-up card grids, cards inside cards, a shadow on everything, centred everything, filler copy.
- **Colour never carries meaning alone:** pair it with a word (counted, dropped, shadow, floor).
- **Motion:** short eases, and `prefers-reduced-motion` turns it off.
- **Responsive:** below 1000px, stages collapse to one column (node first, rails, lanes and stepper hidden); below 860px the playground stacks. No horizontal page scroll (code blocks scroll inside themselves), 16px gutters, 44px touch targets.
- **Accessibility:** semantic sections and headings, visible focus rings, keyboard-operable nodes, toggles and dialog, `aria-live` on recomputed results.
- **Prose:** no em dashes, no emoji, plain words.

## Step 3b: Verification you can run (no browser, no server)

Run these before delivery; they are read-only or scratchpad-only:

1. Extract the inline script to the scratchpad and run `node --check` on it.
2. Run the playground in Node with a small DOM stub (`querySelector`, `querySelectorAll`, elements with `innerHTML`, `textContent`, `style`, `dataset`, `classList`, `setAttribute`, `closest`, `showModal`), switch through every preset, and confirm each self-check reports a match with its fixture.
3. Parse the HTML with Python's `html.parser` and confirm no unclosed or mismatched tags; count `<details>` against `</details>`.
4. Grep the file for em dashes and emoji (both must be zero).

## Step 3c: Visual self-check

If your environment's rules do not let the agent launch a browser or server on its own, give the user `open <absolute path>` (or the platform's equivalent) by default and ask for a screenshot or a description, then review against the design rules. Only if the user says to drive it, use a headless browser (Playwright CLI) at desktop and phone widths and fix overflow, clipping, contrast and console errors. State which path was used; if no render was seen, say the layout is unverified.

## Step 4: Fact-check gate (blocking)

Iron law: no explainer ships with an unverified factual claim. Every checkable claim is supported, corrected, or cut.

1. Extract every checkable claim with its location: numbers and counts, versions, `file:line` references, snippets, config values, mechanism claims ("X runs before Y", "Z is never read"), status claims ("not wired", "shadow").
2. Open the actual source for each. For code, the real file at the exact line, at the pinned commit. Counts come from a command you ran (`grep -c`, `uniq -c`), not from a subagent's sentence. Do not trust comments, function names, docs or the mere existence of a citation; when a doc and the code disagree, the page says so.
3. Verdict per claim: supported, needs-source, unsupported, contradicted. Only supported ships.
4. Resolve the rest by adding support, correcting, softening to labelled interpretation, or cutting.
5. If the repo moved during the work, re-run the line-number checks on the changed files.
6. Report an overall PASS or FAIL, listing corrections made, and hold delivery until PASS.

Red flags that mean stop and verify: "I'm fairly sure", "if I recall", "roughly" attached to a number, a subagent count you have not re-run, a URL cited but not opened this session, a snippet pasted from memory.

## Step 5: Polish checklist

- [ ] Fact-check is PASS; branch and commit pinned in the footer and design record
- [ ] Single file, opens with no server and no build; `node --check` passes
- [ ] Playground presets match their fixtures in the Node harness
- [ ] HTML nesting check clean; every stage has a working (?) pop-up
- [ ] Stage rows, fork lanes and rails line up; stepper and active-row highlighting work
- [ ] Phone width: one column, no horizontal scroll, confirmed by a screenshot or stated as unverified
- [ ] Design record comment present; tokens and fonts match the reference
- [ ] No secrets, PHI, real patient data, emoji or em dashes
- [ ] Original source files unchanged

## Final message

Give the file path, the mode, the stage and pop-up counts, whether a playground was built and what it checks, the fact-check verdict with any corrections made, anything unverified (including the render), and anything the work surfaced that changes the user's picture of the project (for example the repo moved, a feature is now built). Keep it short.

## Execution note

Writing the HTML file and scratchpad files is allowed. Do not start servers, run project scripts or touch databases to build or preview it. Give the user the `open <absolute path>` command by default; opening the file or running a headless browser is the agent's own action only when the user has said to drive it for this task.
