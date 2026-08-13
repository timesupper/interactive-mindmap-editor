---
name: interactive-mindmap-editor
description: Create, repair, present, import, and export interactive HTML mind maps, Markdown outlines, and XMind-compatible files. Use when Claude needs to turn text, Markdown, outlines, articles, book chapters, or notes into editable mind map data/HTML, Markdown outlines, or .xmind files; export JSON to Markdown/XMind; import Markdown/.xmind into JSON; or fix mind map HTML behavior including double-click editing, compact toolbar menus, fullscreen presentation, collapse/expand hit areas, node overlap, character-width wrapping, drag/click conflicts, and recursive add/edit/delete child nodes. Chinese triggers include 生成思维导图, 把文本变成思维导图, 导入 Markdown, 导出 Markdown, 导出 XMind, 导入 xmind, 修复思维导图, 编辑思维导图节点.
---

# Interactive Mindmap Editor

This is the Claude Skill entry point for the same toolkit that Codex loads through `.codex-plugin/plugin.json` and `skills/interactive-mindmap-editor/SKILL.md`.

## Use Cases

Use this skill for:

- Text, Markdown, outlines, notes, articles, or chapters to mind map JSON.
- Mind map JSON to Markdown outline.
- Mind map JSON or text/Markdown to XMind `.xmind`.
- XMind `.xmind` to editable mind map JSON.
- Standalone editable HTML mind map creation or repair.
- HTML interaction fixes for two-line editing, folding, fullscreen, compact toolbar menus, wrapping, overlap, drag, and recursive hierarchy editing.

## Core Data Shape

Use this node structure:

```json
{
  "id": "root",
  "title": "主题",
  "sub": "可选副标题",
  "type": "root",
  "color": "#2b2620",
  "children": []
}
```

Type rules:

- `root`: root node.
- `part`: first-level children.
- `topic`: non-root internal nodes.
- `leaf`: terminal nodes.

## Scripts

Run scripts from the repository root.

Markdown/text to mind map JSON:

```bash
python skills/interactive-mindmap-editor/scripts/markdown_to_mindmap_data.py input.md -o mindmap-data.json --root-title "主题"
```

Mind map JSON to Markdown:

```bash
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_markdown.py mindmap-data.json -o outline.md
```

Mind map JSON to XMind:

```bash
python skills/interactive-mindmap-editor/scripts/mindmap_data_to_xmind.py mindmap-data.json -o output.xmind
```

Markdown/text directly to XMind:

```bash
python skills/interactive-mindmap-editor/scripts/text_to_xmind.py input.md -o output.xmind --root-title "主题"
```

XMind to mind map JSON:

```bash
python skills/interactive-mindmap-editor/scripts/xmind_to_mindmap_data.py input.xmind -o mindmap-data.json
```

## HTML Repair Rules

When creating or repairing standalone HTML mind maps:

- Preserve two-line editing: `title` on the first line and `sub` on the second line.
- Repeated double-click must not create extra edit rows.
- Restrict collapse/expand to the right-side arrow or handle hit area.
- Use right mouse drag for whole-page panning when requested; avoid left-click panning conflicts.
- Wrap long text by character-width; do not truncate stored text unless explicitly requested.
- Re-measure and re-layout while editing so nodes do not overlap.
- Support add child, edit, and delete for all non-root visible levels.
- Adding a child should expand only the target parent, not unrelated branches.
- Persist collapse/expand state across page reloads.
- Toolbar `展开` and `折叠` short-click should change one visible level; long-press should expand/collapse all.
- If many controls exist, group secondary actions behind a round menu button above the visible zoom-in `+` button.
- Keep zoom in, zoom out, and reset visible as round controls.
- Include `导入 Markdown` and `导出 Markdown` when import/export controls are present.
- Route JSON, Markdown, and XMind export through one `showSaveFilePicker` flow. Open it directly from the click, use one stable picker id, persist the last successful file handle, pass it back as `startIn`, save without a second confirmation, cancel without fallback download, and hide the success notice after three seconds.
- Include `全屏展示`; fullscreen should fill the display and show an `X`/`×` exit control only when the pointer reaches the top area.
- Keep global numbering actions in the right-click context menu: apply all numbering, renumber all, and clear all numbering. Persist the enabled state and renumber after structural changes and imports.
- For Markmap previews, render standard Markdown list markers even when the editor displays hierarchical numbering; validate SVG dimensions before initialization and dispose pending transitions, observers, timers, and render tasks on close for Chrome/Edge compatibility.

## Platform Notes

- In Claude, this root `SKILL.md` is the portable skill entry when this repository is installed as a personal or project skill folder.
- In Claude Code project mode, `CLAUDE.md` gives additional repository-level instructions.
- In Codex, use `skills/interactive-mindmap-editor/SKILL.md`; do not remove the Codex skill folder.
