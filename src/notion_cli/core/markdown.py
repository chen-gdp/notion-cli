"""Markdown parser for converting markdown to Notion blocks.

Parses common markdown elements and converts them to Notion block objects
for use with the page append command.
"""

import re

from ultimate_notion.blocks import (
    BulletedItem,
    Code,
    Heading1,
    Heading2,
    Heading3,
    Paragraph,
    ToDoItem,
)


def parse_markdown(text: str) -> list:
    """Parse markdown text into Notion block objects.

    Supports:
    - Headings: # Heading (level 1), ## Heading (level 2), ### Heading (level 3)
    - Bullet lists: - Item
    - Todo lists: - [ ] Unchecked, - [x] Checked
    - Code blocks: ```language\ncode```
    - Paragraphs: Plain text

    Args:
        text: Markdown text to parse.

    Returns:
        List of Notion block objects.
    """
    blocks = []
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Code blocks
        if line.startswith("```"):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append(Code("\n".join(code_lines), language=lang if lang else "plain text"))
            i += 1
            continue

        # Heading 1
        if line.startswith("# ") and not line.startswith("## "):
            blocks.append(Heading1(line[2:].strip()))
            i += 1
            continue

        # Heading 2
        if line.startswith("## ") and not line.startswith("### "):
            blocks.append(Heading2(line[3:].strip()))
            i += 1
            continue

        # Heading 3
        if line.startswith("### "):
            blocks.append(Heading3(line[4:].strip()))
            i += 1
            continue

        # Todo items
        todo_match = re.match(r"- \[([ x])\] (.+)", line)
        if todo_match:
            checked = todo_match.group(1) == "x"
            blocks.append(ToDoItem(todo_match.group(2).strip(), checked=checked))
            i += 1
            continue

        # Bulleted lists
        if line.startswith("- "):
            blocks.append(BulletedItem(line[2:].strip()))
            i += 1
            continue

        # Paragraphs (default)
        blocks.append(Paragraph(line))
        i += 1

    return blocks
