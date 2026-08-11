#!/usr/bin/env python3
"""Convert structured text or Markdown directly to a .xmind file."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


text_module = load_module("text_to_mindmap_data", SCRIPT_DIR / "text_to_mindmap_data.py")
xmind_module = load_module("mindmap_data_to_xmind", SCRIPT_DIR / "mindmap_data_to_xmind.py")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert text or Markdown to .xmind.")
    parser.add_argument("input", help="Input text or Markdown file")
    parser.add_argument("-o", "--output", required=True, help="Output .xmind file")
    parser.add_argument("--root-title", default="思维导图", help="Root node title")
    parser.add_argument("--root-sub", default="由文本生成", help="Root node subtitle")
    parser.add_argument("--sheet-title", help="Optional XMind sheet title")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    data = text_module.convert_text(source, args.root_title, args.root_sub)
    xmind_module.write_xmind(data, Path(args.output), args.sheet_title or data.get("title"))


if __name__ == "__main__":
    main()
