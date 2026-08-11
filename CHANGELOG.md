# Changelog

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
