# One compact record per community, largest first: size, dominant folder,
# best-connected code symbols with file:line, and up to two docstrings.
# Usage: jq -c -f digest.jq graph.json
(reduce (.links // .edges)[] as $e ({}; .[$e.source] += 1 | .[$e.target] += 1)) as $degree
| [.nodes[] | select(.community != null) | . + {degree: ($degree[.id] // 0)}]
| group_by(.community)
| map({
    id: .[0].community,
    size: length,
    folder: ([.[] | (.source_file // "") | select(. != "") | split("/") | .[0:-1] | .[0:4] | join("/")]
             | if length == 0 then "(external)" else (group_by(.) | max_by(length) | .[0]) end),
    top: ([.[] | select(.file_type == "code")] | sort_by(-.degree) | .[0:8]
          | map("\(.label) \(.source_file // "-"):\((.source_location // "") | ltrimstr("L"))")),
    docs: ([.[] | select(.file_type == "rationale") | .label[0:120]] | .[0:2])
  })
| sort_by(-.size)
| .[]
