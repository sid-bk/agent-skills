---
name: code-graph
description: Build and query a code graph of a repository with Graphify, model-assisted. Tree-sitter AST and call graph for structure (no API key), then this session names each community and writes an ARCHITECTURE.md pipeline view. Viewable as symbol-level interactive HTML, a click-to-expand tree, and optionally an Obsidian vault. Invoked as `/code-graph [path] [--include tests,config,data] [--all] [--obsidian]`, `/code-graph update|query|path|explain|find|open ...`. Use when the user asks to graph, map or visualize a codebase's architecture, or to find where a symbol is defined. Writes only to the project's graphify output folder.
---

# /code-graph

Model-assisted code graph. Structure comes from the `graphify` CLI (PyPI `graphifyy`, pinned 0.9.105, installed with `uv tool`) in code-only mode: tree-sitter parsing, call graph, clustering. No API key; Graphify itself never calls a model here. The model work (community names, descriptions, the pipeline view) is done by this session from a compact digest. The offline, no-model counterpart is the `codegraph` controller designed in a separate offline architecture doc; its graph is identical, only the naming differs.

Binary: `graphify` (use its absolute path if the agent's PATH lacks the uv tool bin folder). If it is missing, stop and tell the user (`uv tool install --python 3.12 "graphifyy==0.9.105"`, Tier 2); do not install it yourself.

## Resolve the target and output folder

1. Target `T` = the path argument, default `.`. Resolve it: `T=$(cd "<path>" && pwd -P)`.
2. Map `T` to the output folder `OUT`:

| `T` is | `OUT` |
|---|---|
| `<projects-root>/<project>` | `<projects-root>/graphify_projects/<project>` |
| `<projects-root>/<project>/<sub/path>` | `<projects-root>/graphify_projects/<project>/<sub/path>` |
| `<other-root>/<project>` | `<other-root>/graphify_<suffix>/<project>` |
| `<other-root>/<project>/<sub/path>` | `<other-root>/graphify_<suffix>/<project>/<sub/path>` |
| anywhere else | stop and ask the user where to write |

Refuse if `T` is inside an output root. Never write graph output inside `T`. Every graphify call runs from `T` with `GRAPHIFY_OUT="$OUT"` set, so all outputs land in `OUT`.

## Excludes

Default build is application code only. Exclude groups, each passed as `--exclude '<glob>'` to `extract`:

| Group | Globs |
|---|---|
| tests | `**/tests/**` `**/test/**` `**/e2e/**` `**/__tests__/**` `**/mocks/**` `**/*.spec.*` `**/*.test.*` |
| config | `**/*.yaml` `**/*.yml` `**/*.json` `.github/**` `**/migrations/**` |
| data | `**/packs/**` `**/synth/**` `**/fixtures/**` `**/seeds/**` |

`--include tests,config,data` drops the named groups from the excludes; `--all` drops all of them. Print the active excludes on every build. Save the flags (`--include ...` / `--all` / `--obsidian`) as one line in `OUT/.code-graph-args`.

## Build: `/code-graph [path] [--include ...] [--all] [--obsidian]`

1. Structure (no model):
```bash
mkdir -p "$OUT"
cd "$T" && GRAPHIFY_OUT="$OUT" graphify extract . --code-only "${EXCLUDES[@]}"
cd "$T" && GRAPHIFY_OUT="$OUT" graphify cluster-only . --no-label
graphify tree --graph "$OUT/graph.json" --output "$OUT/tree.html"
printf '%s\n' "$T" > "$OUT/.code-graph-target"
jq -c -f <skill-dir>/digest.jq "$OUT/graph.json" > "$OUT/communities-digest.jsonl"
```
Report node, edge and community counts and the digest size in bytes (about 4 bytes per token) before reading it.

2. Name the communities (model-assisted). Each digest line is one community: `id`, `size`, dominant `folder`, `top` symbols with `file:line`, and up to two `docs` (docstrings). For each community write:
   - `name`: 2 to 6 words naming its role, not its folder (e.g. "Worklist UI screens", "Rule engine templates"). Unique across the graph.
   - `description`: one sentence on what it does, grounded only in the digest line.

   Up to 100 communities: read `communities-digest.jsonl` and do it here. More than 100: split the file into chunks of 100 lines and send one Agent per chunk in a single message; each returns `{"<id>": {"name": ..., "description": ...}}` and nothing else. Never read source files for this step; the digest is the input.

3. Write the results:
   - `OUT/code-graph-communities.json`: `{"<id>": {"name", "description", "folder", "size"}}`.
   - `OUT/code-graph-labels.json`: `{"<id>": "<name>"}` (derive with `jq 'map_values(.name)'`).

4. Draw the views with the names (render only, no re-clustering, so names stay attached to the right communities):
```bash
cd "$T" && GRAPHIFY_OUT="$OUT" graphify export html --graph "$OUT/graph.json" --labels "$OUT/code-graph-labels.json" --node-limit 8000
```
With `--obsidian`, also `export obsidian --graph "$OUT/graph.json" --labels "$OUT/code-graph-labels.json" --dir "$OUT/obsidian"`. Above 8000 nodes `graph.html` falls back to one node per community (now named); say so and suggest graphing a sub-folder.

5. Write `OUT/ARCHITECTURE.md`, the pipeline view. Inputs: `code-graph-communities.json` and the cross-community edge counts from
```bash
jq -r '(.nodes | map({key: .id, value: .community}) | from_entries) as $c
  | [(.links // .edges)[] | [$c[.source], $c[.target]] | select(.[0] != null and .[1] != null and .[0] != .[1]) | sort | map(tostring) | join("-")]
  | group_by(.) | map("\(length)\t\(.[0])") | sort_by(-(split("\t")[0] | tonumber)) | .[0:40][]' "$OUT/graph.json"
```
   Group communities into 4 to 8 pipeline stages (e.g. ingest, data model, engine, API, UI). For each stage: its communities (name, size), one paragraph on its role, and its main links to other stages with edge counts. Cite `file:line` only from the digest's `top` entries. End with a "How to read the views" note pointing at `graph.html`, `tree.html` and the vault.

6. Report to the user: `OUT`, `graph.html`, `tree.html`, `ARCHITECTURE.md`, the vault if built, counts, the excludes used, and the digest size (the token cost of naming).

## Other commands

**Update: `/code-graph update [path]`**: read `OUT/.code-graph-args` and rerun the build with the same flags. Graphify's cache re-parses only changed files. Reuse existing names for communities whose `folder` and top symbols are unchanged; name only new or changed ones.

**Query: `/code-graph query "<question>"`, `path "<A>" "<B>"`, `explain "<node>"`**
```bash
graphify query "<question>" --graph "$OUT/graph.json" --budget 1500
graphify path "<A>" "<B>" --graph "$OUT/graph.json"
graphify explain "<node>" --graph "$OUT/graph.json"
```
Answer only from what the command prints.

**Find: `/code-graph find <symbol>`**: look the symbol up in `OUT/graph.json` with a `jq` filter that prints only matching nodes' `label`, `source_file` and `source_location`. Join `source_file` onto the target in `OUT/.code-graph-target` and print `zed <target>/<source_file>:<line>` (first number in `source_location`). If `source_location` is empty, print the file only and say the line is unknown. Run the `zed` command only if the user asks.

**Open: `/code-graph open [path]`**: print `OUT/graph.html`, `OUT/tree.html`, `OUT/ARCHITECTURE.md`, and `OUT/obsidian/` if it exists (Obsidian: "Open folder as vault").

## Rules

- Keep generated output out of context: never read `graph.json`, `graph.html`, `tree.html` or vault notes. Read only the digest, the jq summaries above, and command output.
- Graphify never calls a model in this skill: never pass `--backend`, `--mode deep`, `--dedup-llm`, never run `graphify label`, and never remove `--code-only` (docs semantic extraction would send repo docs to a model).
- Never export into an existing notes vault; each `OUT/obsidian/` is its own vault.
- Never run `graphify install`, `graphify claude install`, `graphify hook install`, `--watch` or `--mcp` without the user's explicit go-ahead: they edit the agent's global instructions file, `settings.json` or git hooks, or leave a process running.
- Deleting an `OUT` folder is the user's call; it holds only generated files and the build recreates it.
