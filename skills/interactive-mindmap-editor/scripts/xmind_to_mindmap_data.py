#!/usr/bin/env python3
"""Import .xmind files into interactive mind map JSON data.

The importer prefers modern ZIP-based XMind workbooks with content.json. It also
supports the common legacy content.xml shape used by XMind 8-style packages.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

COLORS = ["#c24a34", "#2f6db3", "#3d7a4d", "#7a5ba6", "#b8852f"]


def clean(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip())


def strip_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def note_from_topic(topic: dict[str, Any]) -> str:
    notes = topic.get("notes") or {}
    if isinstance(notes, str):
        return clean(notes)
    if not isinstance(notes, dict):
        return ""

    plain = notes.get("plain") or {}
    if isinstance(plain, str):
        return clean(plain)
    if isinstance(plain, dict) and plain.get("content"):
        return str(plain["content"]).strip()

    real_html = notes.get("realHTML") or notes.get("html") or {}
    if isinstance(real_html, str):
        return strip_html(real_html)
    if isinstance(real_html, dict) and real_html.get("content"):
        return strip_html(str(real_html["content"]))
    return ""


def attached_children(topic: dict[str, Any]) -> list[dict[str, Any]]:
    children = topic.get("children") or {}
    if isinstance(children, list):
        return [child for child in children if isinstance(child, dict)]
    if not isinstance(children, dict):
        return []

    result: list[dict[str, Any]] = []
    for key in ("attached", "detached", "floating"):
        values = children.get(key) or []
        if isinstance(values, list):
            result.extend(child for child in values if isinstance(child, dict))
    return result


def convert_topic(topic: dict[str, Any], *, depth: int = 0, index: int = 0, color: str | None = None) -> dict[str, Any]:
    branch_color = color or (COLORS[index % len(COLORS)] if depth == 1 else "#2b2620")
    node: dict[str, Any] = {
        "id": "root" if depth == 0 else clean(topic.get("id")) or f"n{index + 1}",
        "title": clean(topic.get("title")) or ("思维导图" if depth == 0 else "新节点"),
        "type": "root" if depth == 0 else "leaf",
        "color": "#2b2620" if depth == 0 else branch_color,
    }

    note = note_from_topic(topic)
    if note:
        node["sub"] = note

    child_nodes = []
    for child_index, child in enumerate(attached_children(topic)):
        child_color = COLORS[child_index % len(COLORS)] if depth == 0 else branch_color
        child_nodes.append(convert_topic(child, depth=depth + 1, index=child_index, color=child_color))
    if child_nodes:
        node["children"] = child_nodes
    return node


def normalize_types(node: dict[str, Any], depth: int = 0) -> None:
    children = node.get("children") or []
    if depth == 0:
        node["type"] = "root"
        node.setdefault("children", children)
    elif depth == 1:
        node["type"] = "part"
    elif children:
        node["type"] = "topic"
    else:
        node["type"] = "leaf"

    if children:
        node["children"] = children
        for child in children:
            child.setdefault("color", node.get("color", COLORS[0]))
            normalize_types(child, depth + 1)
    elif depth > 0:
        node.pop("children", None)


def load_modern_content(archive: zipfile.ZipFile) -> dict[str, Any]:
    with archive.open("content.json") as handle:
        content = json.loads(handle.read().decode("utf-8-sig"))
    sheet = content[0] if isinstance(content, list) and content else content
    if not isinstance(sheet, dict) or not isinstance(sheet.get("rootTopic"), dict):
        raise ValueError("content.json does not contain a rootTopic")
    return convert_topic(sheet["rootTopic"], depth=0)


def xml_text(element: ElementTree.Element, tag: str) -> str:
    found = element.find(f"{{*}}{tag}")
    return "".join(found.itertext()).strip() if found is not None else ""


def xml_notes(element: ElementTree.Element) -> str:
    notes = element.find("{*}notes")
    if notes is None:
        return ""
    plain = notes.find("{*}plain")
    if plain is not None:
        return "".join(plain.itertext()).strip()
    html_note = notes.find("{*}html")
    if html_note is not None:
        return strip_html("".join(html_note.itertext()))
    return ""


def xml_child_topics(element: ElementTree.Element) -> list[ElementTree.Element]:
    result: list[ElementTree.Element] = []
    children = element.find("{*}children")
    if children is None:
        return result
    for topics in children.findall("{*}topics"):
        result.extend(topics.findall("{*}topic"))
    return result


def convert_xml_topic(element: ElementTree.Element, *, depth: int = 0, index: int = 0, color: str | None = None) -> dict[str, Any]:
    branch_color = color or (COLORS[index % len(COLORS)] if depth == 1 else "#2b2620")
    node: dict[str, Any] = {
        "id": "root" if depth == 0 else clean(element.get("id")) or f"n{index + 1}",
        "title": clean(xml_text(element, "title")) or ("思维导图" if depth == 0 else "新节点"),
        "type": "root" if depth == 0 else "leaf",
        "color": "#2b2620" if depth == 0 else branch_color,
    }
    note = xml_notes(element)
    if note:
        node["sub"] = note

    children = []
    for child_index, child in enumerate(xml_child_topics(element)):
        child_color = COLORS[child_index % len(COLORS)] if depth == 0 else branch_color
        children.append(convert_xml_topic(child, depth=depth + 1, index=child_index, color=child_color))
    if children:
        node["children"] = children
    return node


def load_legacy_content(archive: zipfile.ZipFile) -> dict[str, Any]:
    with archive.open("content.xml") as handle:
        root = ElementTree.fromstring(handle.read())
    sheet = root.find(".//{*}sheet")
    topic = sheet.find("{*}topic") if sheet is not None else root.find(".//{*}topic")
    if topic is None:
        raise ValueError("content.xml does not contain a topic")
    return convert_xml_topic(topic, depth=0)


def read_xmind(input_path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(input_path, "r") as archive:
        names = set(archive.namelist())
        if "content.json" in names:
            data = load_modern_content(archive)
        elif "content.xml" in names:
            data = load_legacy_content(archive)
        else:
            raise ValueError("Unsupported .xmind package: missing content.json or content.xml")
    normalize_types(data)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Import .xmind into interactive mind map JSON data.")
    parser.add_argument("input", help="Input .xmind file")
    parser.add_argument("-o", "--output", help="Output JSON file. Defaults to stdout.")
    args = parser.parse_args()

    data = read_xmind(Path(args.input))
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
