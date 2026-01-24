---
name: obsidian-canvas
description: Create, edit, and manipulate Obsidian Canvas (.canvas) files. Use this skill when the user wants to visualize concepts, build flowcharts, or organize information spatially using the JSON Canvas format.
---

# Obsidian Canvas

This skill handles the creation and manipulation of `.canvas` files (JSON Canvas).

## Core Workflow

1.  **Library**: Utilization of the provided `scripts/canvas_lib.py` is **MANDATORY**. Do not write raw JSON.
2.  **Execution**: Construct a JSON payload and pipe it to the library script via stdin (CLI mode). Do not create temporary Python scripts.
3.  **Layout**: Focus on logical coordinates (x,y). The library handles ID generation, node height, and edge routing automatically.

## Resources

- **Library**: `scripts/canvas_lib.py` (Core logic for nodes, groups, and smart edges).
- **CLI Spec**: [references/library_spec.md](references/library_spec.md) - **Read strictly for JSON format**.
- **Specification**: See [references/spec.md](references/spec.md) for the detailed JSON schema.
- **Example**: See [assets/flowchart.canvas](assets/flowchart.canvas).

## Layout & Aesthetics

- **Layout**: Space nodes nicely (e.g., 100px gap). Align to a theoretical grid.
- **Swimlanes**: When using groups as swimlanes (columns), align interacting nodes across lanes to the same `y` axis.
- **Colors**: Use presets `"1"`-`"6"` for semantic meaning (Red=Error, Green=Success, Purple=System).

## Output
To create a new canvas, construct a JSON payload and pipe it to the library script:

```bash
cat <<EOF | python3 /path/to/skills/obsidian-canvas/scripts/canvas_lib.py
{
  "output": "Project_Flow.canvas",
  "nodes": [
    {"node_id": "start", "text": "Start", "x": 0, "y": 0, "color": "6"},
    {"node_id": "end", "text": "End", "x": 0, "y": 200, "color": "1"}
  ],
  "edges": [
    {"from_node": "start", "to_node": "end"}
  ],
  "groups": [
    {"label": "Phase 1", "nodes_in_group": ["start", "end"], "color": "5"}
  ]
}
EOF
```
