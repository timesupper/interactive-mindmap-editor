# Interactive Mindmap Editor

Codex plugin for creating, repairing, importing, and exporting editable standalone HTML and XMind mind maps.

## What it does

- Convert text, outlines, articles, and notes into mind map data.
- Export mind map JSON or text outlines to XMind-compatible `.xmind` files.
- Import modern `.xmind` files back into editable mind map JSON.
- Repair editable HTML mind map interactions.
- Generate HTML mind maps with fullscreen presentation controls and a top-hover `X` exit button.
- Use incremental toolbar expand/collapse: click once for one level, long-press for all levels.
- Support two-line node editing, fold/unfold hit areas, overlap-safe layout, wrapping, and recursive node add/edit/delete behavior.

## XMind export

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

## Install in another Codex environment

1. Clone this repository into the user's plugin folder:

   ```powershell
   New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
   git clone https://github.com/timesupper/interactive-mindmap-editor.git "$HOME\plugins\interactive-mindmap-editor"
   ```

2. Create or update the personal marketplace file as UTF-8 without BOM:

   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.agents\plugins" | Out-Null
   $marketplacePath = "$HOME\.agents\plugins\marketplace.json"
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
   ```

3. Register the marketplace root and install the plugin:

   ```powershell
   codex plugin marketplace add "$HOME"
   codex plugin add interactive-mindmap-editor@personal
   ```

If Codex reports `plugin was not found in marketplace personal`, check that the marketplace file has no UTF-8 BOM and that `codex plugin marketplace list` includes `personal`.
