---
name: excalidraw-diagram
description: Create hand-drawn Excalidraw diagrams (architecture, flows, sequence diagrams, before/after/state comparisons) through an Excalidraw MCP server, and export them to a shareable excalidraw.com link. Use when the user asks for a diagram, sketch, whiteboard, or visual explanation, or explicitly says "excalidraw".
---

# Excalidraw Diagram Creation

Two different Excalidraw MCP servers show up in the wild with incompatible tool
sets. Detect which one is connected before drawing anything.

## Step 0 — detect the backend

Search or list your available tools for "excalidraw" and check the tool names returned:

| Tools present | Backend | Use |
|---|---|---|
| `create_view`, `read_me`, `save_checkpoint`, `read_checkpoint`, `export_to_excalidraw` | a chat host's built-in, chat-native Excalidraw integration | **Workflow A** |
| `create_element`, `batch_create_elements`, `update_element`, `query_elements`, `get_canvas_screenshot`, `export_to_excalidraw_url`, `create_from_mermaid`, … | [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) — self-hosted local canvas server | **Workflow B** |

If neither is present, tell the user no Excalidraw MCP is configured — this
skill can't draw without one, and building the JSON by hand into a chat
message doesn't render anywhere useful.

---

## Workflow A — chat-native (`create_view`)

1. Call `read_me` **once per conversation** — it never returns anything new
   on a second call. It gives the full element-format spec, color palette,
   camera-sizing rules (4:3 only: 400×300 / 600×450 / 800×600 / 1200×900 /
   1600×1200), font-size minimums, and worked examples (flow diagram,
   sequence diagram, animation-by-delete-and-replace). Follow it for element
   structure and camera choreography.
2. Plan the layout before writing JSON — regions/columns, legend placement,
   callout space. Fixing coordinates after the fact costs more than planning
   them up front.
3. Call `create_view` with the elements array. The `label: {text, fontSize}`
   shorthand on shapes is real, supported syntax for **this tool** and
   renders correctly inline — use it freely here.
4. Iterating on a drawn diagram: use `restoreCheckpoint` + new elements
   rather than resending the whole scene. Every `create_view` response
   returns a `checkpointId`; `read_checkpoint(id)` fetches the raw element
   list back out if you need it (e.g. before exporting, or before an edit
   that depends on prior coordinates).
5. If the user wants a persistent/shareable link, see **Exporting** below.
   Do not pass the same simplified elements straight to `export_to_excalidraw`
   — it silently drops all the text.

### Exporting — the one pitfall that matters

`export_to_excalidraw` uploads to excalidraw.com and expects a **fully valid
Excalidraw scene**, not the simplified shorthand `create_view` accepts. Two
shorthands break silently on export (shapes/lines still show up; all text
vanishes, and the user reports "there's no text in the image"):

- **`label: {text, fontSize}` on a shape** — not a real Excalidraw field.
  excalidraw.com's parser ignores unknown properties, so the container
  renders with no text at all.
- **Minimal `text` elements** (just `id/x/y/text/fontSize`) — missing
  `fontFamily`, `textAlign`, `verticalAlign`, `containerId`, `originalText`,
  `lineHeight`, `baseline` — often fail to survive excalidraw.com's scene
  restore even though they render fine inline via `create_view`.

**Fix: expand every shorthand element into a full Excalidraw element before
exporting.** For any shape with a `label`, emit two elements: the shape
(carrying `boundElements: [{"id": textId, "type": "text"}]`) and a separate
bound `text` element (`containerId` pointing back to the shape, `textAlign:
"center"`, `verticalAlign: "middle"`, centered inside the container's box).
For standalone text, fill in the full field set.

Doing this by hand is error-prone past a handful of elements. Use this
conversion helper — write it to the scratchpad, call the shape/text/arrow
functions with the same ids and coordinates you already used in
`create_view`, then feed the resulting `scene.json` straight into
`export_to_excalidraw`:

```python
import json, random

def rid():
    return "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(12))

def seed():
    return random.randint(1, 2_000_000_000)

BASE = dict(
    angle=0, groupIds=[], frameId=None, roundness=None,
    boundElements=None, updated=1, link=None, locked=False, isDeleted=False,
    strokeColor="#1e1e1e", backgroundColor="transparent", fillStyle="solid",
    strokeWidth=2, strokeStyle="solid", roughness=1, opacity=100,
)

elements = []

def rect(id_, x, y, w, h, bg="transparent", stroke="#1e1e1e", strokeStyle="solid",
         rounded=True, opacity=100, label=None, label_size=16, label_color=None):
    el = dict(BASE)
    el.update(dict(
        id=id_, type="rectangle", x=x, y=y, width=w, height=h,
        backgroundColor=bg, strokeColor=stroke, strokeStyle=strokeStyle,
        roundness={"type": 3} if rounded else None, opacity=opacity,
        seed=seed(), version=1, versionNonce=seed(),
    ))
    elements.append(el)
    if label:
        add_bound_text(el, label, label_size, label_color)
    return el

def ellipse(id_, x, y, w, h, bg="transparent", stroke="#1e1e1e"):
    el = dict(BASE)
    el.update(dict(
        id=id_, type="ellipse", x=x, y=y, width=w, height=h,
        backgroundColor=bg, strokeColor=stroke,
        seed=seed(), version=1, versionNonce=seed(),
    ))
    elements.append(el)
    return el

def diamond(id_, x, y, w, h, bg="transparent", stroke="#1e1e1e", label=None, label_size=16):
    el = dict(BASE)
    el.update(dict(
        id=id_, type="diamond", x=x, y=y, width=w, height=h,
        backgroundColor=bg, strokeColor=stroke, roundness={"type": 2},
        seed=seed(), version=1, versionNonce=seed(),
    ))
    elements.append(el)
    if label:
        add_bound_text(el, label, label_size)
    return el

def arrow(id_, x, y, w, h, points, stroke="#1e1e1e", strokeStyle="solid",
          endArrowhead="arrow", startArrowhead=None, label=None, label_size=14):
    el = dict(BASE)
    el.update(dict(
        id=id_, type="arrow", x=x, y=y, width=w, height=h, points=points,
        strokeColor=stroke, strokeStyle=strokeStyle,
        startArrowhead=startArrowhead, endArrowhead=endArrowhead,
        roundness={"type": 2}, lastCommittedPoint=None,
        startBinding=None, endBinding=None,
        seed=seed(), version=1, versionNonce=seed(),
    ))
    elements.append(el)
    if label:
        add_bound_text(el, label, label_size, mid_only=True)
    return el

def add_bound_text(container, text_str, font_size=16, color=None, mid_only=False):
    tid = rid()
    est_w = max(20, int(len(text_str) * font_size * 0.55))
    line_h = int(font_size * 1.25)
    if mid_only:  # arrow — center text over the midpoint of its bounding box
        cx = container["x"] + container["width"] / 2
        cy = container["y"] + container["height"] / 2
        tx, ty = cx - est_w / 2, cy - line_h / 2
    else:  # shape — center text inside the box
        tx = container["x"] + max(2, (container["width"] - est_w) / 2)
        ty = container["y"] + (container["height"] - line_h) / 2
    t = dict(BASE)
    t.update(dict(
        id=tid, type="text", x=tx, y=ty, width=est_w, height=line_h,
        strokeColor=color or "#1e1e1e", backgroundColor="transparent",
        text=text_str, fontSize=font_size, fontFamily=1, textAlign="center",
        verticalAlign="middle", containerId=container["id"],
        originalText=text_str, lineHeight=1.25, baseline=int(font_size * 0.9),
        seed=seed(), version=1, versionNonce=seed(),
    ))
    elements.append(t)
    container["boundElements"] = [{"id": tid, "type": "text"}]
    return t

def text(id_, x, y, s, font_size=16, color="#1e1e1e", align="left"):
    est_w = max(10, int(len(s) * font_size * 0.55))
    line_h = int(font_size * 1.25)
    el = dict(BASE)
    el.update(dict(
        id=id_, type="text", x=x, y=y, width=est_w, height=line_h,
        strokeColor=color, backgroundColor="transparent",
        text=s, fontSize=font_size, fontFamily=1, textAlign=align,
        verticalAlign="top", containerId=None, originalText=s,
        lineHeight=1.25, baseline=int(font_size * 0.9),
        seed=seed(), version=1, versionNonce=seed(),
    ))
    elements.append(el)
    return el

def write_scene(path):
    scene = {
        "type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
        "files": {},
    }
    with open(path, "w") as f:
        json.dump(scene, f)
    print("elements:", len(elements))

# --- transcribe your create_view elements as calls, e.g.: ---
# rect("card1", 45, 110, 190, 28, bg="#d0bfff", label="Generated note")
# arrow("a1", 252, 70, 26, 0, [[0, 0], [26, 0]], stroke="#4a9eed")
# text("title", 156, 0, "My Diagram", font_size=24)
# write_scene("/path/to/scratchpad/scene.json")
```

Steps:
1. `read_checkpoint(id)` to get the current raw elements if you didn't keep
   your own running list while drawing.
2. Strip out `cameraUpdate` / `restoreCheckpoint` / `delete` pseudo-elements
   — they aren't real scene elements.
3. Transcribe each remaining element into a call to the helper functions
   above, reusing the same ids and coordinates. This is mechanical, not
   creative — copy the numbers you already used.
4. Run the script, read the resulting `scene.json`, and pass its full
   contents as the `json` argument to `export_to_excalidraw`.
5. Before calling the export done, confirm the returned link actually shows
   text — this exact failure mode (shapes with empty-looking labels) ships
   silently and has fooled a review pass before.

---

## Workflow B — self-hosted canvas (yctimlin/mcp_excalidraw)

Reference: https://github.com/yctimlin/mcp_excalidraw — a local Node.js
server (default `http://127.0.0.1:3000`) exposing 26 tools for full CRUD on
a live, screenshottable Excalidraw canvas with WebSocket sync to a real
browser tab. Not connected by default — documented here so this skill
adapts correctly if it ever is (or if the user asks to set it up).

Setup, only if asked:
```bash
npx -y mcp-excalidraw-server start        # starts the local server + canvas
```
MCP client config:
```json
{"mcpServers": {"excalidraw": {"command": "npx", "args": ["-y", "mcp-excalidraw-server"]}}}
```
Requires Node.js >= 20, no API keys.

Tool groups once connected:
- **Element CRUD**: `create_element`, `get_element`, `update_element`,
  `delete_element`, `query_elements`, `batch_create_elements`,
  `duplicate_elements`
- **Layout**: `align_elements`, `distribute_elements`, `group_elements`,
  `ungroup_elements`, `lock_elements`, `unlock_elements`
- **Scene awareness**: `describe_scene`, `get_canvas_screenshot` — use the
  screenshot tool to actually see what you drew; there's no streaming inline
  preview like Workflow A's `create_view`
- **File I/O**: `export_scene`, `import_scene`, `export_to_image`,
  `export_to_excalidraw_url`, `create_from_mermaid` (fastest path for a
  flowchart: hand it Mermaid syntax directly instead of hand-placing nodes)
- **State**: `clear_canvas`, `snapshot_scene`, `restore_snapshot`
- **Viewport**: `set_viewport` (`scrollToElementIds`, `viewportZoomFactor`)
- **Docs**: `read_diagram_guide`, `get_resource` — call `read_diagram_guide`
  first, the same way Workflow A calls `read_me`

Elements here are native Excalidraw already — `text` goes directly on a
shape as a plain property and arrows bind via `startElementId`/
`endElementId`; the CLI normalizes these into real bound-text/binding
internals for you. `export_to_excalidraw_url` exports the live canvas
state, which is already fully valid, so **the Workflow-A export pitfall
does not apply here** — no conversion step needed.

Since it drives a real canvas rather than a chat-inline preview, always
`get_canvas_screenshot` after drawing to verify before telling the user
it's done.

---

## Common mistakes (either workflow)

- Reusing an element id after deleting it (Workflow A) — always mint a new
  id for the replacement.
- Non-4:3 camera sizes in Workflow A — only 400×300 / 600×450 / 800×600 /
  1200×900 / 1600×1200 are valid; anything else distorts.
- Text below 14px anywhere, below 16px for body text/labels, below 20px for
  titles — unreadable at display scale even if it looks fine in the JSON.
- Declaring a diagram "shared" or "exported" without confirming the link
  actually renders its text.
- Calling `read_me` (or `read_diagram_guide`) more than once per
  conversation — it's a static reference, not per-diagram state.
