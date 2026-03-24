"""Main CLI entry point for notion-cli."""

import typer
from rich.console import Console

from notion_cli.commands import auth, database, get, page, skills
from notion_cli.commands.search import search as search_cmd
from notion_cli.core.output import output_json, output_table
from notion_cli.core.session import get_session

console = Console()
app = typer.Typer(
    name="notion",
    help="Notion CLI for AI agents",
    no_args_is_help=True,
)

# Add subcommands
app.add_typer(auth.app, name="auth")
app.add_typer(database.app, name="db")
app.add_typer(get.app, name="get")
app.add_typer(page.app, name="page")
app.add_typer(skills.app, name="skills")


# Add search as a direct command (not a subcommand group)
@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    type: str | None = typer.Option(None, "--type", help="Filter by type: page or database"),
    limit: int = typer.Option(100, "--limit", help="Maximum results"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search for pages and databases in Notion."""
    search_cmd(query, type, limit, json)


@app.command(name="ls")
def ls_cmd(
    type: str | None = typer.Option(None, "--type", help="Filter by type: page or database"),
    limit: int = typer.Option(100, "--limit", help="Maximum results"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """List all pages and databases (no search query required)."""
    try:
        session = get_session()

        if type == "database":
            raw_results = session.search_db("", exact=False)
        elif type == "page":
            raw_results = session.search_page("", exact=False)
        else:
            db_results = session.search_db("", exact=False)
            page_results = session.search_page("", exact=False)
            raw_results = list(db_results) + list(page_results)

        raw_results = raw_results[:limit]

        formatted = [
            {
                "id": str(r.id),
                "title": r.title,
                "type": r.object,
                "url": r.url,
                "last_edited_time": r.last_edited_time.isoformat() if r.last_edited_time else None,
            }
            for r in raw_results
        ]

        if json:
            output_json(formatted)
        else:
            if not formatted:
                console.print("No results found. Your integration may not have access to any pages.")
                console.print("Try: Share a page in Notion → Add connections → Select your integration")
            else:
                output_table(formatted, ["title", "type", "id", "last_edited_time"])

    except Exception as e:
        if json:
            from notion_cli.core.output import output_error

            output_error("LIST_ERROR", str(e))
        else:
            console.print(f"[red]Error:[/red] {e}")


@app.callback()
def main(
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    version: bool = typer.Option(False, "--version", help="Show version"),
):
    """Notion CLI - Interact with Notion from the command line."""
    if version:
        typer.echo("notion-cli 0.1.0")
        raise typer.Exit()


if __name__ == "__main__":
    app()
