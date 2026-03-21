"""Skills commands for notion-cli."""

import json
from typing import Optional

import typer
from rich.console import Console

from notion_cli.core.output import output_json, output_table

console = Console()
app = typer.Typer()

# Skills registry - populated dynamically
_SKILLS_REGISTRY = {}


def register_skill(name: str, description: str, category: str, usage: str, args: list, options: list, examples: list):
    """Register a skill in the skills registry."""
    _SKILLS_REGISTRY[name] = {
        "name": name,
        "description": description,
        "category": category,
        "usage": usage,
        "args": args,
        "options": options,
        "examples": examples,
    }


def get_all_skills():
    """Get all registered skills."""
    return list(_SKILLS_REGISTRY.values())


@app.command("list")
def skills_list(json: bool = typer.Option(False, "--json", help="Output as JSON")):
    """List all available skills/commands."""
    skills = get_all_skills()

    if not skills:
        # Default skills if registry is empty
        skills = [
            {"name": "search", "description": "Search for pages and databases", "category": "discovery"},
            {"name": "get", "description": "Get page or database by ID", "category": "discovery"},
            {"name": "db get", "description": "Get database schema", "category": "discovery"},
            {"name": "db query", "description": "Query database entries", "category": "content"},
            {"name": "db insert", "description": "Insert entry into database", "category": "content"},
            {"name": "page create", "description": "Create a new page", "category": "content"},
            {"name": "page append", "description": "Append blocks to a page", "category": "content"},
            {"name": "page update", "description": "Update page properties", "category": "content"},
            {"name": "page archive", "description": "Archive or unarchive a page", "category": "content"},
            {"name": "auth setup", "description": "Set up Notion authentication", "category": "config"},
            {"name": "auth status", "description": "Check authentication status", "category": "config"},
        ]

    if json:
        output_json({"total": len(skills), "skills": skills})
    else:
        if not skills:
            console.print("No skills found.")
        else:
            output_table(skills, ["name", "description", "category"])


@app.command("show")
def skills_show(
    name: str = typer.Argument(..., help="Skill name"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Show detailed information about a skill."""
    skill = _SKILLS_REGISTRY.get(name)

    if not skill:
        # Default skill info
        skill_info = {
            "name": name,
            "description": f"Execute the {name} command",
            "category": "general",
            "usage": f"notion {name} [args] [options]",
            "args": [],
            "options": [{"name": "--json", "description": "Output as JSON"}],
            "examples": [f"notion {name} --help"],
        }
    else:
        skill_info = skill

    if json:
        output_json(skill_info)
    else:
        console.print(f"[bold]{skill_info['name']}[/bold]")
        console.print(f"  {skill_info['description']}")
        console.print(f"\nUsage: {skill_info['usage']}")

        if skill_info.get("args"):
            console.print("\nArguments:")
            for arg in skill_info["args"]:
                console.print(f"  {arg['name']}: {arg['description']}")

        if skill_info.get("options"):
            console.print("\nOptions:")
            for opt in skill_info["options"]:
                console.print(f"  {opt['name']}: {opt['description']}")

        if skill_info.get("examples"):
            console.print("\nExamples:")
            for ex in skill_info["examples"]:
                console.print(f"  $ {ex}")
