# Changelog

## 0.8.1+markmap-ui.20260812 - 2026-08-12

- Refined standalone Markmap preview UI with embedded offline rendering as the default path.
- Added preview-state persistence for restoring the last-opened Markmap page and its expand-level state when the HTML is reopened.
- Added level-based Markmap fold behavior: single click collapses one level, double click restores one level, and long press toggles between fully collapsed and fully expanded.
- Reworked Markmap preview actions into a single hover-open menu and merged fullscreen enter/exit into one toggle button.
- Fixed fullscreen interaction conflicts so Markmap preview close and fullscreen controls remain clickable while the page is in fullscreen mode.
## 0.8.0+markmap.20260812 - 2026-08-12

- Added `mindmap_data_to_markmap_markdown.py` for exporting canonical mind map JSON to Markmap-compatible Markdown.
- Added `markmap_markdown_to_mindmap_data.py` for importing Markmap-compatible Markdown into canonical mind map JSON.
- Added `docs/markmap-plan.md` to document the staged Markmap integration strategy.
- Updated Claude and Codex skill entry points to describe Markmap as a Markdown-based preview and interchange layer.
- Updated README, USAGE, and plugin metadata to document Markmap compatibility and command examples.
- Documented standalone HTML preview mode that prefers embedded offline Markmap rendering and falls back to a local tree preview only when embedded library initialization fails.

## 0.7.0+interaction.20260812 - 2026-08-12

- Added free-floating title behavior with persistent `freeNodes` coordinates.
- Added sibling-title reparenting on release, including release-position ordering.
- Added dashed detach previews and blue dashed target previews during drag.
- Stabilized the viewport after drag, edit, add, delete, collapse, resize, and fullscreen operations.
- Added anchor-based layout with aligned siblings and constant edge-to-edge spacing.
- Fixed connector redraw after drag reparenting and prevented moved titles from disappearing off-screen.

## 0.6.0+quad.20260811 - 2026-08-11

- 新增四环境兼容支持：Claude Desktop、Claude Code（CLI）、Codex Desktop、Codex CLI。
- 补全 `.codex-plugin/plugin.json`，使 Codex 桌面版与 CLI 都能以插件方式安装。
- 新增 `markdown_to_mindmap_data.py` 与 `mindmap_data_to_markdown.py`，支持 Markdown 提纲与思维导图 JSON 双向转换。
- Claude 侧 SKILL.md 脚本引用改用 `${CLAUDE_SKILL_DIR}`，跨个人/项目/插件安装位置均可靠。
- 新增 `CLAUDE.md`、`USAGE.md`，分别作为 Claude Code 项目记忆入口和四环境安装说明。
- README 更新为四环境安装说明。

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


