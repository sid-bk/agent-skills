"""Render graph.html and tree.html for a /code-graph output folder.

Reads OUT/graph.json (Graphify) and OUT/code-graph-communities.json (cluster
names and descriptions, model-written or mechanical), and writes self-contained
pages from the templates next to this script. Standard library only.

Usage: python3 render_views.py <OUT>
"""

import json
import re
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent
CATEGORIES = ["Frontend", "Backend", "Tests", "Tooling", "External", "Other"]
TEST_PATH = re.compile(r"(^|/)(tests?|e2e|__tests__|mocks?)(/|$)|\.(spec|test)\.")
FRONTEND_TOPS = {"web", "frontend", "client", "ui", "www"}
FRONTEND_EXTS = {"tsx", "jsx", "vue", "svelte", "css", "scss", "html"}
BACKEND_TOPS = {"api", "server", "backend", "services", "service"}
BACKEND_EXTS = {"py", "go", "rb", "java", "kt", "rs", "cs", "php", "scala"}
TOOLING_TOPS = {"scripts", "infra", "tools", ".github", "docker", "deploy", "ops", "bin"}
SKIPPED_RELATIONS = {"rationale_for"}


def categorize(source_file: str) -> str:
    if not source_file:
        return "External"
    if TEST_PATH.search(source_file):
        return "Tests"
    top = source_file.split("/", 1)[0]
    ext = source_file.rsplit(".", 1)[-1] if "." in source_file else ""
    if top in TOOLING_TOPS:
        return "Tooling"
    if top in FRONTEND_TOPS or (top not in BACKEND_TOPS and ext in FRONTEND_EXTS):
        return "Frontend"
    if top in BACKEND_TOPS or ext in BACKEND_EXTS:
        return "Backend"
    if "/" not in source_file:
        return "Tooling"
    return "Other"


def node_kind(node: dict) -> str:
    label = node.get("label", "")
    source_file = node.get("source_file") or ""
    if not source_file:
        return "external"
    if node.get("_callable_class"):
        return "class"
    if label.endswith("()"):
        return "method" if label.startswith(".") else "function"
    if node.get("source_location") == "L1" and source_file.endswith(label):
        return "file"
    return "symbol"


def line_number(node: dict):
    match = re.search(r"\d+", node.get("source_location") or "")
    return int(match.group()) if match else None


def load_clusters(out: Path, nodes: list) -> dict:
    names_path = out / "code-graph-communities.json"
    named = json.loads(names_path.read_text()) if names_path.exists() else {}
    members: dict = {}
    for node in nodes:
        members.setdefault(node["cluster"], []).append(node["category"])
    clusters = {}
    for cid, categories in members.items():
        info = named.get(str(cid), {})
        clusters[cid] = {
            "name": info.get("name") or f"Cluster {cid}",
            "description": info.get("description", ""),
            "category": max(set(categories), key=categories.count),
            "size": len(categories),
        }
    return clusters


def build_payload(out: Path) -> dict:
    graph = json.loads((out / "graph.json").read_text())
    raw_nodes = graph["nodes"]
    raw_edges = graph.get("links") or graph.get("edges") or []
    docstrings: dict = {}
    rationale_ids = {n["id"] for n in raw_nodes if n.get("file_type") == "rationale"}
    labels_by_id = {n["id"]: n.get("label", "") for n in raw_nodes}
    for edge in raw_edges:
        if edge.get("relation") == "rationale_for" and edge["source"] in rationale_ids:
            docstrings.setdefault(edge["target"], []).append(labels_by_id[edge["source"]])

    nodes, index = [], {}
    for raw in raw_nodes:
        if raw["id"] in rationale_ids or raw.get("community") is None:
            continue
        index[raw["id"]] = len(nodes)
        nodes.append({
            "label": raw.get("label", raw["id"]),
            "file": raw.get("source_file") or "",
            "line": line_number(raw),
            "kind": node_kind(raw),
            "cluster": raw["community"],
            "category": categorize(raw.get("source_file") or ""),
            "doc": " ".join(docstrings.get(raw["id"], []))[:300],
        })

    relations, edges = [], []
    for edge in raw_edges:
        relation = edge.get("relation", "")
        if relation in SKIPPED_RELATIONS:
            continue
        source, target = index.get(edge["source"]), index.get(edge["target"])
        if source is None or target is None or source == target:
            continue
        if relation not in relations:
            relations.append(relation)
        edges.append([source, target, relations.index(relation)])

    target_file = out / ".code-graph-target"
    return {
        "project": out.name,
        "target": target_file.read_text().strip() if target_file.exists() else "",
        "categories": CATEGORIES,
        "nodes": nodes,
        "edges": edges,
        "relations": relations,
        "clusters": load_clusters(out, nodes),
    }


def render(template_name: str, payload: dict, destination: Path) -> None:
    template = (TEMPLATE_DIR / template_name).read_text()
    data = json.dumps(payload, separators=(",", ":")).replace("</", "<\\/")
    search_js = (TEMPLATE_DIR / "search.js").read_text()
    page = template.replace("/*__SEARCH_JS__*/", search_js)
    destination.write_text(page.replace("/*__CODE_GRAPH_DATA__*/null", data))


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: render_views.py <OUT>")
    out = Path(sys.argv[1]).expanduser().resolve()
    if not (out / "graph.json").exists():
        sys.exit(f"error: no graph.json in {out}")
    payload = build_payload(out)
    render("graph.template.html", payload, out / "graph.html")
    render("tree.template.html", payload, out / "tree.html")
    print(f"rendered graph.html and tree.html: {len(payload['nodes'])} nodes, "
          f"{len(payload['edges'])} edges, {len(payload['clusters'])} clusters")


if __name__ == "__main__":
    main()
