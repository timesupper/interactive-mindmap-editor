#!/usr/bin/env python3
"""Convert structured text or Markdown-like notes into mind map JSON data.

This utility is intentionally conservative. It preserves the input hierarchy when
headings, bullets, numbering, or indentation are present. For unstructured prose,
it creates paragraph-level children so Codex can refine the result afterward.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

COLORS = ["#c24a34", "#2f6db3", "#3d7a4d", "#7a5ba6", "#b8852f"]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def split_title_sub(text: str, title_limit: int = 30) -> tuple[str, str]:
    text = clean(text)
    if not text:
        return "新节点", ""
    for sep in ["：", ":", " - ", " -- ", "——", "："]:
        if sep in text:
            left, right = text.split(sep, 1)
            left, right = clean(left), clean(right)
            if left and right:
                return left[:title_limit], right
    sentence = re.split(r"(?<=[。！？!?；;])", text, maxsplit=1)
    if len(sentence) == 2 and clean(sentence[0]):
        return clean(sentence[0])[:title_limit], clean(sentence[1])
    if len(text) > title_limit:
        return text[:title_limit], text[title_limit:].strip()
    return text, ""


def classify_line(raw: str) -> tuple[int, str] | None:
    if not raw.strip():
        return None
    line = raw.rstrip()
    stripped = line.strip()

    heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
    if heading:
        return len(heading.group(1)), heading.group(2)

    numbered_heading = re.match(r"^(第?[一二三四五六七八九十百千万0-9]+[章节篇部分讲课]|[一二三四五六七八九十]+[、.．]|\d+[.)、．])\s*(.+)$", stripped)
    if numbered_heading:
        return 2, numbered_heading.group(2) or stripped

    bullet = re.match(r"^(\s*)([-*+•]|\d+[.)、．]|[一二三四五六七八九十]+[、.．])\s+(.+)$", line)
    if bullet:
        indent = len(bullet.group(1).replace("\t", "    "))
        level = 3 + indent // 2
        return max(2, min(level, 8)), bullet.group(3)

    return 3, stripped


def make_node(node_id: str, text: str, color: str) -> dict[str, Any]:
    title, sub = split_title_sub(text)
    node: dict[str, Any] = {"id": node_id, "title": title, "type": "leaf", "color": color}
    if sub:
        node["sub"] = sub
    return node


def normalize_types(node: dict[str, Any], depth: int = 0) -> None:
    children = node.get("children") or []
    if depth == 0:
        node["type"] = "root"
    elif depth == 1:
        node["type"] = "part"
    elif children:
        node["type"] = "topic"
    else:
        node["type"] = "leaf"
    if children:
        node["children"] = children
        for child in children:
            normalize_types(child, depth + 1)
    else:
        node.pop("children", None)


def convert_text(text: str, root_title: str, root_sub: str) -> dict[str, Any]:
    root: dict[str, Any] = {
        "id": "root",
        "title": root_title,
        "sub": root_sub,
        "type": "root",
        "color": "#2b2620",
        "children": [],
    }
    stack: list[tuple[int, dict[str, Any]]] = [(0, root)]
    counter = 0
    saw_structured = False

    paragraphs: list[str] = []
    paragraph_buffer: list[str] = []

    for raw in text.splitlines():
        item = classify_line(raw)
        if item is None:
            if paragraph_buffer:
                paragraphs.append(clean(" ".join(paragraph_buffer)))
                paragraph_buffer = []
            continue
        level, content = item
        stripped = raw.strip()
        if level == 1:
            if root["title"] == "思维导图":
                root["title"] = clean(content)
            elif clean(content) != clean(root["title"]):
                counter += 1
                node = make_node(f"n{counter}", content, COLORS[len(root["children"]) % len(COLORS)])
                root["children"].append(node)
                stack = [(0, root), (1, node)]
            continue
        structured = bool(re.match(r"^(#{1,6})\s+", stripped) or re.match(r"^\s*([-*+•]|\d+[.)、．]|[一二三四五六七八九十]+[、.．])\s+", raw))
        if structured or saw_structured:
            saw_structured = saw_structured or structured
            if paragraph_buffer:
                paragraphs.append(clean(" ".join(paragraph_buffer)))
                paragraph_buffer = []
            counter += 1
            parent_level = level - 1
            while stack and stack[-1][0] >= level:
                stack.pop()
            parent = stack[-1][1] if stack else root
            color = COLORS[(len(root["children"]) if parent is root else COLORS.index(parent.get("color", COLORS[0])) if parent.get("color") in COLORS else 0) % len(COLORS)]
            if parent is not root:
                color = parent.get("color", color)
            node = make_node(f"n{counter}", content, color)
            parent.setdefault("children", []).append(node)
            stack.append((level, node))
        else:
            paragraph_buffer.append(content)

    if paragraph_buffer:
        paragraphs.append(clean(" ".join(paragraph_buffer)))

    if not saw_structured and paragraphs:
        for index, paragraph in enumerate(paragraphs, 1):
            color = COLORS[(index - 1) % len(COLORS)]
            node = make_node(f"n{index}", paragraph, color)
            root["children"].append(node)

    normalize_types(root)
    return root


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert text to interactive mind map JSON data.")
    parser.add_argument("input", help="Input text or Markdown file")
    parser.add_argument("-o", "--output", help="Output JSON file. Defaults to stdout.")
    parser.add_argument("--root-title", default="思维导图", help="Root node title")
    parser.add_argument("--root-sub", default="由文本生成", help="Root node subtitle")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    data = convert_text(source, args.root_title, args.root_sub)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()

