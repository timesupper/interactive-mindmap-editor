#!/usr/bin/env python3
"""Convert Markmap-compatible Markdown into the canonical mind map JSON shape."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from text_to_mindmap_data import convert_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert Markmap Markdown into interactive mind map JSON data."
    )
    parser.add_argument("input", help="Input Markmap Markdown file")
    parser.add_argument("-o", "--output", help="Output JSON file. Defaults to stdout.")
    parser.add_argument("--root-title", default="思维导图", help="Fallback root title")
    parser.add_argument("--root-sub", default="由 Markmap Markdown 生成", help="Root subtitle")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    tree = convert_text(source, args.root_title, args.root_sub)
    payload = json.dumps(tree, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
