"""Tests for the markdown parser module."""

from notion_cli.core.markdown import parse_markdown


class TestParseMarkdownHeadings:
    """Tests for heading parsing."""

    def test_parse_heading_2(self):
        """
        Condition: Markdown with ## heading.
        Expected: Returns Heading2 block.
        """
        blocks = parse_markdown("## Test Heading")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "Heading2"

    def test_parse_heading_3(self):
        """
        Condition: Markdown with ### heading.
        Expected: Returns Heading3 block.
        """
        blocks = parse_markdown("### Test Heading")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "Heading3"

    def test_multiple_headings(self):
        """
        Condition: Multiple headings in markdown.
        Expected: Returns multiple heading blocks.
        """
        blocks = parse_markdown("## H2\n### H3")

        assert len(blocks) == 2
        assert type(blocks[0]).__name__ == "Heading2"
        assert type(blocks[1]).__name__ == "Heading3"


class TestParseMarkdownLists:
    """Tests for list parsing."""

    def test_parse_bulleted_list(self):
        """
        Condition: Markdown with - item.
        Expected: Returns BulletedItem block.
        """
        blocks = parse_markdown("- Item 1")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "BulletedItem"

    def test_parse_multiple_bullets(self):
        """
        Condition: Multiple bullet items.
        Expected: Returns multiple bulleted list blocks.
        """
        blocks = parse_markdown("- Item 1\n- Item 2")

        assert len(blocks) == 2
        assert all(type(b).__name__ == "BulletedItem" for b in blocks)

    def test_parse_todo_unchecked(self):
        """
        Condition: Markdown with - [ ] task.
        Expected: Returns ToDoItem block with checked=False.
        """
        blocks = parse_markdown("- [ ] Todo item")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "ToDoItem"
        assert blocks[0].checked is False

    def test_parse_todo_checked(self):
        """
        Condition: Markdown with - [x] task.
        Expected: Returns ToDoItem block with checked=True.
        """
        blocks = parse_markdown("- [x] Done item")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "ToDoItem"
        assert blocks[0].checked is True


class TestParseMarkdownCodeBlocks:
    """Tests for code block parsing."""

    def test_parse_code_block(self):
        """
        Condition: Markdown with ``` code block.
        Expected: Returns Code block.
        """
        blocks = parse_markdown("```\ncode\n```")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "Code"

    def test_parse_code_block_with_language(self):
        """
        Condition: Markdown with ```python code block.
        Expected: Returns Code block with language.
        """
        blocks = parse_markdown("```python\nprint('hello')\n```")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "Code"

    def test_code_block_multiline(self):
        """
        Condition: Code block with multiple lines.
        Expected: Returns Code block with all lines.
        """
        md = "```python\nline1\nline2\nline3\n```"
        blocks = parse_markdown(md)

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "Code"


class TestParseMarkdownParagraphs:
    """Tests for paragraph parsing."""

    def test_parse_simple_text(self):
        """
        Condition: Plain text line.
        Expected: Returns Paragraph block.
        """
        blocks = parse_markdown("Simple text")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "Paragraph"

    def test_empty_lines_ignored(self):
        """
        Condition: Empty lines in markdown.
        Expected: Empty lines are ignored.
        """
        blocks = parse_markdown("Line 1\n\nLine 2")

        assert len(blocks) == 2
        assert type(blocks[0]).__name__ == "Paragraph"
        assert type(blocks[1]).__name__ == "Paragraph"


class TestParseMarkdownMixedContent:
    """Tests for mixed content parsing."""

    def test_parse_mixed_content(self):
        """
        Condition: Headings, lists, and paragraphs together.
        Expected: Returns blocks in correct order with correct types.
        """
        md = """## Heading

This is a paragraph.

- Bullet item
- [ ] Todo item

```python
code
```"""
        blocks = parse_markdown(md)

        assert len(blocks) == 5
        assert type(blocks[0]).__name__ == "Heading2"
        assert type(blocks[1]).__name__ == "Paragraph"
        assert type(blocks[2]).__name__ == "BulletedItem"
        assert type(blocks[3]).__name__ == "ToDoItem"
        assert type(blocks[4]).__name__ == "Code"

    def test_empty_input(self):
        """
        Condition: Empty string input.
        Expected: Returns empty list.
        """
        blocks = parse_markdown("")

        assert len(blocks) == 0

    def test_whitespace_only_input(self):
        """
        Condition: String with only whitespace.
        Expected: Returns empty list.
        """
        blocks = parse_markdown("   \n\n  ")

        assert len(blocks) == 0

    def test_heading_1(self):
        """
        Condition: Markdown with # heading.
        Expected: Returns Heading1 block.
        """
        blocks = parse_markdown("# Test Heading")

        assert len(blocks) == 1
        assert type(blocks[0]).__name__ == "Heading1"
