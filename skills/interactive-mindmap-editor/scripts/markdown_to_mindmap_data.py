#!/usr/bin/env python3
"""Convert Markdown outlines into interactive mind map JSON data.

This is a thin wrapper that reuses the same structured-text parser as
``text_to_mindmap_data.py``, so Markdown headings, bullets, numbering, and
indentation all map to the same ``root -> part -> topic -> leaf`` node shape.
"""

from __future__ import annotations

import json
from pathlib import Path

from text_to_mindmap_data import convert_text


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Convert a Markdown outline into mind map JSON.")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("-o", "--output", help="Output JSON file. Defaults to stdout.")
    parser.add_argument("--root-title", default="主题", help="Root node title. Default: 主题")
    parser.add_argument("--root-sub", default="由 Markdown 生成", help="Root node subtitle")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    tree = convert_text(source, args.root_title, args.root_sub)
    payload = json.dumps(tree, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
