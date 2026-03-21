"""Search command for notion-cli."""

from typing import Optional

import typer
from rich.console import Console

from notion_cli.core.output import output_error, output_json, output_table
from notion_cli.core.session import get_session

console = Console()
app = typer.Typer()


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    type: Optional[str] = typer.Option(None, "--type", help="Filter by type: page or database"),
    limit: int = typer.Option(100, "--limit", help="Maximum results"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search for pages and databases in Notion."""
    try:
        session = get_session()
        results = session.search(query)

        # Filter by type if specified
        if type:
            type_lower = type.lower()
            results = [r for r in results if r.object == type_lower]

        # Limit results
        results = results[:limit]

        # Format output
        formatted = [
            {
                "id": str(r.id),
                "title": r.title,
                "type": r.object,
                "url": r.url,
                "last_edited_time": r.last_edited_time.isoformat() if r.last_edited_time else None,
            }
            for r in results
        ]

        if json:
            output_json(formatted)
        else:
            if not formatted:
                console.print("No results found.")
            else:
                output_table(formatted, ["title", "type", "id", "last_edited_time"])

    except Exception as e:
        if json:
            output_error("SEARCH_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")
