---
name: interactive-mindmap-editor
description: Create, repair, present, import, and export interactive HTML mind maps (思维导图), Markdown/Markmap outlines, and XMind-compatible files. Use whenever the user wants to turn text, Markdown, Markmap outlines, articles, book chapters, or notes into an editable mind map (HTML or .xmind), generate mind map JSON data, import .xmind files back into JSON, export JSON to Markdown/Markmap/XMind, or repair an existing interactive HTML mind map editor, including node double-click editing, fullscreen presentation controls, collapse/expand hit areas, node overlap during editing, character-width text wrapping, drag/click conflicts, and recursive add/edit/delete of child nodes. Trigger on Chinese requests like 生成思维导图, 把这段文字做成思维导图, 导出 XMind, 导入 xmind, 导出 Markmap, 导入 Markmap, 修复思维导图, 编辑思维导图节点.
---

# Interactive Mindmap Editor

## Execution Constraints

Before and after any task, read [SKILL_CONSTRAINTS.md](SKILL_CONSTRAINTS.md). It is the source of truth for supported capabilities, performance requirements, missing Markmap scripts, and the execution/acceptance checklists. Do not claim a conversion script exists unless its file is present in the repository.

## Overview

Use this skill to create or modify standalone interactive HTML mind map editors (nodes rendered as DOM elements, connected with SVG paths) and to convert between plain text, Markdown, Markmap-compatible Markdown, mind map JSON, and XMind `.xmind` packages. It supports six related jobs:

1. **Text → mind map**: turn prose, Markdown, outlines, articles, or notes into a hierarchical mind map data object.
2. **HTML generation**: produce standalone editable HTML mind maps with editing, folding, layout, and fullscreen controls.
3. **Markdown / Markmap interchange**: convert outlines to and from the canonical mind map JSON.
4. **XMind export**: write mind map JSON (or text directly) to XMind-compatible `.xmind` packages.
5. **XMind import**: read `.xmind` files back into mind map JSON.
6. **Repair**: fix editing, folding, layout, overlap, drag, and hierarchy behavior in an existing HTML mind map.

## Scripts

Bundled Python scripts live in the skill folder. When this repository is installed as a Claude skill, the skill root is the repository root and the scripts sit under `skills/interactive-mindmap-editor/scripts/`. Reference them through `${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/`, which expands to the real location no matter where the skill is installed (personal `~/.claude/skills/`, project `.claude/skills/`, or a plugin). Do not use bare relative paths like `scripts/...` — the working directory is the project root, not the skill folder, so they would fail. Python is required on PATH.

```bash
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/text_to_mindmap_data.py" input.md -o mindmap-data.json --root-title "主题"
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/markdown_to_mindmap_data.py" input.md -o mindmap-data.json --root-title "主题"
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/mindmap_data_to_markdown.py" mindmap-data.json -o outline.md
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/markmap_markdown_to_mindmap_data.py" markmap.md -o mindmap-data.json
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/mindmap_data_to_markmap_markdown.py" mindmap-data.json -o markmap.md
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/render_markmap_html.py" mindmap-data.json -o output/markmap.html --template "${CLAUDE_SKILL_DIR}/templates/interactive-mindmap.html" --runtime "${CLAUDE_SKILL_DIR}/runtime/markmap-preview.js" --assets "${CLAUDE_SKILL_DIR}/runtime/markmap-assets.js" --styles "${CLAUDE_SKILL_DIR}/runtime/markmap-preview.css"
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/mindmap_data_to_xmind.py" mindmap-data.json -o output.xmind
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/text_to_xmind.py" input.md -o output.xmind --root-title "主题"
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/xmind_to_mindmap_data.py" input.xmind -o mindmap-data.json
```

If `${CLAUDE_SKILL_DIR}` does not resolve (older Claude Code), instead locate the script by globbing for `**/interactive-mindmap-editor/scripts/*.py` from the current project root.

## Workflow

1. Decide which job the user wants: text-to-mindmap creation, HTML generation, Markdown/Markmap interchange, XMind export, XMind import, existing-editor repair, or a combination.
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
- For prose, infer 3–7 first-level branches from recurring themes, argument flow, chronology, or section transitions.
- Use `title` for the concise node label and `sub` for a short explanation or evidence.
- Keep titles short enough to scan; let CSS wrapping handle display length.
- Assign `type: root` to the root, `part` to first-level children, `topic` to internal non-root nodes, and `leaf` to terminal nodes.
- Use consistent colors by top-level branch and inherit colors downward.
- Do not fabricate unsupported claims. If the text is ambiguous, create broader nodes instead of over-specific leaves.

For structured Markdown/outlines, use the bundled script instead of hand-writing parsing logic:

```bash
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/markdown_to_mindmap_data.py" input.md -o mindmap-data.json --root-title "主题"
```

For unstructured long prose, first reason about the hierarchy yourself, then either write the JSON directly or use the script as a rough first pass and refine the output.

## Generating Standalone HTML

When generating an HTML mind map, embed the tree data in the page and implement at minimum:

- Node rendering as DOM elements with SVG connector paths.
- Double-click editing of `title` and `sub` (two-line editor).
- Context menu on right-click: edit, add child, add/edit note, delete.
- Collapse/expand via a small right-side arrow hit area (not the whole title).
- Drag-and-drop layout with collision avoidance.
- `全屏展示` fullscreen toolbar button.
- Toolbar expand/collapse that works one level per short click, all levels on long-press.
- Import/export of JSON and Markdown.
- Right-drag pans the page; left click does not pan.
- If there are many toolbar controls, group secondary actions (展开, 折叠, 导入 Markdown, 导出 Markdown, XMind, 全屏展示, 适配) behind a compact round menu button placed above the visible zoom-in `+` button; keep zoom in, zoom out, and reset view visible as round controls.

For the canonical data shape and interaction details, follow the sections below. The local `00_序言/序言思维导图.html` file in the project is a full working reference implementation.

## Markdown Import/Export

Convert Markdown or structured text to mind map JSON:

```bash
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/markdown_to_mindmap_data.py" input.md -o mindmap-data.json --root-title "主题"
```

Convert mind map JSON back to a Markdown outline:

```bash
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/mindmap_data_to_markdown.py" mindmap-data.json -o outline.md
```

Generated standalone HTML mind maps should include `导入 Markdown` and `导出 Markdown` controls when import/export controls are present.

## Markmap Interchange

For a standalone offline preview, use `render_markmap_html.py` with the bundled template, runtime, CSS, and embedded assets. Do not replace the embedded assets with a CDN URL when the output must open by double-clicking a local HTML file.

Use Markmap as a Markdown-based interchange and preview layer, not as a replacement for the existing editor.

Convert Markmap-compatible Markdown to mind map JSON:

```bash
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/markmap_markdown_to_mindmap_data.py" markmap.md -o mindmap-data.json
```

Convert mind map JSON to Markmap-compatible Markdown:

```bash
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/mindmap_data_to_markmap_markdown.py" mindmap-data.json -o markmap.md
```

Rules:

- Reuse Markdown hierarchy as the interchange format.
- Preserve root title, nested structure, titles, subtitles, and note text where practical.
- Treat editor-only state such as `collapsed`, `freePosition`, and viewport data as non-round-trippable through Markmap.
- Export `freeNodes` as a separate `## 自由标题` section when present.
- For standalone HTML preview mode, prefer embedded offline Markmap rendering, and fall back to a local tree preview only when the embedded libraries are missing or fail to initialize.`r`n- When a Markmap preview toolbar has many actions, it may use a single hover-open menu button instead of two fixed button rows.`r`n- The Markmap preview may persist the active preview page plus the last expand-level state across reopen.`r`n- The Markmap preview may map fold controls to level-based behavior: single click collapses one level, double click restores one level, and long press toggles between fully collapsed and fully expanded.`r`n- A single Markmap fullscreen button may toggle between `全屏` and `退出全屏` labels based on current fullscreen state.

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
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/mindmap_data_to_xmind.py" mindmap-data.json -o output.xmind
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/text_to_xmind.py" input.md -o output.xmind --root-title "主题"
```

Mapping rules:

- Plugin `title` → XMind topic `title`.
- Plugin `sub` and `note` → XMind topic `notes.plain.content`.
- Plugin `children` → XMind `children.attached`.
- Plugin root node → XMind sheet `rootTopic`.
- Preserve hierarchy and text first; style, icons, colors, callouts, and legacy XMind 8 XML are later-stage features.

When generating `.xmind` from user text, prefer `text_to_xmind.py` for structured Markdown/outlines. For unstructured prose, first refine the hierarchy into plugin JSON, then export with `mindmap_data_to_xmind.py`.

## XMind Import

When users provide `.xmind` files, convert them into mind map JSON with:

```bash
python "${CLAUDE_SKILL_DIR}/skills/interactive-mindmap-editor/scripts/xmind_to_mindmap_data.py" input.xmind -o mindmap-data.json
```

Import behavior:

- Prefer modern XMind `content.json` packages.
- Fall back to basic legacy `content.xml` parsing when present.
- XMind topic `title` → node `title`.
- XMind notes → node `sub`.
- XMind child topics → node `children`.
- Normalize node `type` as `root`, `part`, `topic`, or `leaf`.
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

- Do not call `fitView()` after dragging, reparenting, editing, adding, deleting, annotating, folding, expanding, resizing the window, or entering/exiting fullscreen. These operations must not change the user's zoom level or automatically center the whole map.
- Reserve `fitView()` for initial page load, importing a new map, and explicit user commands such as `适配`, reset view, or `Ctrl+0`.
- Before a layout or tree rebuild, capture the screen position of an operation anchor; after layout, compensate only `view.tx` and `view.ty` so the anchor stays in the same screen position. Never change `view.scale` during anchor restoration.
- Use the edited node as the anchor for text and note changes, the parent for add/delete, the dragged node for reparent/detach, and the selected node (or root) for global fold/expand.
- On window or fullscreen size changes, preserve the map coordinate under the old viewport center and restore it under the new viewport center without fitting the whole map.
- Align direct siblings to the same X coordinate and arrange them vertically in data order with a constant gap. Use a smaller normal sibling gap and a larger root-section gap; node height may vary, but the edge-to-edge gap must remain constant.
- When a dragged node is attached to any parent, including root, insert it among direct siblings by release Y position before layout. Let the normal layout provide left alignment and equal spacing.
- Free nodes remain outside tree alignment. Keep their absolute positions and only resolve actual overlap; do not move unrelated tree branches or center the viewport.

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

Generated HTML mind maps should support detaching a node into a free-floating title during drag:

- Start a left-button drag on a non-root node; a click without movement keeps the normal select/edit/collapse behavior.
- A node becomes free only after its pointer displacement from the drag start reaches the configured detach threshold (default `180px`). Do not use a short long-press timer as the detach trigger.
- While free, show a dashed/gold visual state and keep the node at the dragged coordinates. It must not remain in `root.children`, must not inherit a parent, and must not draw a connector to the root or another node.
- Persist free nodes in a dedicated root-level `freeNodes` array. Store their current coordinates in `freePosition: {x, y}` so rebuilding or reopening the HTML preserves the free state.
- During a free drag, highlight a nearby valid node as a pending reparent target. Do not change the data hierarchy while the pointer is moving.
- A sibling node is a valid new parent. When the dragged title approaches a sibling, highlight that sibling and show a blue dashed preview connector; on release, attach the dragged title beneath that sibling instead of returning it to their shared parent.
- Before the pointer is released, crossing the detach threshold must hide the original solid parent connector and replace it with a gold dashed connector from the original parent to the moving title. This is a preview only; keep the original hierarchy intact until release.
- Use target hysteresis to avoid flicker: enter a target around `130px`, but keep the current target until the pointer moves beyond about `155px`.
- When a different target is previewed, hide the original solid connector and show only the target preview connector. Clear every preview connector and target highlight on release, cancellation, or a switch to pinch zoom.
- On pointer release, attach the free node to the highlighted nearby node only when it is within the attach threshold (default `130px`). Otherwise keep it free in `freeNodes`.
- Moving a free node to another title removes it from `freeNodes` and appends it to the target's `children`; moving it to empty space leaves it independent.
- Exclude the dragged node and its descendants from reparent target selection. The root remains a valid target: releasing near it should insert the node into `root.children` as a top-level section, ordered by the release Y position. Never create a cycle.
- After a drag release, select the moved node but do not automatically enter edit mode. Refit the view after hierarchy changes so the moved node and its descendants remain fully visible.
- Keep free-node coordinates outside the normal tree layout and include them in content bounds, collision checks, save/load, Markdown export, and XMind export according to the chosen fallback policy. The default export policy is to serialize free nodes as top-level entries with an explicit `free: true` marker or note rather than silently attaching them.

Recommended state shape:

```js
{
  ...root,
  children: [/* attached hierarchy */],
  freeNodes: [
    {
      id: 'free-1',
      title: '独立标题',
      freePosition: { x: 420, y: 180 },
      free: true,
      children: []
    }
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

## Notes (批注)

- Allow adding/editing a `note` string per node; when present, render a small badge (e.g. `📝`) on the node.
- Open a modal/popup to view and edit the note; store the value in `node.data.note`.
- Persist `note` through JSON export/import and map it to XMind notes on export.

## Global numbering and browser compatibility

Keep `全部自动编号`, `重编全部编号`, and `取消全部编号` in the right-click context menu, including the canvas background. Persist the enabled state and renumber after structural changes and imports. Markmap preview input must use standard `-` list markers, validate finite SVG dimensions before initialization, and dispose pending render work on close or rebuild for Chrome/Edge compatibility.

## Verification Checklist

After changes, verify these behaviors in the local file or browser:

- User text becomes a coherent `root -> part -> topic -> leaf` tree.
- Generated titles and subtitles are concise and faithful to the source text.
- Generated JSON can be imported or assigned to the HTML data object without syntax errors.
- Generated `.xmind` packages contain root-level `content.json`, `metadata.json`, and `manifest.json`.
- Imported `.xmind` files produce mind map JSON with `root -> part -> topic -> leaf` node types.
- Generated HTML includes a `全屏展示` toolbar button, uses the Fullscreen API when available, fills the display in fullscreen mode, and reveals an `X`/`×` exit button only when the mouse points to the top area.
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
- Dragging a node beyond the detach threshold makes it independent; releasing near a valid title reparents it, while releasing in empty space keeps it in `freeNodes` after reload.


