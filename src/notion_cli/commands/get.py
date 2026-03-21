"""Get command for notion-cli."""

from typing import Optional

import typer
from rich.console import Console

from notion_cli.core.output import output_error, output_json, output_table
from notion_cli.core.session import get_session

console = Console()
app = typer.Typer()


@app.command()
def get(
    id: str = typer.Argument(..., help="Page or database ID"),
    blocks: bool = typer.Option(False, "--blocks", help="Include block content for pages"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Get a page or database by ID."""
    try:
        session = get_session()

        # Try to get as page first, then database
        try:
            obj = session.get_page(id)
            obj_type = "page"
        except Exception:
            try:
                obj = session.get_db(id)
                obj_type = "database"
            except Exception:
                output_error("NOT_FOUND", f"No page or database found with ID: {id}")
                return

        # Build result
        result = {
            "id": str(obj.id),
            "type": obj_type,
            "title": obj.title,
            "url": obj.url,
            "created_time": obj.created_time.isoformat() if hasattr(obj, "created_time") and obj.created_time else None,
            "last_edited_time": obj.last_edited_time.isoformat()
            if hasattr(obj, "last_edited_time") and obj.last_edited_time
            else None,
        }

        if obj_type == "page":
            result["archived"] = obj.archived if hasattr(obj, "archived") else False

            if blocks and hasattr(obj, "children"):
                result["blocks"] = [{"type": block.type, "id": str(block.id)} for block in obj.children]
        else:  # database
            result["properties"] = (
                {name: prop.type for name, prop in obj.schema.properties.items()} if hasattr(obj, "schema") else {}
            )

        if json:
            output_json(result)
        else:
            console.print(f"[bold]{result['title']}[/bold] ({result['type']})")
            console.print(f"  ID: {result['id']}")
            console.print(f"  URL: {result['url']}")
            if result.get("archived"):
                console.print("  [red]Archived[/red]")

            if obj_type == "database" and result.get("properties"):
                console.print("\n[bold]Properties:[/bold]")
                for name, prop_type in result["properties"].items():
                    console.print(f"  {name}: {prop_type}")

    except Exception as e:
        if json:
            output_error("GET_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")
