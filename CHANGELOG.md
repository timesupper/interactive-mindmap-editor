# Changelog

## 0.3.1+dual.20260811 - 2026-08-11

- Add Claude Skill compatibility: root-level `SKILL.md` with Claude-style frontmatter and Chinese trigger words.
- Add `install-codex.ps1` one-click install script for Codex (copies to plugins dir, registers marketplace, installs plugin).
- Update README to document the dual-compatible (Claude Skill + Codex plugin) directory layout.
- Keep original Codex plugin structure unchanged under `skills/interactive-mindmap-editor/` and `.codex-plugin/`.

## 0.3.0+codex.20260811163605 - 2026-08-11

- Document fullscreen presentation requirements for future generated HTML mind maps.
- Require a `全屏展示` toolbar button, full-screen content layout, and a top-hover `X` exit button.
- Document incremental toolbar expand/collapse behavior: short-click changes one level, long-press changes all levels.

## 0.2.1+codex.20260811111423 - 2026-08-11

- Clarified new-system installation steps for Codex App and Codex CLI.
- Documented `codex plugin marketplace add "$HOME"` for registering the personal marketplace root.
- Replaced marketplace setup examples with UTF-8 without BOM PowerShell writing logic.
- Added troubleshooting notes for `plugin was not found in marketplace personal` and invalid marketplace JSON errors.

## 0.2.0+codex.20260811104810 - 2026-08-11

- Added `.xmind` import support through `xmind_to_mindmap_data.py`.
- Supports modern XMind packages with `content.json`.
- Adds basic fallback parsing for legacy XMind packages with `content.xml`.
- Converts XMind topic titles, notes, and child topics into plugin JSON fields.
- Normalizes imported node types as `root`, `part`, `topic`, and `leaf`.
- Updates plugin manifest, README, USAGE, and skill guidance for XMind import/export workflows.

## 0.1.0+codex.20260811021844 - 2026-08-11

- Initial personal plugin release.
- Added text or Markdown to mind map JSON conversion.
- Added JSON and text to XMind-compatible `.xmind` export.
- Documented repair guidance for editable HTML mind maps.
- Captured interaction fixes for two-line editing, collapse hit areas, edit-safe layout, wrapping, and recursive child node operations.
