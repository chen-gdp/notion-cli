"""Tests for the errors module."""

import pytest

from notion_cli.core.errors import (
    AuthError,
    NotFoundError,
    NotionCLIError,
    ValidationError,
)


class TestNotionCLIError:
    """Tests for base NotionCLIError class."""

    def test_error_initialization(self):
        """
        Condition: Creating error with code and message.
        Expected: Error stores code, message, and details.
        """
        error = NotionCLIError("TEST_CODE", "Test message", {"key": "value"})

        assert error.code == "TEST_CODE"
        assert error.message == "Test message"
        assert error.details == {"key": "value"}
        assert str(error) == "Test message"

    def test_error_without_details(self):
        """
        Condition: Creating error without details.
        Expected: Details defaults to empty dict.
        """
        error = NotionCLIError("TEST_CODE", "Test message")

        assert error.details == {}

    def test_error_to_dict(self):
        """
        Condition: Converting error to dictionary.
        Expected: Returns dict with code, message, details.
        """
        error = NotionCLIError("TEST_CODE", "Test message", {"key": "value"})

        result = error.to_dict()

        assert result == {"code": "TEST_CODE", "message": "Test message", "details": {"key": "value"}}

    def test_error_to_dict_without_details(self):
        """
        Condition: Converting error without details to dict.
        Expected: Details not included in output.
        """
        error = NotionCLIError("TEST_CODE", "Test message")

        result = error.to_dict()

        assert result == {"code": "TEST_CODE", "message": "Test message"}


class TestAuthError:
    """Tests for AuthError class."""

    def test_auth_error_default_code(self):
        """
        Condition: Creating AuthError with just message.
        Expected: Code defaults to AUTH_ERROR.
        """
        error = AuthError("Authentication failed")

        assert error.code == "AUTH_ERROR"
        assert error.message == "Authentication failed"

    def test_auth_error_inheritance(self):
        """
        Condition: Checking AuthError inheritance.
        Expected: Is instance of NotionCLIError.
        """
        error = AuthError("Auth failed")

        assert isinstance(error, NotionCLIError)


class TestNotFoundError:
    """Tests for NotFoundError class."""

    def test_not_found_error_with_resource_info(self):
        """
        Condition: Creating NotFoundError with type and ID.
        Expected: Code is NOT_FOUND, includes resource details.
        """
        error = NotFoundError("page", "abc123")

        assert error.code == "NOT_FOUND"
        assert "page" in error.message
        assert "abc123" in error.message
        assert error.details == {"type": "page", "id": "abc123"}

    def test_not_found_error_inheritance(self):
        """
        Condition: Checking NotFoundError inheritance.
        Expected: Is instance of NotionCLIError.
        """
        error = NotFoundError("database", "xyz789")

        assert isinstance(error, NotionCLIError)


class TestValidationError:
    """Tests for ValidationError class."""

    def test_validation_error_with_field(self):
        """
        Condition: Creating ValidationError with field and message.
        Expected: Code is VALIDATION_ERROR, includes field in details.
        """
        error = ValidationError("title", "Title is required")

        assert error.code == "VALIDATION_ERROR"
        assert error.message == "Title is required"
        assert error.details == {"field": "title"}

    def test_validation_error_inheritance(self):
        """
        Condition: Checking ValidationError inheritance.
        Expected: Is instance of NotionCLIError.
        """
        error = ValidationError("id", "Invalid ID format")

        assert isinstance(error, NotionCLIError)
