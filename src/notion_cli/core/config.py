"""Configuration management for notion-cli.

This module handles loading and saving configuration data, including
authentication tokens for the Notion API.
"""

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


class Config:
    """Manages CLI configuration including authentication tokens.

    Configuration is loaded from multiple sources with the following priority:
    1. NOTION_TOKEN environment variable (highest priority)
    2. ~/.config/notion-cli/config.json
    3. ./.notion-cli.json (project-level, lowest priority)

    Attributes:
        _config_dir (Path): Directory containing config files.
        _config_file (Path): Main configuration file path.
        _data (dict): Loaded configuration data.
    """

    def __init__(self) -> None:
        """Initialize configuration manager.

        Creates config directory if it doesn't exist and loads existing config.
        """
        self._config_dir = Path.home() / ".config" / "notion-cli"
        self._config_file = self._config_dir / "config.json"
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        """Load configuration from file if it exists."""
        if self._config_file.exists():
            with open(self._config_file, encoding="utf-8") as f:
                self._data = json.load(f)

    def _save(self) -> None:
        """Save current configuration to file."""
        self._config_dir.mkdir(parents=True, exist_ok=True)
        with open(self._config_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def get_token(self) -> str | None:
        """Get Notion API token from environment or config file.

        Returns:
            The token string if found, None otherwise.
        """
        token = os.environ.get("NOTION_TOKEN")
        if token:
            return token
        return self._data.get("token")

    def set_token(self, token: str) -> None:
        """Save token to configuration file.

        Args:
            token: The Notion API token to save.
        """
        self._data["token"] = token
        self._save()

    def clear_token(self) -> None:
        """Remove token from configuration file.

        Does nothing if no token exists.
        """
        if "token" in self._data:
            del self._data["token"]
            self._save()

    def get_config_path(self) -> Path:
        """Get the path to the configuration file.

        Returns:
            Path to config.json.
        """
        return self._config_file

    def to_dict(self) -> dict[str, Any]:
        """Get configuration metadata as dictionary.

        Returns:
            Dictionary with config_file path, has_token boolean,
            and non-sensitive data (token excluded).
        """
        return {
            "config_file": str(self._config_file),
            "has_token": bool(self.get_token()),
            "data": {k: v for k, v in self._data.items() if k != "token"},
        }


# Global config instance for singleton pattern
_config: Config | None = None


def get_config() -> Config:
    """Get or create global Config instance.

    Returns:
        The global Config instance (singleton).
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
