# Changelog

## 0.5.0+dual.20260811190000 - 2026-08-11

- Added root-level `SKILL.md` as the Claude Skill entry point while preserving the Codex skill under `skills/interactive-mindmap-editor/SKILL.md`.
- Expanded `CLAUDE.md` into a Claude Code project-memory guide for this repository.
- Added `install-codex.ps1` for one-command Codex personal plugin installation.
- Documented Codex and Claude installation paths separately.
- Documented project portability rules for Codex plugins, Claude personal skills, Claude project skills, and mind map artifacts.
- Preserved Markdown import/export scripts and compact toolbar menu guidance from the 0.4.x line.

## 0.4.1+codex.20260811180500 - 2026-08-11

- Documented compact toolbar menu behavior for generated standalone HTML mind maps.
- Recommended grouping secondary tools such as expand/collapse, Markdown import/export, XMind export, fullscreen, and fit view behind a round menu button.
- Kept zoom in, zoom out, and reset view as always-visible round controls.

## 0.4.0+codex.20260811172000 - 2026-08-11

- Added explicit Markdown import script `markdown_to_mindmap_data.py`.
- Added Markdown outline export script `mindmap_data_to_markdown.py`.
- Documented Markdown outline to mind map JSON and mind map JSON to Markdown workflows.
- Updated generated HTML guidance to include `导入 Markdown` and `导出 Markdown` controls.

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
