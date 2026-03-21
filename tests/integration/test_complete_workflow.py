"""Complete integration tests for all notion-cli commands.

These tests cover real-world use cases:
1. Task management workflow
2. Documentation creation workflow
3. Database operations workflow
4. Research organization workflow

Run with: NOTION_TOKEN=xxx pytest tests/integration/test_complete_workflow.py -v
"""

import contextlib
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
def unique_id():
    """Generate unique ID for test resources."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


class TestTaskManagementWorkflow:
    """Test complete task/issue tracking workflow."""

    def test_01_find_tasks_database(self, notion_token, unique_id):
        """Find or create a tasks database."""
        # Search for existing tasks database
        result = runner.invoke(app, ["search", "tasks", "--type", "database", "--json"])
        data = json.loads(result.output)

        if data["success"] and data["data"]:
            pytest.tasks_db_id = data["data"][0]["id"]
            print(f"Found tasks DB: {pytest.tasks_db_id}")
        else:
            pytest.skip("No tasks database found")

    def test_02_query_open_tasks(self, notion_token):
        """Query for open high priority tasks."""
        if not hasattr(pytest, "tasks_db_id"):
            pytest.skip("No tasks database available")

        result = runner.invoke(app, ["db", "query", pytest.tasks_db_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "data" in data

        # Store first task for update test
        if data["data"]:
            pytest.test_task_id = data["data"][0]["id"]

    def test_03_create_new_task(self, notion_token, unique_id):
        """Create a new task in the database."""
        if not hasattr(pytest, "tasks_db_id"):
            pytest.skip("No tasks database available")

        task_title = f"Integration Test Task {unique_id}"
        result = runner.invoke(
            app,
            [
                "db",
                "insert",
                pytest.tasks_db_id,
                "--title",
                task_title,
                "--properties",
                "Status=Not started,Priority=High",
                "--json",
            ],
        )

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["title"] == task_title

        # Store for later tests
        pytest.created_task_id = data["data"]["id"]
        pytest.created_task_title = task_title

    def test_04_update_task_status(self, notion_token):
        """Update task status to In progress."""
        if not hasattr(pytest, "created_task_id"):
            pytest.skip("No task created")

        result = runner.invoke(
            app, ["page", "update", pytest.created_task_id, "--properties", "Status=In progress", "--json"]
        )

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_05_archive_completed_task(self, notion_token):
        """Archive the task when done."""
        if not hasattr(pytest, "created_task_id"):
            pytest.skip("No task created")

        result = runner.invoke(app, ["page", "archive", pytest.created_task_id, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["archived"] is True


class TestDocumentationWorkflow:
    """Test documentation creation and maintenance workflow."""

    def test_01_find_wiki_database(self, notion_token, unique_id):
        """Find or create documentation database."""
        result = runner.invoke(app, ["search", "wiki", "--type", "database", "--json"])
        data = json.loads(result.output)

        if data["success"] and data["data"]:
            pytest.wiki_db_id = data["data"][0]["id"]
        else:
            # Try to find any page to use as parent
            result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
            data = json.loads(result.output)
            if data["data"]:
                pytest.wiki_parent_id = data["data"][0]["id"]
            else:
                pytest.skip("No wiki database or pages found")

    def test_02_create_documentation_page(self, notion_token, unique_id):
        """Create a new documentation page."""
        doc_title = f"API Documentation {unique_id}"

        if hasattr(pytest, "wiki_db_id"):
            # Create in database
            result = runner.invoke(
                app,
                [
                    "db",
                    "insert",
                    pytest.wiki_db_id,
                    "--title",
                    doc_title,
                    "--properties",
                    "Category=Reference",
                    "--json",
                ],
            )
        elif hasattr(pytest, "wiki_parent_id"):
            # Create as child page
            result = runner.invoke(
                app, ["page", "create", "--parent", pytest.wiki_parent_id, "--title", doc_title, "--json"]
            )
        else:
            pytest.skip("No location for documentation")

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

        pytest.doc_page_id = data["data"]["id"]
        pytest.doc_title = doc_title

    def test_03_add_documentation_content(self, notion_token):
        """Add structured content to documentation."""
        if not hasattr(pytest, "doc_page_id"):
            pytest.skip("No documentation page created")

        content = """## Overview

This document describes the API endpoints.

## Authentication

Use Bearer token authentication:

```bash
curl -H "Authorization: Bearer TOKEN" https://api.example.com
```

## Endpoints

- GET /users - List all users
- POST /users - Create new user
- DELETE /users/:id - Delete user

## Rate Limiting

- [ ] Implement rate limiting
- [ ] Add retry logic
- [ ] Document error codes

For questions, contact the API team."""

        result = runner.invoke(app, ["page", "append", pytest.doc_page_id, "--content", content, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["blocks_added"] > 0

    def test_04_update_documentation(self, notion_token, unique_id):
        """Update documentation with new information."""
        if not hasattr(pytest, "doc_page_id"):
            pytest.skip("No documentation page")

        new_title = f"{pytest.doc_title} (Updated)"
        result = runner.invoke(app, ["page", "update", pytest.doc_page_id, "--title", new_title, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_05_get_page_with_blocks(self, notion_token):
        """Retrieve page with its content."""
        if not hasattr(pytest, "doc_page_id"):
            pytest.skip("No documentation page")

        result = runner.invoke(app, ["get", pytest.doc_page_id, "--blocks", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert data["data"]["type"] == "page"


class TestResearchWorkflow:
    """Test research and notes organization workflow."""

    def test_01_search_for_existing_research(self, notion_token, unique_id):
        """Search for existing research on a topic."""
        topic = "competitor analysis"

        # Search pages
        result = runner.invoke(app, ["search", topic, "--type", "page", "--json"])
        page_data = json.loads(result.output)

        # Search databases
        result = runner.invoke(app, ["search", topic, "--type", "database", "--json"])
        db_data = json.loads(result.output)

        # Combined results
        all_results = []
        if page_data["success"]:
            all_results.extend(page_data["data"])
        if db_data["success"]:
            all_results.extend(db_data["data"])

        pytest.existing_research = all_results
        print(f"Found {len(all_results)} existing research items")

    def test_02_create_research_database(self, notion_token, unique_id):
        """Create a database for research findings."""
        # Find a parent page
        result = runner.invoke(app, ["search", "", "--type", "page", "--limit", "1", "--json"])
        data = json.loads(result.output)

        if not data["data"]:
            pytest.skip("No parent page available")

        parent_id = data["data"][0]["id"]

        # Create research database (this would need to be implemented)
        # For now, create a page instead
        result = runner.invoke(
            app, ["page", "create", "--parent", parent_id, "--title", f"Research {unique_id}", "--json"]
        )

        if result.exit_code == 0:
            data = json.loads(result.output)
            if data["success"]:
                pytest.research_page_id = data["data"]["id"]

    def test_03_add_research_findings(self, notion_token, unique_id):
        """Add structured research findings."""
        if not hasattr(pytest, "research_page_id"):
            pytest.skip("No research page")

        content = f"""## Competitor Analysis {unique_id}

### Competitor A
- **Strengths:** Fast API, good docs
- **Weaknesses:** Expensive, limited features

### Competitor B
- **Strengths:** Free tier, easy setup
- **Weaknesses:** Poor support, slow response

### Action Items

- [ ] Analyze pricing models
- [ ] Review feature gaps
- [ ] Create comparison matrix

Last updated: {unique_id}"""

        result = runner.invoke(app, ["page", "append", pytest.research_page_id, "--content", content, "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True

    def test_04_incremental_updates(self, notion_token, unique_id):
        """Add more findings incrementally."""
        if not hasattr(pytest, "research_page_id"):
            pytest.skip("No research page")

        additional = f"""### Competitor C (Added {unique_id})

New findings from today:
- Emerging player in market
- Strong community support
- Open source option available

## Summary

Three main competitors identified. Detailed analysis in progress."""

        result = runner.invoke(app, ["page", "append", pytest.research_page_id, "--content", additional, "--json"])

        assert result.exit_code == 0


class TestSkillsDiscovery:
    """Test skills/commands discovery."""

    def test_list_all_skills(self, notion_token):
        """List all available skills/commands."""
        result = runner.invoke(app, ["skills", "list", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        assert "skills" in data["data"]
        assert len(data["data"]["skills"]) > 0

        # Store for verification
        pytest.all_skills = data["data"]["skills"]

    def test_show_skill_details(self, notion_token):
        """Get detailed info for each skill type."""
        skills_to_test = ["search", "page_create", "db_query"]

        for skill_name in skills_to_test:
            result = runner.invoke(app, ["skills", "show", skill_name, "--json"])
            data = json.loads(result.output)

            assert result.exit_code == 0
            assert data["success"] is True
            assert "name" in data["data"]
            assert "description" in data["data"]


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_invalid_page_id(self, notion_token):
        """Handle invalid page ID gracefully."""
        invalid_id = "not-a-valid-uuid"

        result = runner.invoke(app, ["get", invalid_id, "--json"])

        # Should fail gracefully
        assert result.exit_code == 0 or result.exit_code == 1
        if result.exit_code == 0:
            data = json.loads(result.output)
            assert data["success"] is False or "error" in str(data).lower()

    def test_empty_search(self, notion_token):
        """Handle empty search results."""
        # Search for something that doesn't exist
        result = runner.invoke(app, ["search", "xyz123notfound456", "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["success"] is True
        # Results can be empty, that's fine

    def test_missing_required_args(self, notion_token):
        """Handle missing required arguments."""
        result = runner.invoke(app, ["page", "create", "--json"])

        # Typer should handle this
        assert result.exit_code != 0 or "Error" in result.output


class TestCleanup:
    """Cleanup test resources."""

    def test_cleanup_created_resources(self, notion_token):
        """Archive all test resources."""
        resources_to_cleanup = [
            getattr(pytest, "created_task_id", None),
            getattr(pytest, "doc_page_id", None),
            getattr(pytest, "research_page_id", None),
        ]

        for resource_id in resources_to_cleanup:
            if resource_id:
                with contextlib.suppress(Exception):
                    runner.invoke(app, ["page", "archive", resource_id, "--json"])
