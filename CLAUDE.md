# Claude Code Guide

This repository is a multi-entry mind map toolkit that runs on **Claude Desktop, Claude Code (CLI), Codex Desktop, and Codex CLI**:

- **Claude Code (CLI)** reads this `CLAUDE.md` when working inside this repository, and installs the skill via root `SKILL.md`.
- **Claude Desktop** installs the same skill by uploading a `.zip` of this folder in Settings → Features → Skills.
- **Codex** uses `.codex-plugin/plugin.json` and `skills/interactive-mindmap-editor/SKILL.md`, installed as a personal plugin.
- All entry points share the same scripts under `skills/interactive-mindmap-editor/scripts/`.

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
python -m py_compile .\skills\interactive-mindmap-editor\scripts\*.py
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

## Skill Script Paths

When the skill runs under Claude Code as an installed skill, reference bundled scripts with `${CLAUDE_SKILL_DIR}/scripts/...`. That substitution expands to the skill's own folder regardless of where it was installed (`~/.claude/skills/`, project `.claude/skills/`, or a plugin). Under Codex, the skill runs from its own directory, so relative `scripts/...` paths are correct.

## Git Notes

- Keep Codex plugin files and Claude support files in the same repository.
- Do not remove `.codex-plugin/` or `skills/`; Claude support is additive.
- Update `README.md`, `USAGE.md`, and `CHANGELOG.md` when behavior changes.
