"""Skills registry and SKILLS.md generator for notion-cli.

Provides functionality to auto-generate SKILLS.md documentation
from registered CLI commands.
"""

from pathlib import Path
from typing import Any


class SkillRegistry:
    """Registry for CLI skills/commands.

    Manages skill metadata and generates SKILLS.md documentation.
    """

    def __init__(self) -> None:
        """Initialize empty skill registry."""
        self._skills: dict[str, dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        category: str,
        usage: str,
        args: list[dict[str, Any]],
        options: list[dict[str, Any]],
        examples: list[str],
        returns: dict[str, Any] | None = None,
    ) -> None:
        """Register a skill in the registry.

        Args:
            name: Skill/command name
            description: Human-readable description
            category: Skill category (discovery, content, config)
            usage: Command usage string
            args: List of argument definitions
            options: List of option definitions
            examples: List of example commands
            returns: Optional return value schema
        """
        self._skills[name] = {
            "name": name,
            "description": description,
            "category": category,
            "usage": usage,
            "args": args,
            "options": options,
            "examples": examples,
            "returns": returns or {},
        }

    def get(self, name: str) -> dict[str, Any] | None:
        """Get skill by name.

        Args:
            name: Skill name to lookup

        Returns:
            Skill dict or None if not found
        """
        return self._skills.get(name)

    def list_all(self) -> list[dict[str, Any]]:
        """List all registered skills.

        Returns:
            List of all skill definitions
        """
        return list(self._skills.values())

    def generate_skills_md(self, output_path: Path | None = None) -> str:
        """Generate SKILLS.md content.

        Args:
            output_path: Optional path to write file to

        Returns:
            Generated markdown content
        """
        lines = ["# Notion CLI Skills\n\n"]
        lines.append("Auto-generated documentation of available CLI commands.\n\n")

        # Group by category
        by_category: dict[str, list[dict]] = {}
        for skill in self._skills.values():
            cat = skill["category"]
            by_category.setdefault(cat, []).append(skill)

        # Generate TOC
        lines.append("## Table of Contents\n\n")
        for category in sorted(by_category.keys()):
            lines.append(f"- [{category.capitalize()}](#{category})\n")
        lines.append("\n")

        # Generate sections
        for category in sorted(by_category.keys()):
            lines.append(f"## {category.capitalize()}\n\n")
            for skill in sorted(by_category[category], key=lambda s: s["name"]):
                lines.extend(self._generate_skill_doc(skill))

        content = "".join(lines)

        if output_path:
            output_path.write_text(content, encoding="utf-8")

        return content

    def _generate_skill_doc(self, skill: dict[str, Any]) -> list[str]:
        """Generate documentation for a single skill.

        Args:
            skill: Skill definition dict

        Returns:
            List of markdown lines
        """
        lines = []
        lines.append(f"### {skill['name']}\n\n")
        lines.append(f"{skill['description']}\n\n")

        # Usage
        lines.append("**Usage:**\n\n")
        lines.append(f"```bash\n{skill['usage']}\n```\n\n")

        # Arguments
        if skill["args"]:
            lines.append("**Arguments:**\n\n")
            for arg in skill["args"]:
                req = " (required)" if arg.get("required") else " (optional)"
                lines.append(f"- `{arg['name']}`{req}: {arg['description']}\n")
            lines.append("\n")

        # Options
        if skill["options"]:
            lines.append("**Options:**\n\n")
            for opt in skill["options"]:
                lines.append(f"- `{opt['name']}`: {opt['description']}\n")
            lines.append("\n")

        # Examples
        if skill["examples"]:
            lines.append("**Examples:**\n\n")
            for ex in skill["examples"]:
                lines.append(f"```bash\n{ex}\n```\n\n")

        lines.append("---\n\n")
        return lines


# Global registry instance
_registry: SkillRegistry | None = None


def get_registry() -> SkillRegistry:
    """Get or create global skill registry.

    Returns:
        Global SkillRegistry instance (singleton)
    """
    global _registry
    if _registry is None:
        _registry = SkillRegistry()
    return _registry


def generate_skills_md(output_path: Path | None = None) -> str:
    """Generate SKILLS.md from global registry.

    Args:
        output_path: Optional path to write file

    Returns:
        Generated markdown content
    """
    return get_registry().generate_skills_md(output_path)
