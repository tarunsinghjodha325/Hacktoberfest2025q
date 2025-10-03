#!/usr/bin/env python3
"""
markdown_toc.py
Generate a Markdown Table of Contents from headings in a .md file (or STDIN).

Usage:
  python3 markdown_toc.py README.md
  cat README.md | python3 markdown_toc.py
"""

import re
import sys
from typing import Iterable

HEADING_RE = re.compile(r'^(?P<prefix>#{1,6})\s+(?P<title>.+?)\s*#*\s*$')

def slugify_github(text: str) -> str:
    """Rough GitHub-style slug: lowercase, remove punctuation, spaces -> hyphens."""
    text = text.strip().lower()
    # remove punctuation except hyphen and space
    text = re.sub(r'[^\w\- ]+', '', text)
    # replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    # collapse multiple hyphens
    text = re.sub(r'-{2,}', '-', text)
    return text

def iter_headings(lines: Iterable[str]):
    for line in lines:
        m = HEADING_RE.match(line)
        if not m:
            continue
        level = len(m.group('prefix'))
        title = m.group('title').strip()
        yield level, title, slugify_github(title)

def build_toc(lines: Iterable[str]) -> str:
    toc_lines = []
    for level, title, slug in iter_headings(lines):
        indent = '  ' * (level - 1)  # 2 spaces per level
        toc_lines.append(f"{indent}- [{title}](#{slug})")
    return "\n".join(toc_lines)

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.readlines()
    else:
        content = sys.stdin.readlines()

    toc = build_toc(content)
    print(toc if toc else "# (No headings found)")

if __name__ == "__main__":
    main()
