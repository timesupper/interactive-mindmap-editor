---
name: interactive-mindmap-editor
description: Create, repair, and extend standalone interactive HTML mind map editors. Use when Codex needs to turn user-provided text, Markdown, outlines, articles, book chapters, or notes into editable mind map data/HTML, or fix editable node titles/subtitles, double-click editing, collapse/expand hit areas, node overlap during editing, character-width wrapping, drag/click conflicts, and recursive add/edit/delete child-node behavior in HTML/CSS/JavaScript mind map files.
---

# Interactive Mindmap Editor

## Overview

Use this skill to create or modify standalone HTML mind map editors where nodes are rendered as DOM elements and connected with SVG paths. It supports two related jobs: converting text into a mind map hierarchy, and repairing interactive editing/folding/layout behavior in an existing mind map.

## Workflow

1. Decide whether the user wants text-to-mindmap creation, existing-editor repair, or both.
2. For existing HTML, locate node rendering, measurement, layout, edit, drag, context-menu, and collapse logic. Search for `createNodeEl`, `refreshNodeEl`, `measure`, `layout`, `relayout`, `beginEdit`, `addChild`, `deleteNode`, `toggleCollapse`, `mousedown`, `dblclick`, and `contextmenu`.
3. Confirm the data model before changing behavior. Check whether nodes store `id`, `title`, `sub`, `type`, `color`, `children`, and `collapsed`.
4. Keep edits scoped. Preserve the existing visual language and engine unless the user asks for a new app.
5. After editing, inspect modified snippets and search for stale duplicate logic.

## Text To Mind Map

When the user supplies text and asks for a mind map, produce a tree using this node shape:

```js
{
  id: 'root',
  title: '主题',
  sub: '可选副标题',
  type: 'root',
  color: '#2b2620',
  children: [
    { id: 'n1', title: '一级节点', sub: '摘要', type: 'part', color: '#c24a34', children: [] }
  ]
}
```

Use these extraction rules:

- Preserve explicit headings, numbering, bullets, indentation, and Markdown hierarchy when present.
- For prose, infer 3-7 first-level branches from recurring themes, argument flow, chronology, or section transitions.
- Use `title` for the concise node label and `sub` for a short explanation or evidence.
- Keep titles short enough to scan; let CSS wrapping handle display length.
- Assign `type: root` to the root, `part` to first-level children, `topic` to internal non-root nodes, and `leaf` to terminal nodes.
- Use consistent colors by top-level branch and inherit colors downward.
- Do not fabricate unsupported claims. If the text is ambiguous, create broader nodes instead of over-specific leaves.

For structured Markdown/outlines, use the bundled script instead of hand-writing parsing logic:

```bash
python scripts/text_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"
```

For unstructured long prose, first reason about the hierarchy yourself, then either write the JSON directly or use the script as a rough first pass and refine the output.

## Injecting Data Into Existing HTML

When updating an existing standalone mind map HTML:

- Locate the root data object, often named `tree`, `treeData`, or similar.
- Replace only the data object when the existing renderer already supports the desired interactions.
- Keep each generated node id unique and stable enough for editing.
- Preserve the existing color palette and branch type conventions when present.
- If the HTML supports import JSON, prefer generating a JSON file and instructing/importing through that path unless the user wants the HTML changed directly.

## Editing Nodes

For two-line node editors, treat the first line as `title` and the second line as `sub`.

- Do not create extra title/subtitle rows on repeated double-click.
- If the node is already editing, refocus the existing title field instead of rebuilding the editor.
- Clean stale `.n-edit-input`, duplicate `.n-sub`, and legacy `.n-tag` elements when refreshing a node.
- Use `focusout` on the whole node, not `blur` on individual fields, so moving from title to subtitle does not commit early.
- Ignore `mousedown` and `dblclick` that originate inside edit fields, so text selection does not start dragging or rebuild editing controls.
- Use `textarea` instead of single-line `input` when text should wrap while editing.

Recommended pattern:

```js
if (editingId === id && rec.el.classList.contains('editing')) {
  rec.el.querySelector('.n-edit-input[data-field="title"]')?.focus();
  return;
}

const onFocusOut = () => {
  setTimeout(() => {
    if (editingId === id && !rec.el.contains(document.activeElement)) finish(true);
  }, 0);
};
```

## Text Length And Wrapping

When the user asks for a character-based line limit, prefer width by character units, not content truncation.

- Use `max-width: 30em` or a CSS variable such as `--node-line-chars: 30em` for approximately 30 Chinese characters per line.
- Do not use `maxlength` unless the user explicitly asks to cap total stored text.
- Keep `white-space: normal` and `overflow-wrap: anywhere` on displayed title/subtitle text.
- Use `width: max-content` plus `max-width` for compact nodes that grow until the character-width limit.
- In edit mode, set the editing node width to the same character-width limit so editing and saved display match.

## Layout And Overlap

Editing can change node width and height. Re-measure and re-layout immediately after inserting edit fields and while text changes.

- Raise the editing node with a temporary `z-index` so it is never hidden during animated transitions.
- Call the existing `relayout(false)` on input changes for immediate collision avoidance.
- Call the existing animated relayout only when finishing edits or when fold/unfold behavior changes.
- Preserve the existing `measure -> layout -> assignAbs -> updatePositions -> renderEdges` flow when present.

## Collapse And Expand

Collapse/expand should not fire from the whole title area unless the user explicitly wants that.

- Restrict collapse/expand to a small hit area around the right-side arrow/handle.
- Ignore non-left mouse buttons in drag/collapse start logic.
- Keep right-click dedicated to the context menu.
- Store `rec.data.collapsed = rec.collapsed` whenever a node is toggled.
- Before rebuilding the tree after add/delete/import-like operations, persist current collapsed state into each node's data object.

Recommended hit-test shape:

```js
function isToggleHandleHit(rec, clientX, clientY) {
  if (!rec || rec.children.length === 0) return false;
  const rect = rec.el.getBoundingClientRect();
  return clientX >= rect.right - 18 && clientX <= rect.right + 18 &&
    clientY >= rect.top && clientY <= rect.bottom;
}
```

## Adding, Editing, And Deleting Hierarchy

All visible node levels should support add/edit/delete unless the product explicitly protects the root.

- Right-click on any non-root node should expose edit, add child, notes if present, and delete.
- Right-click on the root may expose edit and add top-level section; deletion should normally remain disabled for root.
- When adding a child to a leaf node, initialize `parent.data.children = []` and upgrade the parent type from `leaf` to `topic` or the local equivalent.
- Only expand the parent receiving the new child. Do not expand unrelated branches.
- Create new non-root descendants as leaf nodes by default; they can be upgraded when they later receive children.
- After adding, rebuild from data and enter edit mode on the new node.

Recommended add-child guard:

```js
persistCollapsedState();
if (!Array.isArray(parent.data.children)) parent.data.children = [];
if (!isRootChild && parent.data.type === 'leaf') parent.data.type = 'topic';
parent.data.collapsed = false;
parent.collapsed = false;
```

## Verification Checklist

After changes, verify these behaviors in the local file or browser:

- User text becomes a coherent `root -> part -> topic -> leaf` tree.
- Generated titles and subtitles are concise and faithful to the source text.
- Generated JSON can be imported or assigned to the HTML data object without syntax errors.
- Double-click title and subtitle both enter the same two-line editor.
- Repeated double-click does not add extra rows.
- Moving focus from title to subtitle does not save early.
- Long text wraps around the requested character width and does not turn vertical.
- Editing or typing pushes nearby nodes away and does not obscure other titles.
- Only the arrow/handle area toggles collapse; title clicks do not.
- Right-click opens the context menu without toggling collapse.
- Adding a child to a leaf works, and the new child can itself receive children.
- Adding or deleting nodes preserves unrelated branch collapse states.
