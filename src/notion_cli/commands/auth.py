"""Authentication commands for notion-cli."""

import os

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from notion_cli.core.config import get_config
from notion_cli.core.output import output_error, output_json
from notion_cli.core.session import check_auth

console = Console()
app = typer.Typer()


def _validate_token(token: str) -> bool:
    return token.startswith("secret_") or token.startswith("ntn_")


def _save_token(token: str) -> None:
    """Save token to config."""
    config = get_config()
    config.set_token(token)


@app.command("setup")
def auth_setup(
    token: str | None = typer.Option(None, "--token", help="Notion integration token (for non-interactive setup)"),
):
    """Set up Notion authentication."""
    config = get_config()

    if token:
        # Non-interactive mode (for automation/CI)
        if not _validate_token(token):
            output_error("INVALID_TOKEN", "Token must start with 'secret_' or 'ntn_'")
            raise typer.Exit(1)

        _save_token(token)
        console.print("[green]✓ Token saved successfully![/green]")
        console.print(f"Config file: {config.get_config_path()}")
    else:
        # Interactive mode
        console.print(
            Panel.fit(
                "[bold blue]Notion CLI Authentication[/bold blue]\n\n"
                "To use this CLI, you need a Notion integration token.\n"
                "1. Go to https://www.notion.so/my-integrations\n"
                "2. Click 'New integration'\n"
                "3. Give it a name (e.g., 'Notion CLI')\n"
                "4. Copy the 'Internal Integration Token'\n"
                "5. Paste it below",
                title="Setup",
                border_style="blue",
            )
        )

        token = Prompt.ask("Enter your Notion token", password=True)

        if not token:
            output_error("INVALID_INPUT", "Token cannot be empty")
            return

        if not _validate_token(token):
            output_error("INVALID_TOKEN", "Token must start with 'secret_' or 'ntn_'")
            return

        _save_token(token)

        console.print("\n[green]✓ Token saved successfully![/green]")
        console.print(f"Config file: {config.get_config_path()}")


@app.command("status")
def auth_status(json: bool = typer.Option(False, "--json", help="Output as JSON")):
    """Check authentication status."""
    config = get_config()

    if json:
        output_json(
            {
                "authenticated": check_auth(),
                "config_file": str(config.get_config_path()),
                "token_source": "environment" if os.environ.get("NOTION_TOKEN") else "config",
            }
        )
    else:
        if check_auth():
            console.print("[green]✓ Authenticated[/green]")
            console.print(f"Config file: {config.get_config_path()}")
        else:
            console.print("[red]✗ Not authenticated[/red]")
            console.print("Run: notion auth setup")


@app.command("logout")
def auth_logout():
    """Remove saved authentication."""
    config = get_config()
    config.clear_token()
    console.print("[green]✓ Logged out successfully[/green]")
