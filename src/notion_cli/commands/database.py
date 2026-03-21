"""Database commands for notion-cli."""

import typer
from rich.console import Console

from notion_cli.core.output import output_error, output_json, output_table
from notion_cli.core.session import get_session

console = Console()
app = typer.Typer()


@app.command("get")
def db_get(
    database_id: str = typer.Argument(..., help="Database ID"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Get database schema."""
    try:
        session = get_session()
        db = session.get_db(database_id)

        result = {
            "id": str(db.id),
            "title": db.title,
            "properties": {name: prop.type for name, prop in db.schema.properties.items()},
        }

        if json:
            output_json(result)
        else:
            console.print(f"[bold]{db.title}[/bold]")
            for name, prop_type in result["properties"].items():
                console.print(f"  {name}: {prop_type}")

    except Exception as e:
        if json:
            output_error("DB_GET_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")


@app.command("query")
def db_query(
    database_id: str = typer.Argument(..., help="Database ID"),
    filter: str | None = typer.Option(None, "--filter", help="Filter criteria (key=value,key2=value2)"),
    limit: int = typer.Option(100, "--limit", help="Maximum results"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Query database entries."""
    try:
        session = get_session()
        db = session.get_db(database_id)

        # Build filter from string
        filters = {}
        if filter:
            for pair in filter.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    filters[key] = value

        # Query database
        results = db.query().execute()

        # Format output
        formatted = []
        for page in results[:limit]:
            formatted.append({"id": str(page.id), "title": page.title, "url": page.url})

        if json:
            output_json(formatted)
        else:
            if not formatted:
                console.print("No results found.")
            else:
                output_table(formatted, ["title", "id"])

    except Exception as e:
        if json:
            output_error("DB_QUERY_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")


@app.command("insert")
def db_insert(
    database_id: str = typer.Argument(..., help="Database ID"),
    title: str = typer.Option(..., "--title", help="Entry title"),
    properties: str | None = typer.Option(None, "--properties", help="Properties (key=value,key2=value2)"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Insert a new entry into database."""
    try:
        session = get_session()
        db = session.get_db(database_id)

        # Build properties dict
        props = {"title": title}
        if properties:
            for pair in properties.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    props[key] = value

        # Create page
        page = db.create_page(**props)

        result = {"id": str(page.id), "title": page.title, "url": page.url}

        if json:
            output_json(result)
        else:
            console.print(f"[green]✓ Created:[/green] {page.title}")
            console.print(f"  ID: {page.id}")

    except Exception as e:
        if json:
            output_error("DB_INSERT_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")
