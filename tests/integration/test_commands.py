"""Command-by-command integration tests.

Tests each CLI command individually with the real Notion API.
"""

import json
import os

import pytest
from typer.testing import CliRunner

from notion_cli.cli import app

runner = CliRunner()


@pytest.fixture(scope="module")
def notion_token():
    """Get Notion token from environment."""
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        pytest.skip("NOTION_TOKEN not set")
    return token


class TestAuthCommands:
    """Test auth subcommands."""

    def test_auth_status_json(self, notion_token):
        """Test auth status with JSON output."""
        result = runner.invoke(app, ["auth", "status", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["authenticated"] is True

    def test_auth_status_human(self, notion_token):
        """Test auth status with human-readable output."""
        result = runner.invoke(app, ["auth", "status"])

        assert result.exit_code == 0
        assert "Authenticated" in result.output or "✓" in result.output


class TestSearchCommand:
    """Test search command variations."""

    def test_search_basic(self, notion_token):
        """Basic search."""
        result = runner.invoke(app, ["search", "test", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_search_with_type_page(self, notion_token):
        """Search filtering by page type."""
        result = runner.invoke(app, ["search", "test", "--type", "page", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        for item in data["data"]:
            assert item["type"] == "page"

    def test_search_with_type_database(self, notion_token):
        """Search filtering by database type."""
        result = runner.invoke(app, ["search", "test", "--type", "database", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        for item in data["data"]:
            assert item["type"] == "database"

    def test_search_with_limit(self, notion_token):
        """Search with result limit."""
        result = runner.invoke(app, ["search", "test", "--limit", "5", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert len(data["data"]) <= 5

    def test_search_empty_query(self, notion_token):
        """Search with empty query (returns everything)."""
        result = runner.invoke(app, ["search", "", "--limit", "10", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True


class TestDatabaseCommands:
    """Test database subcommands."""

    def test_db_get_schema(self, notion_token):
        """Get database schema."""
        # First find a database
        search_result = runner.invoke(app, ["search", "", "--type", "database", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No databases available")

        db_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["db", "get", db_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "id" in data["data"]
        assert "title" in data["data"]
        assert "properties" in data["data"]

    def test_db_query_basic(self, notion_token):
        """Query database entries."""
        search_result = runner.invoke(app, ["search", "", "--type", "database", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No databases available")

        db_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["db", "query", db_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_db_query_with_filter(self, notion_token):
        """Query with filter."""
        search_result = runner.invoke(app, ["search", "", "--type", "database", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No databases available")

        db_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["db", "query", db_id, "--filter", "Status=Done", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True


class TestPageCommands:
    """Test page subcommands."""

    def test_page_create(self, notion_token):
        """Create a page."""
        # Find parent
        search_result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No pages available")

        parent_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["page", "create", "--parent", parent_id, "--title", "Test Page", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "id" in data["data"]

        # Store for cleanup
        pytest.page_id = data["data"]["id"]

    def test_page_append(self, notion_token):
        """Append content to page."""
        # Find a page
        search_result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No pages available")

        page_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["page", "append", page_id, "--content", "## Test\n\n- Item 1\n- Item 2", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_page_update(self, notion_token):
        """Update page."""
        search_result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No pages available")

        page_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["page", "update", page_id, "--title", "Updated Title", "--json"])

        assert result.exit_code == 0


class TestGetCommand:
    """Test get command."""

    def test_get_page(self, notion_token):
        """Get page by ID."""
        search_result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No pages available")

        page_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["get", page_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["type"] == "page"

    def test_get_database(self, notion_token):
        """Get database by ID."""
        search_result = runner.invoke(app, ["search", "", "--type", "database", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No databases available")

        db_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["get", db_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["type"] == "database"


class TestSkillsCommands:
    """Test skills subcommands."""

    def test_skills_list(self, notion_token):
        """List all skills."""
        result = runner.invoke(app, ["skills", "list", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "skills" in data["data"]

    def test_skills_show(self, notion_token):
        """Show skill details."""
        result = runner.invoke(app, ["skills", "show", "search", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
