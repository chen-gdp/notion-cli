"""Tests for the output module."""

import json

import pytest

from notion_cli.core.output import output_error, output_json, output_table


class TestOutputJson:
    """Tests for output_json function."""

    def test_output_json_success(self, capsys):
        """
        Condition: Called with success=True and data.
        Expected: Prints JSON with success=True, data, and null error.
        """
        test_data = {"id": "123", "name": "test"}

        with pytest.raises(SystemExit) as exc_info:
            output_json(test_data, success=True)

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["success"] is True
        assert result["data"] == test_data
        assert result["error"] is None

    def test_output_json_error(self, capsys):
        """
        Condition: Called with success=False and error data.
        Expected: Prints JSON with success=False, null data, and error.
        """
        error_data = {"code": "NOT_FOUND", "message": "Page not found"}

        with pytest.raises(SystemExit) as exc_info:
            output_json(error_data, success=False)

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["success"] is False
        assert result["data"] is None
        assert result["error"] == error_data

    def test_output_json_with_complex_data(self, capsys):
        """
        Condition: Called with nested data structures.
        Expected: Properly serializes to JSON.
        """
        test_data = {"results": [{"id": "1"}, {"id": "2"}], "total": 2, "nested": {"key": "value"}}

        with pytest.raises(SystemExit):
            output_json(test_data, success=True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["data"]["total"] == 2
        assert len(result["data"]["results"]) == 2


class TestOutputTable:
    """Tests for output_table function."""

    def test_output_table_with_data(self, capsys):
        """
        Condition: Called with list of dicts and column names.
        Expected: Prints formatted table with headers and rows.
        """
        data = [{"title": "Page 1", "type": "page", "id": "123"}, {"title": "Page 2", "type": "database", "id": "456"}]
        columns = ["title", "type", "id"]

        output_table(data, columns)

        captured = capsys.readouterr()
        assert "Page 1" in captured.out
        assert "Page 2" in captured.out
        assert "page" in captured.out
        assert "database" in captured.out
        assert "title" in captured.out
        assert "type" in captured.out

    def test_output_table_empty_data(self, capsys):
        """
        Condition: Called with empty list.
        Expected: Prints "No results found." message.
        """
        output_table([], ["title", "id"])

        captured = capsys.readouterr()
        assert "No results found" in captured.out

    def test_output_table_missing_columns(self, capsys):
        """
        Condition: Data dicts missing some columns.
        Expected: Shows empty string for missing values.
        """
        data = [
            {"title": "Page 1", "id": "123"},
            {"title": "Page 2"},  # Missing id
        ]
        columns = ["title", "id"]

        output_table(data, columns)

        captured = capsys.readouterr()
        assert "Page 1" in captured.out
        assert "Page 2" in captured.out


class TestOutputError:
    """Tests for output_error function."""

    def test_output_error_basic(self, capsys):
        """
        Condition: Called with code and message.
        Expected: Prints JSON error and exits with code 1.
        """
        with pytest.raises(SystemExit) as exc_info:
            output_error("AUTH_ERROR", "Authentication failed")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["success"] is False
        assert result["error"]["code"] == "AUTH_ERROR"
        assert result["error"]["message"] == "Authentication failed"
        assert "details" not in result["error"]

    def test_output_error_with_details(self, capsys):
        """
        Condition: Called with code, message, and details.
        Expected: Includes details in error JSON.
        """
        details = {"field": "token", "reason": "expired"}

        with pytest.raises(SystemExit):
            output_error("VALIDATION_ERROR", "Invalid input", details)

        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result["error"]["code"] == "VALIDATION_ERROR"
        assert result["error"]["details"] == details
