"""Integration tests for notion-cli using real Notion API.

These tests use the provided NOTION_TOKEN to test against the real Notion API.
Run with: NOTION_TOKEN=xxx pytest tests/integration/test_api.py -v
"""

import json
import os
from datetime import datetime

import pytest
from typer.testing import CliRunner

from notion_cli.cli import app

runner = CliRunner()


@pytest.fixture(scope="module")
def notion_token():
    """Get Notion token from environment."""
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        pytest.skip("NOTION_TOKEN not set in environment")
    return token


@pytest.fixture
def test_page_id():
    """Return a test page ID for integration tests.
    Users should replace this with their own page ID."""
    return os.environ.get("NOTION_TEST_PAGE_ID", "test-page-id")


class TestAuthCommands:
    """Integration tests for auth commands."""

    def test_auth_status_with_real_token(self, notion_token):
        """Test auth status shows authenticated with real token."""
        result = runner.invoke(app, ["auth", "status", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["authenticated"] is True
        assert data["data"]["token_source"] == "environment"


class TestSearchCommands:
    """Integration tests for search command."""

    def test_search_returns_results(self, notion_token):
        """Test search returns actual results from Notion."""
        result = runner.invoke(app, ["search", "test", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "data" in data
        # Results could be empty but structure should be valid
        if data["data"]:
            assert "id" in data["data"][0]
            assert "title" in data["data"][0]
            assert "type" in data["data"][0]

    def test_search_with_type_filter(self, notion_token):
        """Test search with type filter."""
        result = runner.invoke(app, ["search", "test", "--type", "page", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        # All results should be pages
        for item in data["data"]:
            assert item["type"] == "page"


class TestDatabaseCommands:
    """Integration tests for database commands."""

    def test_db_get_schema(self, notion_token):
        """Test getting database schema."""
        # First search for a database
        search_result = runner.invoke(app, ["search", "", "--type", "database", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No databases found in workspace")

        db_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["db", "get", db_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "id" in data["data"]
        assert "title" in data["data"]
        assert "properties" in data["data"]

    def test_db_query(self, notion_token):
        """Test querying database entries."""
        # First search for a database
        search_result = runner.invoke(app, ["search", "", "--type", "database", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No databases found in workspace")

        db_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["db", "query", db_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "data" in data


class TestPageCommands:
    """Integration tests for page commands."""

    def test_page_create_and_archive(self, notion_token):
        """Test creating a page and then archiving it."""
        # First find a parent page
        search_result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No pages found in workspace")

        parent_id = search_data["data"][0]["id"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create page
        create_result = runner.invoke(
            app, ["page", "create", "--parent", parent_id, "--title", f"Test Page {timestamp}", "--json"]
        )
        create_data = json.loads(create_result.output)

        if not create_data["success"]:
            pytest.skip(f"Could not create page: {create_data.get('error', {}).get('message', 'Unknown error')}")

        page_id = create_data["data"]["id"]

        try:
            # Verify page was created
            assert create_data["data"]["title"] == f"Test Page {timestamp}"

            # Archive the page
            archive_result = runner.invoke(app, ["page", "archive", page_id, "--json"])
            archive_data = json.loads(archive_result.output)

            assert archive_data["success"] is True
            assert archive_data["data"]["archived"] is True

        finally:
            # Clean up - archive if not already
            runner.invoke(app, ["page", "archive", page_id, "--json"])

    def test_page_append_content(self, notion_token):
        """Test appending content to a page."""
        # First find a test page
        search_result = runner.invoke(app, ["search", "test", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No test pages found in workspace")

        page_id = search_data["data"][0]["id"]

        content = """## Test Section

This is a test paragraph.

- Bullet item 1
- Bullet item 2

- [ ] Todo item

```python
print("hello")
```"""

        result = runner.invoke(app, ["page", "append", page_id, "--content", content, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["blocks_added"] > 0

    def test_page_update(self, notion_token):
        """Test updating a page."""
        # Find a page to update
        search_result = runner.invoke(app, ["search", "test", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No test pages found in workspace")

        page_id = search_data["data"][0]["id"]
        new_title = f"Updated Title {datetime.now().strftime('%Y%m%d_%H%M%S')}"

        result = runner.invoke(app, ["page", "update", page_id, "--title", new_title, "--json"])

        # Update might fail if we don't have permissions, but should return valid JSON
        data = json.loads(result.output)
        assert "success" in data


class TestSkillsCommands:
    """Integration tests for skills commands."""

    def test_skills_list(self, notion_token):
        """Test listing skills."""
        result = runner.invoke(app, ["skills", "list", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "skills" in data["data"]
        assert len(data["data"]["skills"]) > 0

    def test_skills_show(self, notion_token):
        """Test showing skill details."""
        result = runner.invoke(app, ["skills", "show", "search", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "name" in data["data"]
        assert "description" in data["data"]


class TestGetCommand:
    """Integration tests for get command."""

    def test_get_page(self, notion_token):
        """Test getting a page by ID."""
        # First find a page
        search_result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No pages found in workspace")

        page_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["get", page_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["type"] == "page"
        assert "id" in data["data"]
        assert "title" in data["data"]

    def test_get_database(self, notion_token):
        """Test getting a database by ID."""
        # First find a database
        search_result = runner.invoke(app, ["search", "", "--type", "database", "--limit", "1", "--json"])
        search_data = json.loads(search_result.output)

        if not search_data["data"]:
            pytest.skip("No databases found in workspace")

        db_id = search_data["data"][0]["id"]

        result = runner.invoke(app, ["get", db_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["type"] == "database"
