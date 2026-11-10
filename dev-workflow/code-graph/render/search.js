/* Shared search for graph.html and tree.html. Every word must appear in the
   node's label, path, cluster name, cluster description or docstring; label
   matches rank highest. Returns [[score, nodeIndex, matchedIn], ...]. */
function createSearch(D) {
  const degree = D.nodes.map(() => 0);
  D.edges.forEach(([s, t]) => { degree[s] += 1; degree[t] += 1; });
  const text = D.nodes.map((n) => {
    const c = D.clusters[n.cluster] || {};
    return { label: n.label.toLowerCase(), file: n.file.toLowerCase(), cluster: (c.name || "").toLowerCase(),
             rest: ((c.description || "") + " " + n.doc + " " + n.kind + " " + n.category).toLowerCase() };
  });
  return function runSearch(query) {
    const words = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    const phrase = words.join(" ");
    const scored = [];
    text.forEach((t, i) => {
      let score = 0, matchedIn = "";
      for (const w of words) {
        if (t.label.includes(w)) score += 5;
        else if (t.cluster.includes(w)) { score += 3; matchedIn = matchedIn || "cluster"; }
        else if (t.file.includes(w)) { score += 2; matchedIn = matchedIn || "path"; }
        else if (t.rest.includes(w)) { score += 1; matchedIn = matchedIn || "description"; }
        else return;
      }
      if (t.label === phrase || t.label === phrase + "()") score += 20;
      if (t.cluster === phrase) score += 8;
      scored.push([score, i, matchedIn]);
    });
    return scored.sort((a, b) => b[0] - a[0] || degree[b[1]] - degree[a[1]]);
  };
}
