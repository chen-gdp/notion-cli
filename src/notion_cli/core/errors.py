"""Custom exceptions for notion-cli.

Provides a hierarchy of exceptions for different error scenarios,
with consistent error codes and structured error data.
"""

from typing import Any


class NotionCLIError(Exception):
    """Base exception for all CLI errors.

    Attributes:
        code: Error code string for programmatic handling.
        message: Human-readable error message.
        details: Optional additional error context.
    """

    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize error with code, message, and optional details.

        Args:
            code: Error code for programmatic handling.
            message: Human-readable error message.
            details: Optional additional error context.
        """
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for JSON output.

        Returns:
            Dictionary with code, message, and optional details.
        """
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.details:
            result["details"] = self.details
        return result


class AuthError(NotionCLIError):
    """Authentication or authorization error."""

    def __init__(self, message: str) -> None:
        """Initialize auth error with message.

        Args:
            message: Description of the authentication failure.
        """
        super().__init__("AUTH_ERROR", message)


class NotFoundError(NotionCLIError):
    """Resource not found error."""

    def __init__(self, resource_type: str, resource_id: str) -> None:
        """Initialize not found error with resource info.

        Args:
            resource_type: Type of resource (page, database, etc.).
            resource_id: ID of the missing resource.
        """
        message = f"{resource_type} '{resource_id}' not found"
        super().__init__("NOT_FOUND", message, {"type": resource_type, "id": resource_id})


class ValidationError(NotionCLIError):
    """Input validation error."""

    def __init__(self, field: str, message: str) -> None:
        """Initialize validation error with field info.

        Args:
            field: Name of the field that failed validation.
            message: Description of the validation failure.
        """
        super().__init__("VALIDATION_ERROR", message, {"field": field})
