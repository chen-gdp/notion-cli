"""Search command for notion-cli."""

import typer
from rich.console import Console

from notion_cli.core.output import output_error, output_json, output_table
from notion_cli.core.session import get_session

console = Console()
app = typer.Typer()


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query (matches titles only, not content)"),
    type: str | None = typer.Option(None, "--type", help="Filter by type: page or database"),
    limit: int = typer.Option(100, "--limit", help="Maximum results"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search for pages and databases by title. Note: Searches titles only, not page content/body."""
    try:
        session = get_session()

        # Use appropriate search method based on type filter
        if type == "database":
            raw_results = session.search_db(query, exact=False)
        elif type == "page":
            raw_results = session.search_page(query, exact=False)
        else:
            # Search both and combine
            db_results = session.search_db(query, exact=False)
            page_results = session.search_page(query, exact=False)
            raw_results = list(db_results) + list(page_results)

        # Limit results
        raw_results = raw_results[:limit]

        # Format output
        formatted = []
        for r in raw_results:
            # Determine type using is_page/is_db properties
            if hasattr(r, "is_page") and r.is_page:
                obj_type = "page"
            elif hasattr(r, "is_db") and r.is_db:
                obj_type = "database"
            else:
                obj_type = "unknown"

            formatted.append(
                {
                    "id": str(r.id),
                    "title": r.title,
                    "type": obj_type,
                    "url": r.url,
                    "last_edited_time": r.last_edited_time.isoformat() if r.last_edited_time else None,
                }
            )

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
