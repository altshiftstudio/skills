# JSON Canvas Specification

## File Structure
A `.canvas` file is a JSON object with two top-level arrays:
```json
{
  "nodes": [],
  "edges": []
}
```

## Nodes
Nodes are ordered by z-index (last in array = top).

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| `id` | Yes | string | Unique 16-char hex ID (e.g., `6f0ad84f44ce9c17`) |
| `type` | Yes | string | `text`, `file`, `link`, `group` |
| `x`, `y` | Yes | int | Position in pixels |
| `width`, `height` | Yes | int | Dimensions in pixels |
| `color` | No | string | Preset `"1"`-`"6"` or hex string |

### Node Types

**Text Node**
```json
{ "type": "text", "text": "Markdown content" }
```

**File Node**
```json
{ "type": "file", "file": "path/to/file.md", "subpath": "#Heading" }
```

**Link Node**
```json
{ "type": "link", "url": "https://example.com" }
```

**Group Node**
```json
{ "type": "group", "label": "Label", "background": "path/img.png", "backgroundStyle": "cover" }
```
`backgroundStyle`: `cover`, `ratio`, `repeat`.

## Colors
Colors can be applied to nodes and edges using the `color` attribute.

### Presets
Use string values `"1"` through `"6"` for theme-adaptive semantic colors:

| Preset | Color | Semantic Usage |
| :--- | :--- | :--- |
| `"1"` | **Red** | Errors, critical info, stops |
| `"2"` | **Orange** | Warnings, caution, waiting |
| `"3"` | **Yellow** | Notes, ideas, drafts |
| `"4"` | **Green** | Success, completion, active |
| `"5"` | **Cyan** | Information, links, cold |
| `"6"` | **Purple** | Important, headers, hot |

### Custom Colors
Use any valid hex color string (e.g., `"#FF5733"`).
```json
{ "color": "#4A90E2" }
```

## Edges
Edges connect nodes.

```json
{
  "id": "edge-id",
  "fromNode": "node-1",
  "fromSide": "right",
  "toNode": "node-2",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "connection"
}
```

| Attr | Desc | Values |
|---|---|---|
| `fromSide`/`toSide` | Connection point | `top`, `right`, `bottom`, `left` |
| `fromEnd`/`toEnd` | Endpoint shape | `none`, `arrow` |

## Resources
- [Official Spec](https://jsoncanvas.org/spec/1.0/)
