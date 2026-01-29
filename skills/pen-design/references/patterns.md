# PEN Format Patterns

Element creation, styling, and theming examples for .pen files.

## Contents

- [Elements](#elements)
  - [Frame](#frame)
  - [Text](#text)
  - [Icon](#icon)
  - [Component Instance](#component-instance)
- [Styling](#styling)
  - [Fill](#fill)
  - [Stroke](#stroke)
  - [Corner Radius](#corner-radius)
  - [Shadow](#shadow)
- [Layout](#layout)
  - [Padding](#padding)
  - [Sizing](#sizing)
- [Theming](#theming)
  - [Variable Definition](#variable-definition)
  - [Common Tokens](#common-tokens)
- [Advanced](#advanced)
  - [Slots](#slots)
  - [AI Context](#ai-context)

---

## Elements

### Frame

```json
{
  "type": "frame",
  "id": "btn01",
  "name": "Button/Primary",
  "reusable": true,
  "fill": "$--primary",
  "cornerRadius": "$--radius-m",
  "padding": [12, 24],
  "gap": 8,
  "layout": "horizontal",
  "justifyContent": "center",
  "alignItems": "center",
  "children": [...]
}
```

### Text

```json
{
  "type": "text",
  "id": "lbl01",
  "name": "Button Label",
  "content": "Click me",
  "fill": "$--primary-foreground",
  "fontFamily": "$--font-primary",
  "fontSize": 14,
  "fontWeight": "500",
  "lineHeight": 1.4286
}
```

### Icon

```json
{
  "type": "icon_font",
  "id": "ico01",
  "width": 20,
  "height": 20,
  "iconFontName": "chevron-right",
  "iconFontFamily": "lucide",
  "fill": "$--foreground"
}
```

### Component Instance

```json
{
  "type": "ref",
  "id": "alert1",
  "ref": "AlertComponent",
  "name": "Alert/Error",
  "fill": "$--color-error",
  "descendants": {
    "titleText": {"content": "Error occurred"},
    "icon": {"fill": "$--color-error-foreground"}
  }
}
```

---

## Styling

### Fill

```json
// Token reference
"fill": "$--primary"

// Hex color
"fill": "#0F5FFE"

// With alpha
"fill": "#ff550080"

// Disabled fill
"fill": {"type": "color", "color": "#ffffff", "enabled": false}

// Image fill
"fill": {"type": "image", "url": "./hero.png", "mode": "fill"}
```

### Stroke

```json
// Basic stroke
"stroke": {
  "align": "inside",
  "thickness": 1,
  "fill": "$--border"
}

// Per-side stroke (bottom only)
"stroke": {
  "align": "inside",
  "thickness": {"bottom": 1},
  "fill": "$--border"
}
```

### Corner Radius

```json
// All corners
"cornerRadius": 8

// Token
"cornerRadius": "$--radius-pill"

// Individual [TL, TR, BR, BL]
"cornerRadius": [8, 8, 0, 0]
```

### Shadow

```json
"effect": {
  "type": "shadow",
  "shadowType": "outer",
  "color": "#0000000f",
  "offset": {"x": 0, "y": 2},
  "blur": 3.5,
  "spread": -1
}
```

---

## Layout

### Padding

```json
// All sides
"padding": 16

// [vertical, horizontal]
"padding": [12, 24]

// [top, right, bottom, left]
"padding": [8, 16, 8, 16]
```

### Sizing

```json
// Fixed
"width": 360

// Fill available space
"width": "fill_container"

// Fill with minimum
"width": "fill_container(360)"

// Fit content with maximum
"height": "fit_content(800)"
```

---

## Theming

### Variable Definition

```json
"variables": {
  "--primary": {
    "type": "color",
    "value": [
      {"value": "#0F5FFE"},
      {"value": "#3B82F6", "theme": {"Mode": "Dark"}}
    ]
  },
  "--font-primary": {
    "type": "string",
    "value": "Inter"
  },
  "--radius-m": {
    "type": "number",
    "value": 8
  }
}
```

### Common Tokens

| Category | Tokens |
|----------|--------|
| **Background** | `$--background`, `$--foreground`, `$--muted`, `$--accent` |
| **Brand** | `$--primary`, `$--secondary`, `$--destructive` |
| **Foreground** | `$--primary-foreground`, `$--secondary-foreground`, `$--muted-foreground` |
| **Semantic** | `$--color-success`, `$--color-warning`, `$--color-error`, `$--color-info` |
| **UI** | `$--border`, `$--input`, `$--ring` |
| **Typography** | `$--font-primary`, `$--font-secondary` |
| **Radii** | `$--radius-none`, `$--radius-xs`, `$--radius-m`, `$--radius-pill` |

---

## Advanced

### Slots

Define insertion points for child content:

```json
{
  "type": "frame",
  "id": "card",
  "name": "Card",
  "slot": ["header-slot", "content-slot", "footer-slot"],
  "children": [...]
}
```

### AI Context

Add `context` property for AI understanding:

```json
{
  "type": "frame",
  "name": "Sidebar",
  "context": "Vertical navigation with logo at top and menu items below.",
  ...
}
```
