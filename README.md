# Interactive Mindmap Editor

Dual-compatible toolkit for Codex and Claude that creates, repairs, imports, and exports editable standalone HTML, Markdown, and XMind mind maps.

## What it does

- Works as a Codex personal plugin.
- Works as a Claude personal or project skill.
- Works as a plain script toolkit when called directly from Python.
- Convert text, outlines, articles, and notes into mind map data.
- Convert Markdown outlines to mind map JSON, and export mind map JSON back to Markdown outlines.
- Export mind map JSON or text outlines to XMind-compatible `.xmind` files.
- Import modern `.xmind` files back into editable mind map JSON.
- Repair editable HTML mind map interactions.
- Generate HTML mind maps with fullscreen presentation controls and a top-hover `X` exit button.
- Group secondary HTML toolbar actions behind a compact round menu button when many controls are present.
- Use incremental toolbar expand/collapse: click once for one level, long-press for all levels.
- Support two-line node editing, fold/unfold hit areas, overlap-safe layout, wrapping, and recursive node add/edit/delete behavior.

## Compatibility layout

```text
interactive-mindmap-editor/
├── .codex-plugin/
│   └── plugin.json
├── SKILL.md
├── CLAUDE.md
├── install-codex.ps1
├── README.md
├── USAGE.md
├── CHANGELOG.md
└── skills/
    └── interactive-mindmap-editor/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── scripts/
            ├── markdown_to_mindmap_data.py
            ├── mindmap_data_to_markdown.py
            ├── mindmap_data_to_xmind.py
            ├── text_to_mindmap_data.py
            ├── text_to_xmind.py
            └── xmind_to_mindmap_data.py
```

Entry points:

- Codex reads `.codex-plugin/plugin.json`, then `skills/interactive-mindmap-editor/SKILL.md`.
- Claude Skill reads root `SKILL.md` when this repository is installed as a skill folder.
- Claude Code also reads `CLAUDE.md` when working inside this repository.
- All entry points share the same scripts under `skills/interactive-mindmap-editor/scripts/`.

## Markdown import/export

Convert Markdown or structured text to plugin JSON:

```powershell
python .\skills\interactive-mindmap-editor\scripts\markdown_to_mindmap_data.py .\input.md -o .\mindmap-data.json --root-title "主题"
```

Convert plugin JSON back to a Markdown outline:

```powershell
python .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_markdown.py .\mindmap-data.json -o .\outline.md
```

Generated standalone HTML mind maps should include `导入 Markdown` and `导出 Markdown` controls when import/export controls are present.

## Global numbering and Markmap compatibility

Standalone HTML editors should keep these global actions in the right-click context menu: `全部自动编号`, `重编全部编号`, and `取消全部编号`.

The enabled state should persist after reopening the HTML. While numbering is enabled, add/delete/reorder/reparent/free-node and JSON/Markdown import operations should renumber the complete tree. Markmap preview should display the same numbers while using standard `-` list markers internally so all child levels parse consistently in Chrome and Edge.

For embedded Markmap rendering, validate preview container dimensions before creating the SVG, guard `fit()` against invalid dimensions, and dispose pending transitions, observers, timers, and render tasks when the preview closes.

## HTML file export

Generated standalone HTML should route JSON, Markdown, and XMind exports through one system Save As flow:

- Open `showSaveFilePicker` directly from the export button click so the browser preserves the user gesture.
- Use a stable picker `id` for all export formats and persist the last successfully saved file handle in IndexedDB.
- Pass the restored file handle as `startIn` so later exports, including exports after reopening the HTML, start in the previous save folder.
- Save immediately after the user confirms the Save As window; do not show a second confirmation dialog.
- Treat closing or cancelling the Save As window as cancellation and do not start a fallback download.
- Show a non-blocking success message with the saved filename and hide it automatically after three seconds.
- Prefer `showSaveFilePicker` over `showDirectoryPicker` for local `file://` pages because directory pickers can reject protected system folders such as Downloads.

## HTML toolbar menu

When a generated standalone HTML mind map has many controls, group secondary actions behind a compact round menu button placed above the visible zoom controls. Keep zoom in, zoom out, and reset view visible as round buttons.

Recommended menu items:

- `展开`
- `折叠`
- `导入 Markdown`
- `导出 Markdown`
- `XMind`
- `全屏展示`
- `适配`

## XMind import/export

Convert plugin JSON to `.xmind`:

```powershell
python .\skills\interactive-mindmap-editor\scripts\mindmap_data_to_xmind.py .\mindmap-data.json -o .\output.xmind
```

Convert Markdown or structured text directly to `.xmind`:

```powershell
python .\skills\interactive-mindmap-editor\scripts\text_to_xmind.py .\input.md -o .\output.xmind --root-title "主题"
```

Import `.xmind` back to plugin JSON:

```powershell
python .\skills\interactive-mindmap-editor\scripts\xmind_to_mindmap_data.py .\input.xmind -o .\mindmap-data.json
```

## Version history

See [CHANGELOG.md](CHANGELOG.md) for version iteration notes.

## Install in Codex

Recommended PowerShell install:

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"
cd "$HOME\plugins\interactive-mindmap-editor"
.\install-codex.ps1
```

Manual Codex install:

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"

$marketplacePath = "$HOME\.agents\plugins\marketplace.json"
New-Item -ItemType Directory -Force "$HOME\.agents\plugins" | Out-Null

$marketplace = [ordered]@{
  name = "personal"
  interface = [ordered]@{ displayName = "Personal" }
  plugins = @(
    [ordered]@{
      name = "interactive-mindmap-editor"
      source = [ordered]@{
        source = "local"
        path = "./plugins/interactive-mindmap-editor"
      }
      policy = [ordered]@{
        installation = "AVAILABLE"
        authentication = "ON_INSTALL"
      }
      category = "Productivity"
    }
  )
}

$json = $marketplace | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($marketplacePath, $json, $utf8NoBom)

codex plugin marketplace add "$HOME"
codex plugin add interactive-mindmap-editor@personal
```

If Codex reports `plugin was not found in marketplace personal`, check that `marketplace.json` has no UTF-8 BOM and that `codex plugin marketplace list` includes `personal`.

Codex project portability:

- Install once per machine for normal use; every Codex task can then use the plugin.
- For another device, run the install commands on that device.
- For a project-pinned copy, clone this repository into the project and ask Codex to use scripts from that local path.

## Install in Claude

Personal Claude skill install on Windows:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\.claude\skills\interactive-mindmap-editor"
```

Project-local Claude skill install:

```powershell
cd "E:\path\to\your\project"
New-Item -ItemType Directory -Force ".\.claude\skills" | Out-Null
git clone https://github.com/timesupper/interactive-mindmap-editor.git ".\.claude\skills\interactive-mindmap-editor"
```

Claude project portability:

- Use personal skill install when many projects should share the same latest behavior.
- Use project-local install when a project must carry a pinned copy of the skill.
- Move mind map artifacts (`.html`, `.json`, `.md`, `.xmind`) with the project.
- Keep root `SKILL.md` in the skill folder; Claude uses it as the skill entry.

## Updating

Codex update:

```powershell
cd "$HOME\plugins\interactive-mindmap-editor"
git pull
.\install-codex.ps1
```

Claude personal skill update:

```powershell
cd "$HOME\.claude\skills\interactive-mindmap-editor"
git pull
```

Claude project skill update:

```powershell
cd "E:\path\to\your\project\.claude\skills\interactive-mindmap-editor"
git pull
```
