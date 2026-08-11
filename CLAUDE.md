# Claude Code Guide

This repository is a multi-entry mind map toolkit:

- Codex uses `.codex-plugin/plugin.json` and `skills/interactive-mindmap-editor/SKILL.md`.
- Claude Skill installs use root `SKILL.md`.
- Claude Code project memory uses this `CLAUDE.md`.
- Shared scripts live under `skills/interactive-mindmap-editor/scripts/`.

## Purpose

Use this project to create, repair, import, and export editable standalone HTML mind maps, Markdown outlines, and XMind-compatible `.xmind` files.

## Core Data Shape

Mind map JSON should use this shape:

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

Node rules:

- Root node type is `root`.
- First-level children use `part`.
- Internal non-root nodes use `topic`.
- Terminal nodes use `leaf`.
- Prefer `title` for concise labels and `sub` for short explanations.

## Commands

Run commands from the repository root.

Markdown outline to mind map JSON:

```powershell
python .\skills\interactive-mindmap-editor\scripts\markdown_to_mindmap_data.py .\input.md -o .\mindmap-data.json --root-title "主题"
```

Mind map JSON to Markdown outline:

```powershell
python .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_markdown.py .\mindmap-data.json -o .\outline.md
```

Mind map JSON to XMind:

```powershell
python .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_xmind.py .\mindmap-data.json -o .\output.xmind
```

Markdown or structured text directly to XMind:

```powershell
python .\skills\interactive-mindmap-editor\scripts\text_to_xmind.py .\input.md -o .\output.xmind --root-title "主题"
```

XMind to mind map JSON:

```powershell
python .\skills\interactive-mindmap-editor\scripts\xmind_to_mindmap_data.py .\input.xmind -o .\mindmap-data.json
```

Validate Python scripts:

```powershell
python -m py_compile .\skills\interactive-mindmap-editor\scripts\markdown_to_mindmap_data.py .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_markdown.py .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_xmind.py .\skills\interactive-mindmap-editor\scripts\text_to_xmind.py .\skills\interactive-mindmap-editor\scripts\xmind_to_mindmap_data.py
```

## HTML Mind Map Rules

When creating or repairing standalone HTML mind maps:

- Preserve two-line editing: first line edits `title`, second line edits `sub`.
- Repeated double-click must not create extra edit rows.
- Collapse/expand should only trigger from the right-side arrow or handle area.
- Right mouse drag pans the page; left click should not pan the whole page.
- Long text should wrap by character-width, not by truncating stored text.
- Editing a node should re-layout nearby nodes so titles do not overlap.
- All non-root visible levels should support add child, edit, and delete.
- Adding a child should expand only the target parent, not unrelated branches.
- Persist collapse/expand state so reopening the page restores the previous state.
- Toolbar `展开` and `折叠` short-click should change one level; long-press should expand/collapse all.
- If there are many toolbar controls, group secondary actions behind a round menu button above the visible zoom-in `+` button.
- Keep zoom in, zoom out, and reset view visible as round controls.
- Generated HTML with import/export controls should include `导入 Markdown` and `导出 Markdown`.
- Generated HTML should include `全屏展示`; fullscreen should fill the display and reveal an `X`/`×` exit button only when the mouse points to the top area.

## Git Notes

- Keep Codex plugin files and Claude support files in the same repository.
- Do not remove `.codex-plugin/` or `skills/`; Claude support is additive.
- Update `README.md`, `USAGE.md`, and `CHANGELOG.md` when behavior changes.

## Installation And Portability

For Codex:

- Install once per machine as a personal plugin.
- After installation, any Codex project/task can use the plugin without copying this repository into each project.
- To pin a project to a specific version, clone this repository into that project and ask Codex to use scripts from that path.

For Claude:

- Install as a personal skill by placing this repository at `$HOME\.claude\skills\interactive-mindmap-editor`.
- Install as a project skill by placing this repository at `<project>\.claude\skills\interactive-mindmap-editor`.
- Use personal skill for shared global behavior; use project skill when a project must carry its own pinned copy.
- Keep `SKILL.md` at the skill folder root; Claude uses it as the skill entry.

When migrating mind map work between projects:

- Move `.html`, `.json`, `.md`, and `.xmind` artifacts with the target project.
- Keep this repository installed globally in Codex/Claude when possible.
- If the target environment cannot install global skills/plugins, copy this repository into the project's `.claude\skills\interactive-mindmap-editor` folder for Claude or into `$HOME\plugins\interactive-mindmap-editor` for Codex.
