#!/usr/bin/env python3
"""Export interactive mind map JSON data to a modern .xmind file.

The output is a ZIP-based .xmind package containing content.json,
metadata.json, and manifest.json at the archive root.
"""

from __future__ import annotations

import argparse
import json
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_ms() -> int:
    return int(datetime.now(tz=timezone.utc).timestamp() * 1000)


def topic_id(prefix: str = "topic") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def node_text(node: dict[str, Any], key: str, default: str = "") -> str:
    value = node.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def note_content(node: dict[str, Any]) -> str:
    parts: list[str] = []
    sub = node_text(node, "sub")
    note = node_text(node, "note")
    if sub:
        parts.append(sub)
    if note and note != sub:
        parts.append(note)
    return "\n\n".join(parts)


def to_xmind_topic(node: dict[str, Any], *, is_root: bool = False) -> dict[str, Any]:
    title = node_text(node, "title", "思维导图" if is_root else "新节点")
    topic: dict[str, Any] = {
        "id": node_text(node, "id") or topic_id(),
        "title": title,
    }

    note = note_content(node)
    if note:
        topic["notes"] = {"plain": {"content": note}}

    children = node.get("children") or []
    if children:
        topic["children"] = {
            "attached": [to_xmind_topic(child) for child in children]
        }

    return topic


def build_content(data: dict[str, Any], sheet_title: str | None = None) -> list[dict[str, Any]]:
    title = sheet_title or node_text(data, "title", "思维导图")
    return [
        {
            "id": f"sheet-{uuid.uuid4().hex[:12]}",
            "title": title,
            "rootTopic": to_xmind_topic(data, is_root=True),
            "topicPositioning": "fixed",
            "extensions": [],
            "theme": {
                "id": "default",
                "title": "Default",
            },
        }
    ]


def build_metadata() -> dict[str, Any]:
    return {
        "creator": {
            "name": "interactive-mindmap-editor",
            "version": "0.1.0",
        },
        "created": now_ms(),
        "modified": now_ms(),
    }


def build_manifest() -> dict[str, Any]:
    return {
        "file-entries": {
            "content.json": {"media-type": "application/json"},
            "metadata.json": {"media-type": "application/json"},
            "manifest.json": {"media-type": "application/json"},
        }
    }


def write_xmind(data: dict[str, Any], output: Path, sheet_title: str | None = None) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    content = build_content(data, sheet_title)
    metadata = build_metadata()
    manifest = build_manifest()

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("content.json", json.dumps(content, ensure_ascii=False, indent=2))
        archive.writestr("metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2))
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Export mind map JSON data to .xmind.")
    parser.add_argument("input", help="Input mind map JSON file")
    parser.add_argument("-o", "--output", required=True, help="Output .xmind file")
    parser.add_argument("--sheet-title", help="Optional XMind sheet title")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    write_xmind(data, Path(args.output), args.sheet_title)


if __name__ == "__main__":
    main()
