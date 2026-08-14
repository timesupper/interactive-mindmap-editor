#!/usr/bin/env python3
"""Build a standalone offline Markmap preview HTML from mind map JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def replace_once(template: str, marker: str, value: str) -> str:
    if marker not in template:
        raise SystemExit(f"Template marker not found: {marker}")
    return template.replace(marker, value, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Mind map JSON file")
    parser.add_argument("-o", "--output", required=True, help="Output HTML file")
    parser.add_argument("--template", required=True, help="HTML template file")
    parser.add_argument("--runtime", required=True, help="Markmap runtime JavaScript")
    parser.add_argument("--assets", required=True, help="Markmap assets JavaScript")
    parser.add_argument("--styles", required=True, help="Markmap preview CSS")
    parser.add_argument("--title", default="Interactive Mindmap", help="HTML title")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must be an object.")
    html = Path(args.template).read_text(encoding="utf-8")
    html = replace_once(html, "{{TITLE}}", args.title.replace("&", "&amp;").replace("<", "&lt;"))
    html = replace_once(html, "{{DATA}}", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    html = replace_once(html, "{{ASSETS}}", Path(args.assets).read_text(encoding="utf-8"))
    html = replace_once(html, "{{RUNTIME}}", Path(args.runtime).read_text(encoding="utf-8"))
    html = replace_once(html, "{{STYLES}}", Path(args.styles).read_text(encoding="utf-8"))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
