#!/usr/bin/env python3
"""Convert canonical mind map JSON into Markmap-compatible Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def clean(value: Any) -> str:
    return str(value or "").strip()


def label(node: dict[str, Any]) -> str:
    title = clean(node.get("title")) or "未命名节点"
    sub = clean(node.get("sub"))
    note = clean(node.get("note"))
    if sub:
        title = f"{title}：{sub}"
    if note:
        title = f"{title}（批注：{note}）"
    return title.replace("\n", " ")


def emit(children: list[dict[str, Any]], depth: int = 0) -> list[str]:
    lines: list[str] = []
    indent = "  " * depth
    for child in children:
        lines.append(f"{indent}- {label(child)}")
        nested = child.get("children") or []
        if isinstance(nested, list):
            lines.extend(emit(nested, depth + 1))
    return lines


def convert_data(data: dict[str, Any]) -> str:
    root = clean(data.get("title")) or "思维导图"
    root_sub = clean(data.get("sub"))
    lines = [f"# {root}"]
    if root_sub:
        lines.extend(["", root_sub])
    children = data.get("children") or []
    if isinstance(children, list) and children:
        lines.extend(["", *emit(children)])
    free_nodes = data.get("freeNodes") or []
    if isinstance(free_nodes, list) and free_nodes:
        lines.extend(["", "## 自由标题", *emit(free_nodes)])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert mind map JSON into Markmap-compatible Markdown."
    )
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
