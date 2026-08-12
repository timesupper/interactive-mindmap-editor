---
name: interactive-mindmap-editor
description: Create, repair, and extend standalone interactive HTML mind map editors and XMind-compatible imports/exports. Use when Codex needs to turn user-provided text, Markdown, outlines, articles, book chapters, or notes into editable mind map data/HTML or .xmind files, export plugin JSON to XMind, import .xmind into plugin JSON, or fix editable node titles/subtitles, double-click editing, fullscreen presentation controls, collapse/expand hit areas, node overlap during editing, character-width wrapping, drag/click conflicts, and recursive add/edit/delete child-node behavior in HTML/CSS/JavaScript mind map files.
---

# Interactive Mindmap Editor

## Overview

Use this skill to create or modify standalone HTML mind map editors where nodes are rendered as DOM elements and connected with SVG paths. It supports four related jobs: converting text into a mind map hierarchy, exporting that hierarchy to XMind-compatible `.xmind`, importing `.xmind` back into plugin JSON, and repairing interactive editing/folding/layout behavior in an existing mind map.

## Locating Bundled Scripts

This skill's Python scripts live in a `scripts/` subfolder next to this SKILL.md. Locate them at runtime with the filesystem (e.g. glob from the current working directory for `**/interactive-mindmap-editor/scripts/*.py`, or resolve the plugin install path shown by `codex plugin list`). When Codex runs, the working directory is the project root, not the skill folder, so relative `scripts/...` paths in the examples below are shorthand — expand them to the real path before running.

## Workflow

1. Decide whether the user wants text-to-mindmap creation, XMind export, XMind import, existing-editor repair, or a combination.
2. For existing HTML, locate node rendering, measurement, layout, edit, drag, context-menu, fullscreen, and collapse logic. Search for `createNodeEl`, `refreshNodeEl`, `measure`, `layout`, `relayout`, `beginEdit`, `addChild`, `deleteNode`, `toggleCollapse`, `requestFullscreen`, `fullscreenchange`, `mousedown`, `dblclick`, and `contextmenu`.
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
python scripts/markdown_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"
```

For unstructured long prose, first reason about the hierarchy yourself, then either write the JSON directly or use the script as a rough first pass and refine the output.

## Markdown Import/Export

Convert Markdown or structured text to mind map JSON:

```bash
python scripts/markdown_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"
```

Convert mind map JSON back to a Markdown outline:

```bash
python scripts/mindmap_data_to_markdown.py mindmap-data.json -o outline.md
```

Generated standalone HTML mind maps should include `导入 Markdown` and `导出 Markdown` controls when import/export controls are present.

## Compact Toolbar Menu

When a standalone HTML mind map has many toolbar controls, group secondary actions behind a compact round menu button so the canvas stays readable.

Use this behavior when the toolbar includes several of these controls: `展开`, `折叠`, `导入 Markdown`, `导出 Markdown`, `XMind`, `全屏展示`, and `适配`.

- Place the round menu button directly above the always-visible zoom-in `+` button.
- Keep zoom in, zoom out, and reset view visible as round controls.
- Put secondary actions in a collapsible vertical menu panel.
- Clicking the menu button toggles the secondary action panel.
- Clicking the canvas or any area outside `.controls` should close the menu.
- Preserve existing click and long-press behavior for `展开` and `折叠` inside the menu.
- Preserve import/export, fullscreen, and fit-view behavior after moving buttons into the menu.
- Use `aria-expanded`, `aria-controls`, and `aria-hidden` so the menu state is explicit.

Recommended HTML shape:

```html
<div class="controls">
  <div class="tool-menu" id="toolMenu">
    <div class="tool-menu-panel" id="toolMenuPanel" aria-hidden="true">
      <button id="expandBtn" title="点击展开一级，长按全部展开"><span>＋</span>展开</button>
      <button id="collapseBtn" title="点击折叠一级，长按全部折叠"><span>－</span>折叠</button>
      <button id="importMarkdownBtn" title="导入 Markdown 提纲"><span>⬆</span>导入 Markdown</button>
      <button id="exportMarkdownBtn" title="导出 Markdown 提纲"><span>⬇</span>导出 Markdown</button>
      <button id="xmindBtn" title="导出 XMind 文件"><span>⬇</span>XMind</button>
      <button id="fullscreenBtn" title="全屏展示"><span>⛶</span>全屏展示</button>
      <button id="fitBtn" title="适应画布"><span>⤢</span>适配</button>
    </div>
    <button id="toolMenuBtn" title="展开/折叠工具菜单" aria-expanded="false" aria-controls="toolMenuPanel">☰</button>
  </div>
  <button id="zoomInBtn" title="放大">＋</button>
  <button id="zoomOutBtn" title="缩小">－</button>
  <button id="resetBtn" title="重置视图">↺</button>
</div>
```

Recommended behavior:

```js
const controlsEl = document.querySelector('.controls');
const toolMenuBtn = document.getElementById('toolMenuBtn');
const toolMenuPanel = document.getElementById('toolMenuPanel');

function setToolMenuOpen(open) {
  controlsEl.classList.toggle('menu-open', open);
  toolMenuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  toolMenuPanel.setAttribute('aria-hidden', open ? 'false' : 'true');
}

toolMenuBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  setToolMenuOpen(!controlsEl.classList.contains('menu-open'));
});

window.addEventListener('click', (e) => {
  if (!e.target.closest('.controls')) setToolMenuOpen(false);
});
```

## XMind Export

For XMind export, create modern ZIP-based `.xmind` packages with `content.json`, `metadata.json`, and `manifest.json` at the archive root. Do not wrap those files in a top-level folder.

Use the bundled scripts:

```bash
python scripts/mindmap_data_to_xmind.py mindmap-data.json -o output.xmind
python scripts/text_to_xmind.py input.md -o output.xmind --root-title "主题"
```

Mapping rules:

- Plugin `title` -> XMind topic `title`.
- Plugin `sub` and `note` -> XMind topic `notes.plain.content`.
- Plugin `children` -> XMind `children.attached`.
- Plugin root node -> XMind sheet `rootTopic`.
- Preserve hierarchy and text first; style, icons, colors, callouts, and legacy XMind 8 XML are later-stage features.

When generating `.xmind` from user text, prefer `text_to_xmind.py` for structured Markdown/outlines. For unstructured prose, first refine the hierarchy into plugin JSON, then export with `mindmap_data_to_xmind.py`.

## XMind Import

When users provide `.xmind` files, convert them into plugin JSON with:

```bash
python scripts/xmind_to_mindmap_data.py input.xmind -o mindmap-data.json
```

Import behavior:

- Prefer modern XMind `content.json` packages.
- Fall back to basic legacy `content.xml` parsing when present.
- XMind topic `title` -> plugin `title`.
- XMind notes -> plugin `sub`.
- XMind child topics -> plugin `children`.
- Normalize plugin node `type` as `root`, `part`, `topic`, or `leaf`.
- Assign simple branch colors for HTML compatibility.
- Preserve hierarchy and text first; XMind styling, markers, labels, boundaries, summaries, relationships, and fold states may be ignored unless the user asks for deeper fidelity.

## Injecting Data Into Existing HTML

When updating an existing standalone mind map HTML:

- Locate the root data object, often named `tree`, `treeData`, or similar.
- Replace only the data object when the existing renderer already supports the desired interactions.
- Keep each generated node id unique and stable enough for editing.
- Preserve the existing color palette and branch type conventions when present.
- If the HTML supports import JSON, prefer generating a JSON file and instructing/importing through that path unless the user wants the HTML changed directly.

## Fullscreen Presentation

Generated standalone HTML mind maps should include a toolbar button labeled `全屏展示` unless the user explicitly asks for a minimal export without controls.

- Add a visible toolbar button such as `fullscreenBtn` with a recognizable fullscreen icon plus the text `全屏展示`.
- Use the browser Fullscreen API: call `requestFullscreen()` on the main app/wrap element or `document.documentElement`, and call `document.exitFullscreen()` to exit.
- Listen for `fullscreenchange` so UI state stays correct when the user exits with Esc or browser controls.
- When fullscreen is active, add a class such as `is-fullscreen` to `body` and make the mind map content fill the whole display: set the canvas/wrap region to `position: fixed; inset: 0; width: 100vw; height: 100vh; z-index` above normal page chrome.
- Hide or compress nonessential headers in fullscreen so the mind map content, edges, nodes, toolbar, and viewport occupy the full screen.
- Call the existing `fitView()` or equivalent after entering and after exiting fullscreen, preferably after a short `requestAnimationFrame` delay, so the map is centered in the new viewport.
- Provide a top hover exit control: create a fixed top hover zone that is active only in fullscreen, and reveal an `X`/`×` exit button when the mouse points to the top area of the page.
- Keep the `X` exit button hidden during normal viewing and hidden in fullscreen until the top hover zone is hovered. The button should be keyboard/click accessible and should not overlap editing inputs.
- Do not use the whole top area as a permanent visible bar in fullscreen; it should feel like presentation mode, with only the map visible until the user moves the mouse to the top.
- Keep zoom, pan, editing, import/export, and context menus working after entering and exiting fullscreen.

Recommended HTML/CSS/JS shape:

```html
<button id="fullscreenBtn" title="全屏展示"><span>⛶</span>全屏展示</button>
<div id="fullscreenExitZone" aria-hidden="true">
  <button id="fullscreenExitBtn" title="退出全屏" aria-label="退出全屏">×</button>
</div>
```

```css
#fullscreenExitZone {
  display: none;
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  height: 64px;
  z-index: 1000;
}
body.is-fullscreen #fullscreenExitZone { display: block; }
#fullscreenExitBtn {
  opacity: 0;
  pointer-events: none;
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
}
#fullscreenExitZone:hover #fullscreenExitBtn {
  opacity: 1;
  pointer-events: auto;
}
body.is-fullscreen .mindmap-wrap {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
}
```

```js
function isFullscreen() {
  return document.fullscreenElement || document.webkitFullscreenElement;
}
async function enterFullscreen() {
  const target = document.documentElement;
  if (target.requestFullscreen) await target.requestFullscreen();
  else if (target.webkitRequestFullscreen) target.webkitRequestFullscreen();
  document.body.classList.add('is-fullscreen');
  requestAnimationFrame(() => fitView());
}
async function exitFullscreen() {
  if (document.exitFullscreen) await document.exitFullscreen();
  else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
  document.body.classList.remove('is-fullscreen');
  requestAnimationFrame(() => fitView());
}
document.addEventListener('fullscreenchange', () => {
  document.body.classList.toggle('is-fullscreen', Boolean(isFullscreen()));
  requestAnimationFrame(() => fitView());
});
```

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

### Viewport stability and sibling alignment

- Never run `fitView()` implicitly after drag, reparent, edit, add, delete, note changes, collapse/expand, window resize, or fullscreen changes. Keep the current zoom and viewing position stable.
- Allow full-map fitting only on initial load, after importing a different map, or when the user explicitly chooses `适配`, reset, or `Ctrl+0`.
- Capture an anchor node's screen center before layout/rebuild and restore it afterward by changing only `view.tx`/`view.ty`; do not modify `view.scale`.
- Anchor edits and notes to the changed node, add/delete to the parent, drag/reparent to the moved node, and global collapse/expand to the selected node or root.
- Preserve the map coordinate at the viewport center across window and fullscreen size changes rather than refitting the map.
- Give all direct children of one parent the same X coordinate. Sort them by data order and use constant edge-to-edge vertical spacing, with a larger gap between root-level sections.
- Reparented nodes must be inserted by release Y position before layout, for both ordinary parents and root. Free nodes keep absolute coordinates and do not participate in sibling alignment.

## Collapse And Expand

Collapse/expand should not fire from the whole title area unless the user explicitly wants that.

- Restrict collapse/expand to a small hit area around the right-side arrow/handle.
- Ignore non-left mouse buttons in drag/collapse start logic.
- Keep right-click dedicated to the context menu.
- Store `rec.data.collapsed = rec.collapsed` whenever a node is toggled.
- Before rebuilding the tree after add/delete/import-like operations, persist current collapsed state into each node's data object.
- For global toolbar controls, make short clicks incremental: `展开` should expand only one visible collapsed level, and `折叠` should collapse only the deepest currently visible expanded level.
- Use long press on the same toolbar controls for bulk operations: long-press `展开` should expand all, and long-press `折叠` should collapse all non-root nodes.
- Use a clear long-press threshold such as 600 ms and suppress the following click after the long-press action fires.
- Keep explicit context-menu items such as `全部展开` and `全部折叠` as full-tree operations.

Recommended hit-test shape:

```js
function isToggleHandleHit(rec, clientX, clientY) {
  if (!rec || rec.children.length === 0) return false;
  const rect = rec.el.getBoundingClientRect();
  return clientX >= rect.right - 18 && clientX <= rect.right + 18 &&
    clientY >= rect.top && clientY <= rect.bottom;
}
```

Recommended one-level toolbar behavior:

```js
function expandOneLevel() {
  const targets = Object.values(nodes).filter(rec =>
    rec.children.length > 0 && rec.collapsed && isNodeVisible(rec)
  );
  targets.forEach(rec => { rec.collapsed = false; rec.data.collapsed = false; });
  if (targets.length) { saveCollapsedState?.(); relayout(true); }
}

function collapseOneLevel() {
  const candidates = Object.values(nodes).filter(rec =>
    rec !== rootNode && rec.children.length > 0 && !rec.collapsed && isNodeVisible(rec)
  );
  if (!candidates.length) return;
  const deepest = Math.max(...candidates.map(rec => rec.depth));
  candidates
    .filter(rec => rec.depth === deepest)
    .forEach(rec => { rec.collapsed = true; rec.data.collapsed = true; });
  saveCollapsedState?.();
  relayout(true);
}
```

## Adding, Editing, And Deleting Hierarchy

## Free-Floating Titles

When a node is dragged far enough from its current parent, make it a free-floating title:

- Use a pointer displacement threshold, default `180px`, to enter free mode. A short press or a brief hold alone must not detach the node.
- Store detached nodes in root-level `freeNodes`, not in `root.children`; set `freePosition: {x, y}` and keep the node's children with it.
- Free nodes have no parent and no connector to the tree. Render them at their saved absolute coordinates with a visible dashed/gold free-state style.
- While dragging, only preview a possible new parent. On release, attach to a nearby valid node only within `130px`; otherwise retain the free node unchanged.
- Treat siblings as valid parent targets. Approaching a sibling highlights it and draws a blue dashed target connector; releasing there makes the dragged node its child.
- Once pointer displacement exceeds the `180px` detach threshold, hide the original solid parent edge and draw a gold dashed edge from the original parent to the moving node until release. Do not mutate hierarchy during this preview.
- Use `130px` to acquire a target and approximately `155px` to release the current target, preventing target highlight flicker at the boundary.
- Exclude hidden, editing, free, dragged, and descendant nodes from targets. Clear preview edges and highlights on release, cancellation, and pinch-zoom takeover.
- Moving a free node into a target removes it from `freeNodes` and appends it to `target.children`. Moving it into empty space keeps it independent and persistent after reload.
- Exclude the dragged node and its descendants from valid targets. Keep the root as a valid target; releasing near it moves the node into `root.children` as a top-level section at the release Y position. Never create a cycle.
- After release, select the moved node without opening its editor automatically, preserve the current viewport and zoom, and apply only the minimum layout adjustment needed to keep the moved subtree usable.

Recommended root data extension:

```js
{
  ...root,
  children: [/* hierarchical nodes */],
  freeNodes: [
    { id: 'free-1', title: '独立标题', free: true,
      freePosition: { x: 420, y: 180 }, children: [] }
  ]
}
```

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
- Generated `.xmind` packages contain root-level `content.json`, `metadata.json`, and `manifest.json`.
- Imported `.xmind` files produce plugin JSON with `root -> part -> topic -> leaf` node types.
- Generated HTML includes a `全屏展示` toolbar button, uses Fullscreen API when available, fills the display in fullscreen mode, and reveals an `X`/`×` exit button only when the mouse points to the top area.
- Double-click title and subtitle both enter the same two-line editor.
- Repeated double-click does not add extra rows.
- Moving focus from title to subtitle does not save early.
- Long text wraps around the requested character width and does not turn vertical.
- Editing or typing pushes nearby nodes away and does not obscure other titles.
- Only the arrow/handle area toggles collapse; title clicks do not.
- Toolbar short-click expand/collapse changes one level only; toolbar long-press expands/collapses all.
- Right-click opens the context menu without toggling collapse.
- Adding a child to a leaf works, and the new child can itself receive children.
- Adding or deleting nodes preserves unrelated branch collapse states.
- Dragging a node far enough detaches it; release near a valid node reparents it, and release in empty space preserves it as a free node after reopening the page.
