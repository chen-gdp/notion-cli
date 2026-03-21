"""Output formatting for notion-cli.

Provides functions for formatting CLI output as JSON (for agents) or
human-readable tables (for interactive use).
"""

import json
import sys
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


def output_json(data: dict[str, Any], success: bool = True) -> None:
    """Output structured JSON for AI parsing.

    Args:
        data: The data to output (or error data if success=False).
        success: Whether the operation succeeded.

    Raises:
        SystemExit: With code 0 on success, 1 on failure.
    """
    response = {"success": success, "data": data if success else None, "error": data if not success else None}
    console.print(json.dumps(response, indent=2, default=str))
    sys.exit(0 if success else 1)


def output_table(data: list[dict[str, Any]], columns: list[str]) -> None:
    """Output human-readable table.

    Args:
        data: List of dictionaries to display.
        columns: Column names to display.
    """
    if not data:
        console.print("No results found.")
        return

    table = Table(show_header=True, header_style="bold")
    for col in columns:
        table.add_column(col)

    for item in data:
        row = [str(item.get(col, "")) for col in columns]
        table.add_row(*row)

    console.print(table)


def output_error(code: str, message: str, details: dict[str, Any] | None = None) -> None:
    """Output error in consistent format.

    Args:
        code: Error code string.
        message: Human-readable error message.
        details: Optional additional error details.

    Raises:
        SystemExit: Always exits with code 1.
    """
    error_data: dict[str, Any] = {"code": code, "message": message}
    if details:
        error_data["details"] = details
    output_json(error_data, success=False)
