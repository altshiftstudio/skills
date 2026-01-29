# Pencil MCP Operations Reference

Detailed syntax and examples for `batch_design` and other Pencil MCP tools.

## Contents

- [batch_design Operations](#batch_design-operations)
  - [Insert (I)](#insert-i)
  - [Update (U)](#update-u)
  - [Copy (C)](#copy-c)
  - [Replace (R)](#replace-r)
  - [Move (M)](#move-m)
  - [Delete (D)](#delete-d)
  - [Generate Image (G)](#generate-image-g)
- [Working with Components](#working-with-components)
- [Common Patterns](#common-patterns)
- [Reading Tools](#reading-tools)
- [Utility Tools](#utility-tools)

---

## batch_design Operations

Execute up to 25 operations per call. On error, all operations roll back.

### Insert (I)

```
insertedNodeId = I(parent, nodeData)
```

- **parent**: Frame ID, binding name, or `document` (root only)
- **nodeData**: Node properties following .pen schema
- IDs auto-generate — never include `id` property
- Returns inserted node ID

```javascript
// Insert frame
container=I("parentId", {type: "frame", layout: "vertical", gap: 16})

// Insert into binding
item=I(container, {type: "text", content: "Hello"})

// Insert component instance
card=I(container, {type: "ref", ref: "CardComponent"})
```

### Update (U)

```
U(path, updateData)
```

- **path**: Node ID or instance path (`instanceId/childId`)
- Cannot change `id`, `type`, or `ref`
- Cannot update `children` — use Replace (R) instead

```javascript
// Update text content
U("textNodeId", {content: "Updated text", fontSize: 16})

// Update nested component child
U("card/titleText", {content: "New Title"})

// Update layout
U("frameId", {layout: "horizontal", gap: 24, padding: [16, 24]})
```

### Copy (C)

```
copiedNodeId = C(sourceId, parent, copyData)
```

- **sourceId**: ID of node to copy
- **parent**: Target parent ID or binding
- **copyData**: Override properties + optional `descendants` map
- Copying reusable nodes creates `ref` instances
- **Critical**: Use `descendants` for child overrides, not separate U() calls

```javascript
// Copy with position
screen2=C("screenId", document, {
  name: "Screen V2",
  positionDirection: "right",
  positionPadding: 100
})

// Copy with descendant overrides
label=C("labelComp", container, {
  descendants: {
    "textId": {content: "Custom Label"},
    "iconId": {fill: "#FF0000"}
  }
})
```

### Replace (R)

```
replacedNodeId = R(path, nodeData)
```

- Swaps node at path with new node
- Ideal for replacing slot content in components

```javascript
// Replace text with different element
newEl=R("oldTextId", {type: "frame", layout: "horizontal", children: []})

// Replace slot in component instance
custom=R("card/contentSlot", {type: "text", content: "Custom content"})
```

### Move (M)

```
M(nodeId, parent, index?)
```

- **nodeId**: Must be actual ID, not path or binding
- **parent**: Target parent ID or binding (optional)
- **index**: Position among siblings (optional, defaults to end)

```javascript
// Move to end of parent
M("nodeId", "newParentId")

// Move to specific position
M("nodeId", "parentId", 0)  // First position
```

### Delete (D)

```
D(nodeId)
```

- **nodeId**: Must be actual ID, not path or binding

```javascript
D("unwantedNodeId")
```

### Generate Image (G)

```
G(nodeId, type, prompt)
```

- **nodeId**: Frame or rectangle to apply image fill
- **type**: `"ai"` (generated) or `"stock"` (Unsplash)
- **prompt**: Description or search keywords
- No `image` node type — images are fills on frames/rectangles

```javascript
// Create frame then apply image
hero=I(container, {type: "frame", width: 800, height: 400})
G(hero, "stock", "modern office workspace")

// AI-generated image
G("logoFrame", "ai", "minimalist tech logo, flat design, blue")
```

---

## Working with Components

### Instance Path Syntax

Access nested children with slash-separated paths:

```
instanceId/childId
instanceId/parentId/childId
```

### Override Patterns

```javascript
// 1. Insert instance, then update children
card=I(container, {type: "ref", ref: "Card"})
U(card+"/title", {content: "New Title"})
U(card+"/subtitle", {content: "Description"})

// 2. Insert with inline child override
card=I(container, {
  type: "ref",
  ref: "Card",
  children: [{type: "text", content: "Override", fontSize: 14}]
})

// 3. Replace slot entirely
newSlot=R(card+"/contentSlot", {type: "frame", layout: "vertical"})
I(newSlot, {type: "text", content: "Custom content"})
```

---

## Common Patterns

### Dashboard Layout

```javascript
// Structure
sidebar=I("dashboardFrame", {type: "ref", ref: "Sidebar", width: 240, height: "fill_container"})
main=I("dashboardFrame", {type: "frame", layout: "vertical", gap: 24, padding: 32, width: "fill_container"})

// Stats row
statsRow=I(main, {type: "frame", layout: "horizontal", gap: 16})
card1=I(statsRow, {type: "ref", ref: "StatCard", width: "fill_container"})
card2=I(statsRow, {type: "ref", ref: "StatCard", width: "fill_container"})
card3=I(statsRow, {type: "ref", ref: "StatCard", width: "fill_container"})

// Override card content
U(card1+"/value", {content: "$12,450"})
U(card1+"/label", {content: "Revenue"})
```

### Form Section

```javascript
form=I(container, {type: "frame", layout: "vertical", gap: 16})

// Input fields
input1=I(form, {type: "ref", ref: "TextInput", width: "fill_container"})
U(input1+"/label", {content: "Email"})
U(input1+"/placeholder", {content: "you@example.com"})

input2=I(form, {type: "ref", ref: "TextInput", width: "fill_container"})
U(input2+"/label", {content: "Password"})

// Submit button
submit=I(form, {type: "ref", ref: "Button/Primary"})
U(submit+"/label", {content: "Sign In"})
```

### Screen Duplication

```javascript
// Copy screen with variations
v2=C("originalScreen", document, {
  name: "Screen V2",
  positionDirection: "right",
  positionPadding: 100
})

// Modify the copy
D(v2+"/optionalSection")
U(v2+"/header/title", {content: "Alternative Version"})
```

---

## Reading Tools

### batch_get

Read nodes and search for patterns.

```javascript
// List all components in design system
{patterns: [{reusable: true}], searchDepth: 3, readDepth: 2}

// Read specific nodes
{nodeIds: ["frameId1", "frameId2"], readDepth: 2}

// Search by type
{patterns: [{type: "text"}], searchDepth: 2}
```

**Tips**:
- Combine multiple searches in one call
- Use `readDepth: 1-2` to avoid context overflow
- Set `resolveVariables: true` to see computed values

### get_editor_state

Returns active file, selection, and design context. Call first to orient.

### get_screenshot

Capture node as image. **Always verify visual output after batch_design calls.**

### snapshot_layout

Debug layout issues. Use `problemsOnly: true` to find clipping/overlap.

---

## Utility Tools

| Tool | Purpose |
|------|---------|
| `open_document` | Open file or create new (`"new"`) |
| `get_guidelines` | Load topic rules: `landing-page`, `design-system`, `table`, `code`, `tailwind` |
| `get_variables` | Read design tokens and themes |
| `set_variables` | Update tokens (auto-registers new theme axes) |
| `find_empty_space_on_canvas` | Find placement for new frames |
| `replace_all_matching_properties` | Bulk find-and-replace for colors, fonts, etc. |
| `search_all_unique_properties` | Audit unique values across nodes |
| `get_style_guide_tags` | Browse visual style categories |
| `get_style_guide` | Load style guide by tags or name |
