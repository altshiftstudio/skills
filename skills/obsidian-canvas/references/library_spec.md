# Canvas Library CLI Specification

This document describes the JSON interface for `scripts/canvas_lib.py`.

## Usage

Pipe a JSON object into the script via `stdin`:

```bash
echo '{...}' | python3 scripts/canvas_lib.py
```

## Root Object

| Property | Type | Required | Description |
|---|---|---|---|
| `output` | string | **Yes** | Output filename (e.g., `"diagram.canvas"`). |
| `nodes` | array | No | List of Node objects. |
| `edges` | array | No | List of Edge objects. |
| `groups` | array | No | List of Group objects. |

---

## Nodes

Nodes are the content blocks on the canvas.

### Text Node (Default)

| Property | Type | Description |
|---|---|---|
| `node_id` | string | explicit ID for referencing in edges. If omitted, a UUID is generated. |
| `text` | string | The markdown content of the node. |
| `x`, `y` | int | Position coordinates. |
| `width` | int | default `250`. |
| `height` | int | **Optional**. If omitted, calculated automatically based on text length. |
| `color` | string | `1`-`6` preset or hex. |

```json
{
  "node_id": "step1",
  "text": "Start Process",
  "x": 0,
  "y": 0,
  "color": "6"
}
```

### File Node

Use `file` property instead of `text`.

| Property | Type | Description |
|---|---|---|
| `file` | string | Absolute or relative path to an Obsidian file. |
| `x`, `y` | int | Position. |
| `width`, `height` | int | Dimensions. |

```json
{
  "node_id": "doc1",
  "file": "Notes/Meeting.md",
  "x": 300,
  "y": 0
}
```

---

## Edges

Connections between nodes.

| Property | Type | Description |
|---|---|---|
| `from_node` | string | `node_id` of the source. |
| `to_node` | string | `node_id` of the target. |
| `label` | string | Optional text label on the line. |
| `color` | string | Optional color (`1`-`6`). |
| `from_side` | string | `top`, `bottom`, `left`, `right`. **Optional**: defaults to Smart Routing. |
| `to_side` | string | `top`, `bottom`, `left`, `right`. **Optional**: defaults to Smart Routing. |

```json
{
  "from_node": "step1",
  "to_node": "doc1",
  "label": "References"
}
```

### Smart Routing
If `from_side` or `to_side` are omitted, the library calculates them based on relative positions (e.g., if target is to the right, flow `right` -> `left`).

---

## Groups

Containers for visually grouping nodes.

| Property | Type | Description |
|---|---|---|
| `label` | string | The group title. |
| `nodes_in_group` | array<string> | List of `node_id`s to contain. The library automatically calculates the group's bounding box with appropriate padding. |
| `color` | string | Background color specificiation. |

```json
{
  "label": "Initialization",
  "nodes_in_group": ["step1", "doc1"],
  "color": "5"
}
```
