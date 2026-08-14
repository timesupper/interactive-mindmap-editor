from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPTS = ROOT / "skills" / "interactive-mindmap-editor" / "scripts"
FIXTURE = Path(__file__).parent / "fixtures" / "sample-mindmap.json"


def run(script: str, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def test_markmap_json_round_trip(tmp_path: Path) -> None:
    markdown = tmp_path / "map.md"
    markdown.write_text("# 投资体系\n\n- 基本面分析\n  - 财务指标\n- 技术分析\n", encoding="utf-8")
    json_path = tmp_path / "map.json"
    subprocess.run(
        [sys.executable, str(SCRIPTS / "markmap_markdown_to_mindmap_data.py"), str(markdown), "-o", str(json_path)],
        check=True,
    )
    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["title"] == "投资体系"
    assert len(data["children"]) == 2
    output = run("mindmap_data_to_markmap_markdown.py", str(FIXTURE))
    assert "# 投资体系" in output
    assert "- 基本面分析" in output
    assert "  - 财务指标：收入、利润和现金流" in output


def test_render_html(tmp_path: Path) -> None:
    output = tmp_path / "map.html"
    subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "render_markmap_html.py"),
            str(FIXTURE),
            "--template",
            str(ROOT / "templates" / "interactive-mindmap.html"),
            "--runtime",
            str(ROOT / "runtime" / "markmap-preview.js"),
            "--assets",
            str(ROOT / "runtime" / "markmap-assets.js"),
            "--styles",
            str(ROOT / "runtime" / "markmap-preview.css"),
            "-o",
            str(output),
        ],
        check=True,
    )
    html = output.read_text(encoding="utf-8")
    assert "InteractiveMindmapMarkmap" in html
    assert "Markmap.create" in html
    assert "投资体系" in html
    assert "{{STYLES}}" not in html
    assert "imm-markmap-dialog" in html
    assert "{{DATA}}" not in html
