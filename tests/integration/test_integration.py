"""Integration tests for notion-cli.

These tests require a valid NOTION_TOKEN environment variable.
They test real API interactions with Notion.

Run with: NOTION_TOKEN=xxx uv run pytest tests/integration/ -v
"""

import json
import os
import subprocess

import pytest

# Skip all tests if no token is available
pytestmark = [
    pytest.mark.skipif(
        not os.environ.get("NOTION_TOKEN"),
        reason="NOTION_TOKEN environment variable not set",
    ),
    pytest.mark.integration,
]


class TestAuthCommands:
    """Test authentication commands."""

    def test_auth_status_with_token(self):
        """Test that auth status shows authenticated when token is set."""
        result = subprocess.run(
            ["notion", "auth", "status", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert data["data"]["authenticated"] is True
        assert data["data"]["token_source"] in ["environment", "config"]


class TestSearchCommands:
    """Test search functionality."""

    def test_search_returns_valid_structure(self):
        """Test that search returns expected JSON structure."""
        result = subprocess.run(
            ["notion", "search", "test", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert "success" in data
        assert data["success"] is True
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_search_with_type_filter(self):
        """Test search with --type filter."""
        # Search for databases
        result = subprocess.run(
            ["notion", "search", "test", "--type", "database", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True

        # All results should be databases if any exist
        for item in data["data"]:
            assert item["type"] == "database"

    def test_search_empty_query(self):
        """Test search with empty string returns all content."""
        result = subprocess.run(
            ["notion", "search", "", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True


class TestGetCommands:
    """Test get command for pages and databases."""

    def test_get_page_by_id(self, existing_page_id):
        """Test getting a page by ID."""
        result = subprocess.run(
            ["notion", "get", existing_page_id, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert data["data"]["type"] == "page"
        assert "id" in data["data"]
        assert "title" in data["data"]

    def test_get_nonexistent_page(self):
        """Test getting a non-existent page returns error."""
        result = subprocess.run(
            ["notion", "get", "nonexistent-page-id", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Should return error
        data = json.loads(result.stdout)
        assert data["success"] is False
        assert "error" in data


class TestDatabaseCommands:
    """Test database operations."""

    def test_db_get_schema(self, existing_database_id):
        """Test getting database schema."""
        result = subprocess.run(
            ["notion", "db", "get", existing_database_id, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert "properties" in data["data"]

    def test_db_query(self, existing_database_id):
        """Test querying database entries."""
        result = subprocess.run(
            ["notion", "db", "query", existing_database_id, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert isinstance(data["data"], list)


class TestPageCommands:
    """Test page operations."""

    def test_page_create_in_database(self, existing_database_id):
        """Test creating a page in a database."""
        result = subprocess.run(
            [
                "notion",
                "page",
                "create",
                "--parent",
                existing_database_id,
                "--title",
                "Test Page from Integration Test",
                "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert "id" in data["data"]

        # Clean up: archive the test page
        page_id = data["data"]["id"]
        subprocess.run(
            ["notion", "page", "archive", page_id, "--json"],
            capture_output=True,
            check=False,
        )

    def test_page_append_content(self, existing_page_id):
        """Test appending content to a page."""
        result = subprocess.run(
            [
                "notion",
                "page",
                "append",
                existing_page_id,
                "--content",
                "## Test Section\n\nThis is a test.",
                "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True


class TestSkillsCommands:
    """Test skills discovery."""

    def test_skills_list(self):
        """Test listing available skills/commands."""
        result = subprocess.run(
            ["notion", "skills", "list", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert isinstance(data["data"], list)

        # Should have at least these core skills
        skill_names = [s["name"] for s in data["data"]]
        assert "search" in skill_names
        assert "auth" in skill_names


class TestCompleteWorkflow:
    """Test complete workflows combining multiple commands."""

    def test_search_and_get_workflow(self):
        """Test searching and then getting a specific item."""
        # Step 1: Search for content
        search_result = subprocess.run(
            ["notion", "search", "test", "--limit", "1", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        if search_result.returncode != 0:
            pytest.skip("No content found to test with")

        search_data = json.loads(search_result.stdout)
        if not search_data["data"]:
            pytest.skip("No content found to test with")

        item_id = search_data["data"][0]["id"]

        # Step 2: Get the specific item
        get_result = subprocess.run(
            ["notion", "get", item_id, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert get_result.returncode == 0
        get_data = json.loads(get_result.stdout)
        assert get_data["success"] is True
        assert get_data["data"]["id"] == item_id

    def test_create_and_archive_workflow(self, existing_database_id):
        """Test creating a page and then archiving it."""
        # Step 1: Create a test page
        create_result = subprocess.run(
            [
                "notion",
                "page",
                "create",
                "--parent",
                existing_database_id,
                "--title",
                "Integration Test Page (Temporary)",
                "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert create_result.returncode == 0
        create_data = json.loads(create_result.stdout)
        page_id = create_data["data"]["id"]

        # Step 2: Archive the page
        archive_result = subprocess.run(
            ["notion", "page", "archive", page_id, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert archive_result.returncode == 0
        archive_data = json.loads(archive_result.stdout)
        assert archive_data["success"] is True


class TestListCommands:
    """Test list (ls) command."""

    def test_ls_returns_valid_structure(self):
        """Test that ls returns expected JSON structure."""
        result = subprocess.run(
            ["notion", "ls", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert "success" in data
        assert data["success"] is True
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_ls_with_type_filter(self):
        """Test ls with --type filter."""
        # List only pages
        result = subprocess.run(
            ["notion", "ls", "--type", "page", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True

        # All results should be pages if any exist
        for item in data["data"]:
            assert item["type"] == "page"


class TestAuthSetupCommand:
    """Test auth setup command."""

    def test_auth_setup_with_token(self):
        """Test auth setup with --token flag."""
        # Get existing token
        token = os.environ.get("NOTION_TOKEN", "")
        if not token:
            pytest.skip("NOTION_TOKEN not set")

        result = subprocess.run(
            ["notion", "auth", "setup", "--token", token, "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True

    def test_auth_logout(self):
        """Test auth logout command."""
        result = subprocess.run(
            ["notion", "auth", "logout"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Should succeed (no json output for logout)
        assert result.returncode == 0

        # Restore token for other tests
        token = os.environ.get("NOTION_TOKEN", "")
        if token:
            subprocess.run(
                ["notion", "auth", "setup", "--token", token],
                capture_output=True,
                check=False,
            )


class TestPageUpdateCommand:
    """Test page update command."""

    def test_page_update_title(self, existing_page_id):
        """Test updating page title."""
        result = subprocess.run(
            [
                "notion",
                "page",
                "update",
                existing_page_id,
                "--title",
                "Updated Title for Test",
                "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True

    def test_page_update_properties(self, existing_database_id):
        """Test updating page properties."""
        # First create a page in database
        create_result = subprocess.run(
            [
                "notion",
                "page",
                "create",
                "--parent",
                existing_database_id,
                "--title",
                "Test Page for Update",
                "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if create_result.returncode != 0:
            pytest.skip("Could not create test page")

        create_data = json.loads(create_result.stdout)
        page_id = create_data["data"]["id"]

        subprocess.run(
            [
                "notion",
                "page",
                "update",
                page_id,
                "--properties",
                "Status=Done",
                "--json",
            ],
            capture_output=True,
            check=False,
        )

        # Clean up
        subprocess.run(
            ["notion", "page", "archive", page_id, "--json"],
            capture_output=True,
            check=False,
        )


class TestDbInsertCommand:
    """Test database insert command."""

    def test_db_insert_creates_entry(self, existing_database_id):
        """Test inserting a new entry into database."""
        result = subprocess.run(
            [
                "notion",
                "db",
                "insert",
                existing_database_id,
                "--title",
                "Test Entry from Integration Test",
                "--json",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert "id" in data["data"]

        # Clean up: archive the created entry
        entry_id = data["data"]["id"]
        subprocess.run(
            ["notion", "page", "archive", entry_id, "--json"],
            capture_output=True,
            check=False,
        )


class TestSkillsShowCommand:
    """Test skills show command."""

    def test_skills_show_search(self):
        """Test showing details for search skill."""
        result = subprocess.run(
            ["notion", "skills", "show", "search", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert "name" in data["data"]
        assert data["data"]["name"] == "search"

    def test_skills_show_db_query(self):
        """Test showing details for db_query skill."""
        result = subprocess.run(
            ["notion", "skills", "show", "db_query", "--json"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Command failed: {result.stderr}"

        data = json.loads(result.stdout)
        assert data["success"] is True
        assert data["data"]["name"] == "db_query"


# Fixtures
@pytest.fixture
def existing_page_id():
    """Get an existing page ID for testing."""
    result = subprocess.run(
        ["notion", "ls", "--type", "page", "--limit", "1", "--json"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        pytest.skip("Could not find existing page")

    data = json.loads(result.stdout)
    if not data.get("data"):
        pytest.skip("No pages found in workspace")

    return data["data"][0]["id"]


@pytest.fixture
def existing_database_id():
    """Get an existing database ID for testing."""
    result = subprocess.run(
        ["notion", "ls", "--type", "database", "--limit", "1", "--json"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        pytest.skip("Could not find existing database")

    data = json.loads(result.stdout)
    if not data.get("data"):
        pytest.skip("No databases found in workspace")

    return data["data"][0]["id"]
