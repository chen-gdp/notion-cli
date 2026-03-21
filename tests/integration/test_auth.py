"""Integration tests for auth commands."""

import json
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from notion_cli.cli import app

runner = CliRunner()


class TestAuthCommands:
    """Integration tests for auth commands."""

    def test_auth_status_not_authenticated(self, tmp_path: Path):
        """
        Condition: No token configured.
        Expected: Shows not authenticated status.
        """
        with patch.dict("os.environ", {}, clear=True):
            result = runner.invoke(app, ["auth", "status", "--json"])

            assert result.exit_code == 0
            data = json.loads(result.output)
            assert data["success"] is True
            assert data["data"]["authenticated"] is False

    def test_auth_status_with_env_token(self):
        """
        Condition: NOTION_TOKEN set in environment.
        Expected: Shows authenticated status.
        """
        with patch.dict("os.environ", {"NOTION_TOKEN": "secret_test"}):
            result = runner.invoke(app, ["auth", "status", "--json"])

            assert result.exit_code == 0
            data = json.loads(result.output)
            assert data["data"]["authenticated"] is True
            assert data["data"]["token_source"] == "environment"

    def test_auth_setup_invalid_token(self, tmp_path: Path):
        """
        Condition: User enters invalid token.
        Expected: Shows error and exits.
        """
        with patch("rich.prompt.Prompt.ask", return_value="invalid_token"):
            result = runner.invoke(app, ["auth", "setup"])

            assert result.exit_code == 1
            assert "INVALID_TOKEN" in result.output or "must start with" in result.output

    def test_auth_setup_valid_token(self, tmp_path: Path):
        """
        Condition: User enters valid token.
        Expected: Saves token and confirms.
        """
        config_file = tmp_path / ".config" / "notion-cli" / "config.json"

        with (
            patch.object(Path, "home", return_value=tmp_path),
            patch("rich.prompt.Prompt.ask", return_value="secret_valid_token_123"),
        ):
            result = runner.invoke(app, ["auth", "setup"])

            assert result.exit_code == 0
            assert "saved successfully" in result.output
            assert config_file.exists()

    def test_auth_logout_removes_token(self, tmp_path: Path):
        """
        Condition: Token exists in config.
        Expected: Removes token from config.
        """
        config_file = tmp_path / ".config" / "notion-cli" / "config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text('{"token": "secret_xxx"}')

        with patch.object(Path, "home", return_value=tmp_path):
            result = runner.invoke(app, ["auth", "logout"])

            assert result.exit_code == 0
            assert "Logged out" in result.output
