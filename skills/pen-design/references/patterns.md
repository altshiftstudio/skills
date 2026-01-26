# PEN Format Patterns Reference

Detailed patterns and examples for PEN design manipulation.

---

## Creating Elements

### Frame (Container)
```json
{
  "type": "frame",
  "id": "unique-id",
  "name": "Button/Primary",
  "reusable": true,
  "fill": "$--primary",
  "cornerRadius": "$--radius-m",
  "padding": [12, 24],
  "gap": 8,
  "justifyContent": "center",
  "alignItems": "center",
  "children": [...]
}
```

### Text
```json
{
  "type": "text",
  "id": "text-id",
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
  "id": "icon-id",
  "width": 20,
  "height": 20,
  "iconFontName": "chevron-right",
  "iconFontFamily": "lucide",
  "fill": "$--foreground"
}
```

### Component Instance (ref)
```json
{
  "type": "ref",
  "id": "instance-id",
  "ref": "source-component-id",
  "name": "Alert/Error",
  "fill": "$--color-error",
  "descendants": {
    "title-text-id": {
      "content": "Error occurred",
      "fill": "$--color-error-foreground"
    }
  }
}
```

---

## Styling

### Fill Values
```json
"fill": "$--primary"                    // Token reference
"fill": "#0F5FFE"                       // Hex color
"fill": "#ff550080"                     // Hex with alpha
"fill": {                               // Object form
  "type": "color",
  "color": "#ffffff",
  "enabled": false
}
"fill": {                               // Image fill
  "type": "image",
  "url": "./image.png",
  "mode": "fill"
}
```

### Corner Radius
```json
"cornerRadius": 8                       // All corners
"cornerRadius": "$--radius-pill"        // Token (999 = pill)
"cornerRadius": [8, 8, 0, 0]            // [TL, TR, BR, BL]
```

### Stroke
```json
"stroke": {
  "align": "inside",
  "thickness": 1,
  "fill": "$--border"
}
```

### Per-Side Stroke
```json
"stroke": {
  "align": "inside",
  "thickness": { "bottom": 1 },
  "fill": "$--border"
}
```

### Shadow Effect
```json
"effect": {
  "type": "shadow",
  "shadowType": "outer",
  "color": "#0000000f",
  "offset": { "x": 0, "y": 2 },
  "blur": 3.5,
  "spread": -1
}
```

---

## Layout

### Padding Formats
```json
"padding": 16                           // All sides
"padding": [12, 24]                     // [vertical, horizontal]
"padding": [8, 16, 8, 16]               // [top, right, bottom, left]
```

### Sizing
```json
"width": 360                            // Fixed
"width": "fill_container"               // Flex grow
"width": "fill_container(360)"          // Flex grow, min 360
"height": "fit_content(800)"            // Fit content, max 800
```

---

## Theme Variables

### Definition
```json
"variables": {
  "--primary": {
    "type": "color",
    "value": [
      { "value": "#0F5FFE" },
      { "value": "#0F5FFE", "theme": { "Mode": "Dark" } }
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
```
$--background, $--foreground, $--primary, $--secondary
$--muted, $--accent, $--destructive, $--border, $--input
$--primary-foreground, $--secondary-foreground, $--muted-foreground
$--color-success, $--color-warning, $--color-error, $--color-info
$--font-primary, $--font-secondary
$--radius-none, $--radius-xs, $--radius-m, $--radius-pill
```

---

## Slots

Slots define insertion points for child elements:
```json
{
  "type": "frame",
  "id": "card",
  "name": "Card",
  "slot": ["header-slot-id", "content-slot-id", "footer-slot-id"],
  "children": [...]
}
```

---

## AI Context Property

Add `context` for AI understanding:
```json
{
  "type": "frame",
  "name": "Sidebar",
  "context": "Vertical sidebar navigation with app logo and menu items.",
  ...
}
```

---

## Quick Queries

| Goal | Pattern |
|------|---------|
| Find components | `"reusable": true` |
| Find buttons | `"name":.*Button` |
| Find by token | `"fill": "$--primary"` |
| Find text | `"type": "text"` |
| Find instances | `"type": "ref"` |
