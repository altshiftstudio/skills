---
name: pen-design
description: Design and manipulate Pencil (.pen) files using MCP tools. Use this skill when (1) creating UI screens, dashboards, or layouts in .pen format, (2) reading or modifying existing .pen designs, (3) working with design system components, (4) generating code from .pen files, or (5) understanding PEN file structure, tokens, or schema.
---

# Pencil Design

Create and manipulate `.pen` design files using Pencil MCP tools.

## Workflow

### 1. Orientation

```
get_editor_state     → Check active file and selection
get_guidelines       → Load topic-specific rules (landing-page, design-system, table, code, tailwind)
batch_get            → Read file structure or find components
```

### 2. Design (if creating from scratch)

```
get_style_guide_tags → Browse available visual styles
get_style_guide      → Load style guide for inspiration
open_document        → Create new file if needed
```

### 3. Build

```
batch_design         → Insert, update, copy, replace, move, delete nodes (max 25 ops/call)
get_screenshot       → Verify visual output after changes
snapshot_layout      → Debug layout issues or find clipping problems
```

### 4. Refine

```
get_variables        → Read design tokens and themes
set_variables        → Update tokens for consistent styling
replace_all_matching_properties → Bulk property updates
```

---

## Quick Reference

### Element Types

| Type | Purpose | Key Properties |
|------|---------|----------------|
| `frame` | Container/layout | `layout`, `gap`, `padding`, `children`, `reusable` |
| `text` | Typography | `content`, `fontFamily`, `fontSize`, `fontWeight` |
| `rectangle` | Shape | `width`, `height`, `fill`, `cornerRadius` |
| `ref` | Component instance | `ref` (source ID), `descendants` (overrides) |
| `icon_font` | Icon | `iconFontName`, `iconFontFamily` ("lucide") |
| `path` | Vector | `geometry` (SVG path data) |

### Layout

| Property | Values |
|----------|--------|
| `layout` | `"none"` (absolute), `"horizontal"`, `"vertical"` |
| `justifyContent` | `start`, `center`, `end`, `space_between` |
| `alignItems` | `start`, `center`, `end`, `stretch` |
| `width`/`height` | `360`, `"fill_container"`, `"fill_container(360)"`, `"fit_content"` |
| `padding` | `16`, `[12, 24]`, `[8, 16, 8, 16]` |

### Tokens

Prefix: `$--`

| Category | Examples |
|----------|----------|
| Colors | `$--primary`, `$--foreground`, `$--background`, `$--border` |
| Semantic | `$--color-success`, `$--color-warning`, `$--color-error` |
| Typography | `$--font-primary`, `$--font-secondary` |
| Radii | `$--radius-none`, `$--radius-m`, `$--radius-pill` |

---

## Operations (batch_design)

Operations use JavaScript-like syntax. Every Insert/Copy/Replace needs a binding.

| Op | Syntax | Use |
|----|--------|-----|
| **I** | `btn=I(parent, {type: "frame", ...})` | Insert node |
| **U** | `U(path, {content: "New"})` | Update properties |
| **C** | `copy=C(sourceId, parent, {...})` | Copy node |
| **R** | `new=R(path, {type: "text", ...})` | Replace node |
| **M** | `M(nodeId, newParent, index?)` | Move node |
| **D** | `D(nodeId)` | Delete node |
| **G** | `G(nodeId, "stock", "office")` | Apply image fill |

### Component Instances

```javascript
// Insert instance and override text
card=I(container, {type: "ref", ref: "CardComp"})
U(card+"/titleText", {content: "New Title"})

// Replace slot content
newContent=R(card+"/slot", {type: "text", content: "Custom"})
```

### Critical Rules

1. **IDs auto-generate** — never set `id` in node data
2. **Bindings required** — every I/C/R must have `name=...`
3. **Max 25 ops** — split larger designs across calls
4. **Copy descendants** — use `descendants` property, not separate U() calls
5. **Verify visually** — call `get_screenshot` after modifications

---

## Reference Files

| File | When to Read |
|------|--------------|
| [mcp-operations.md](references/mcp-operations.md) | Detailed operation syntax, examples, and edge cases |
| [patterns.md](references/patterns.md) | Element creation examples, styling patterns, theming |
| [schema.json](references/schema.json) | Authoritative property definitions for validation |
