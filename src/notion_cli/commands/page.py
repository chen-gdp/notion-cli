"""Page commands for notion-cli."""

import typer
from rich.console import Console

from notion_cli.core.markdown import parse_markdown
from notion_cli.core.output import output_error, output_json
from notion_cli.core.session import get_session

console = Console()
app = typer.Typer()


@app.command("create")
def page_create(
    parent: str = typer.Option(..., "--parent", help="Parent page/database ID"),
    title: str = typer.Option(..., "--title", help="Page title"),
    properties: str | None = typer.Option(None, "--properties", help="Properties for database entries"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Create a new page."""
    try:
        session = get_session()

        # Get parent (could be page or database)
        parent_obj = session.get_page(parent)
        if not parent_obj:
            parent_obj = session.get_db(parent)

        # Build properties
        props = {"title": title}
        if properties:
            for pair in properties.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    props[key] = value

        # Create page
        if hasattr(parent_obj, "create_page"):
            page = parent_obj.create_page(**props)
        else:
            page = parent_obj.create_child_page(title=title)

        result = {"id": str(page.id), "title": page.title, "url": page.url}

        if json:
            output_json(result)
        else:
            console.print(f"[green]✓ Created:[/green] {page.title}")
            console.print(f"  ID: {page.id}")

    except Exception as e:
        if json:
            output_error("PAGE_CREATE_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")


@app.command("append")
def page_append(
    page_id: str = typer.Argument(..., help="Page ID"),
    content: str = typer.Option(..., "--content", help="Content to append (markdown)"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Append blocks to a page."""
    try:
        session = get_session()
        page = session.get_page(page_id)

        # Parse markdown and append blocks
        blocks = parse_markdown(content)
        page.append(*blocks)

        result = {"page_id": str(page.id), "blocks_added": len(blocks)}

        if json:
            output_json(result)
        else:
            console.print(f"[green]✓ Added {len(blocks)} blocks[/green]")

    except Exception as e:
        if json:
            output_error("PAGE_APPEND_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")


@app.command("update")
def page_update(
    page_id: str = typer.Argument(..., help="Page ID"),
    title: str | None = typer.Option(None, "--title", help="New title"),
    properties: str | None = typer.Option(None, "--properties", help="Properties to update"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Update page properties."""
    try:
        session = get_session()
        page = session.get_page(page_id)

        updated = []

        if title:
            page.title = title
            updated.append("title")

        if properties:
            for pair in properties.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    setattr(page, key, value)
                    updated.append(key)

        result = {"id": str(page.id), "updated_fields": updated}

        if json:
            output_json(result)
        else:
            console.print(f"[green]✓ Updated:[/green] {', '.join(updated)}")

    except Exception as e:
        if json:
            output_error("PAGE_UPDATE_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")


@app.command("archive")
def page_archive(
    page_id: str = typer.Argument(..., help="Page ID"),
    unarchive: bool = typer.Option(False, "--unarchive", help="Unarchive instead"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Archive or unarchive a page."""
    try:
        session = get_session()
        page = session.get_page(page_id)

        page.archived = not unarchive

        action = "unarchived" if unarchive else "archived"
        result = {"id": str(page.id), "action": action, "archived": page.archived}

        if json:
            output_json(result)
        else:
            console.print(f"[green]✓ {action.capitalize()}:[/green] {page.title}")

    except Exception as e:
        if json:
            output_error("PAGE_ARCHIVE_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")
