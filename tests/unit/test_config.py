"""Tests for the config module."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from notion_cli.core.config import Config, get_config


class TestConfig:
    """Tests for Config class."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, tmp_path: Path):
        """Setup and teardown for each test."""
        # Store original env var
        self.original_token = os.environ.get("NOTION_TOKEN")

        # Clear env var for isolation
        if "NOTION_TOKEN" in os.environ:
            del os.environ["NOTION_TOKEN"]

        # Reset global config instance
        import notion_cli.core.config as config_module

        config_module._config = None

        # Patch Path.home() to return tmp_path for config directory
        self.config_dir = tmp_path / ".config" / "notion-cli"
        self.config_file = self.config_dir / "config.json"

        with patch.object(Path, "home", return_value=tmp_path):
            yield

        # Restore original env var
        if self.original_token:
            os.environ["NOTION_TOKEN"] = self.original_token
        elif "NOTION_TOKEN" in os.environ:
            del os.environ["NOTION_TOKEN"]

    def test_config_creates_directory_on_save(self):
        """
        Condition: Config directory does not exist.
        Expected: Config directory is created when saving data.
        """
        config = Config()
        config.set_token("test_token")

        assert self.config_dir.exists()

    def test_get_token_from_environment_variable(self):
        """
        Condition: NOTION_TOKEN environment variable is set.
        Expected: Token is retrieved from environment variable.
        """
        os.environ["NOTION_TOKEN"] = "secret_env_token"
        config = Config()

        token = config.get_token()

        assert token == "secret_env_token"

    def test_get_token_from_config_file(self):
        """
        Condition: Config file exists with token, env var not set.
        Expected: Token is retrieved from config file.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_data = {"token": "secret_file_token"}
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

        config = Config()
        token = config.get_token()

        assert token == "secret_file_token"

    def test_env_var_takes_priority_over_config_file(self):
        """
        Condition: Both env var and config file have tokens.
        Expected: Environment variable token takes priority.
        """
        os.environ["NOTION_TOKEN"] = "secret_env_token"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_data = {"token": "secret_file_token"}
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

        config = Config()
        token = config.get_token()

        assert token == "secret_env_token"

    def test_get_token_returns_none_when_no_token(self):
        """
        Condition: No env var and no config file.
        Expected: Returns None.
        """
        config = Config()

        token = config.get_token()

        assert token is None

    def test_set_token_saves_to_config_file(self):
        """
        Condition: Token is set via set_token method.
        Expected: Token is saved to config file.
        """
        config = Config()
        config.set_token("new_secret_token")

        assert self.config_file.exists()
        with open(self.config_file) as f:
            data = json.load(f)
        assert data["token"] == "new_secret_token"

    def test_set_token_updates_existing_config(self):
        """
        Condition: Config file exists with existing data.
        Expected: Token is added while preserving other data.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        existing_data = {"other_key": "other_value"}
        with open(self.config_file, "w") as f:
            json.dump(existing_data, f)

        config = Config()
        config.set_token("new_token")

        with open(self.config_file) as f:
            data = json.load(f)
        assert data["token"] == "new_token"
        assert data["other_key"] == "other_value"

    def test_clear_token_removes_from_config(self):
        """
        Condition: Config file has token.
        Expected: Token is removed from config file.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_data = {"token": "to_be_removed", "other": "data"}
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

        config = Config()
        config.clear_token()

        with open(self.config_file) as f:
            data = json.load(f)
        assert "token" not in data
        assert data["other"] == "data"

    def test_clear_token_when_no_token_does_nothing(self):
        """
        Condition: Config file has no token.
        Expected: No error raised, other data preserved.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_data = {"other": "data"}
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

        config = Config()
        config.clear_token()  # Should not raise

        with open(self.config_file) as f:
            data = json.load(f)
        assert data == {"other": "data"}

    def test_get_config_path_returns_correct_path(self):
        """
        Condition: Config is initialized.
        Expected: Returns the correct config file path.
        """
        config = Config()

        path = config.get_config_path()

        assert path == self.config_file

    def test_to_dict_hides_token(self):
        """
        Condition: Config has token.
        Expected: to_dict returns metadata without exposing token.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_data = {"token": "secret", "other": "value"}
        with open(self.config_file, "w") as f:
            json.dump(config_data, f)

        config = Config()
        result = config.to_dict()

        assert result["has_token"] is True
        assert "token" not in result["data"]
        assert result["data"]["other"] == "value"
        assert "config_file" in result

    def test_to_dict_when_no_token(self):
        """
        Condition: Config has no token.
        Expected: has_token is False.
        """
        config = Config()
        result = config.to_dict()

        assert result["has_token"] is False


class TestGetConfig:
    """Tests for get_config function."""

    def test_get_config_returns_same_instance(self, tmp_path: Path):
        """
        Condition: get_config is called multiple times.
        Expected: Returns the same Config instance (singleton).
        """
        # Reset global instance
        import notion_cli.core.config as config_module

        config_module._config = None

        with patch.object(Path, "home", return_value=tmp_path):
            config1 = get_config()
            config2 = get_config()

            assert config1 is config2

    def test_get_config_creates_new_instance_when_none(self, tmp_path: Path):
        """
        Condition: No global config exists.
        Expected: Creates and returns new Config instance.
        """
        # Reset global instance
        import notion_cli.core.config as config_module

        config_module._config = None

        with patch.object(Path, "home", return_value=tmp_path):
            config = get_config()

            assert isinstance(config, Config)
