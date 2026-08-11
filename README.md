# Interactive Mindmap Editor

Codex plugin for creating, repairing, and extending editable standalone HTML mind maps.

## What it does

- Convert text, outlines, articles, and notes into mind map data.
- Export mind map JSON or text outlines to XMind-compatible `.xmind` files.
- Repair editable HTML mind map interactions.
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

## Install in another Codex environment

1. Clone or copy this repository into a local plugin folder, for example:

   `~/plugins/interactive-mindmap-editor`

2. Add it to a local marketplace entry whose source path points to this plugin folder.

3. Install it from that marketplace:

   `codex plugin add interactive-mindmap-editor@personal`

For a personal marketplace, Codex normally reads `~/.agents/plugins/marketplace.json`.
