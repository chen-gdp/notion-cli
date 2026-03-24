"""Main CLI entry point for notion-cli."""

import typer

from notion_cli.commands import auth, database, get, page, skills
from notion_cli.commands.search import search as search_cmd

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
