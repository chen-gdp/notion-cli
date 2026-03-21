"""Tests for the session module with mocked ultimate_notion."""

import os
from unittest.mock import MagicMock, patch

import pytest

from notion_cli.core.config import Config
from notion_cli.core.errors import AuthError
from notion_cli.core.session import NotionSession, check_auth, get_session


class TestNotionSession:
    """Tests for NotionSession class."""

    @pytest.fixture(autouse=True)
    def reset_session(self):
        """Reset session singleton before each test."""
        NotionSession.close()
        yield
        NotionSession.close()

    def test_get_session_without_token_raises_auth_error(self):
        """
        Condition: No token in env var or config.
        Expected: Raises AuthError with helpful message.
        """
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Config, "get_token", return_value=None):
                with pytest.raises(AuthError) as exc_info:
                    NotionSession.get()

                assert "notion auth setup" in str(exc_info.value).lower()

    def test_get_session_creates_session_with_token(self, mock_notion_session):
        """
        Condition: Token is available.
        Expected: Creates and returns Session instance.
        """
        mock_session_class, mock_session = mock_notion_session

        with patch.dict(os.environ, {"NOTION_TOKEN": "secret_token"}):
            session = NotionSession.get()

            assert session == mock_session
            mock_session_class.assert_called_once_with(token="secret_token")

    def test_get_session_returns_same_instance(self, mock_notion_session):
        """
        Condition: Session already created.
        Expected: Returns cached instance.
        """
        mock_session_class, mock_session = mock_notion_session

        with patch.dict(os.environ, {"NOTION_TOKEN": "secret_token"}):
            session1 = NotionSession.get()
            session2 = NotionSession.get()

            assert session1 is session2
            mock_session_class.assert_called_once()

    def test_close_clears_session(self, mock_notion_session):
        """
        Condition: Session exists.
        Expected: Closes and clears session.
        """
        mock_session_class, mock_session = mock_notion_session

        with patch.dict(os.environ, {"NOTION_TOKEN": "secret_token"}):
            NotionSession.get()
            NotionSession.close()

            mock_session.close.assert_called_once()

    def test_is_authenticated_with_token(self):
        """
        Condition: Token exists.
        Expected: Returns True.
        """
        with patch.dict(os.environ, {"NOTION_TOKEN": "secret_token"}):
            assert NotionSession.is_authenticated() is True

    def test_is_authenticated_without_token(self):
        """
        Condition: No token available.
        Expected: Returns False.
        """
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Config, "get_token", return_value=None):
                assert NotionSession.is_authenticated() is False


class TestGetSession:
    """Tests for get_session function."""

    def test_get_session_returns_session_instance(self, mock_notion_session):
        """
        Condition: Session can be created.
        Expected: Returns Session instance.
        """
        mock_session_class, mock_session = mock_notion_session

        with patch.dict(os.environ, {"NOTION_TOKEN": "secret_token"}):
            session = get_session()

            assert session == mock_session


class TestCheckAuth:
    """Tests for check_auth function."""

    def test_check_auth_with_token(self):
        """
        Condition: Token exists.
        Expected: Returns True.
        """
        with patch.dict(os.environ, {"NOTION_TOKEN": "secret_token"}):
            assert check_auth() is True

    def test_check_auth_without_token(self):
        """
        Condition: No token.
        Expected: Returns False.
        """
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(Config, "get_token", return_value=None):
                assert check_auth() is False
