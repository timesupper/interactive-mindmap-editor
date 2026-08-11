#!/usr/bin/env python3
"""Convert interactive mind map JSON data into a Markdown outline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def text(value: Any) -> str:
    return str(value or "").strip()


def node_label(node: dict[str, Any]) -> str:
    title = text(node.get("title")) or "未命名节点"
    sub = text(node.get("sub"))
    if sub:
        return f"{title}：{sub}"
    return title


def emit_children(children: list[dict[str, Any]], depth: int = 0) -> list[str]:
    lines: list[str] = []
    indent = "  " * depth
    for child in children:
        lines.append(f"{indent}- {node_label(child)}")
        note = text(child.get("note"))
        if note:
            note_indent = "  " * (depth + 1)
            for line in note.splitlines():
                if line.strip():
                    lines.append(f"{note_indent}> {line.strip()}")
        nested = child.get("children") or []
        if isinstance(nested, list) and nested:
            lines.extend(emit_children(nested, depth + 1))
    return lines


def convert_data(data: dict[str, Any]) -> str:
    root_title = text(data.get("title")) or "思维导图"
    root_sub = text(data.get("sub"))
    lines = [f"# {root_title}"]
    if root_sub:
        lines.extend(["", root_sub])
    children = data.get("children") or []
    if isinstance(children, list) and children:
        lines.append("")
        lines.extend(emit_children(children))
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert mind map JSON data to a Markdown outline.")
    parser.add_argument("input", help="Input mind map JSON file")
    parser.add_argument("-o", "--output", help="Output Markdown file. Defaults to stdout.")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must be an object.")
    payload = convert_data(data)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
