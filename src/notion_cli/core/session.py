"""Session management for notion-cli.

Provides a singleton wrapper around the ultimate_notion Session
with authentication handling and error management.
"""

from ultimate_notion import Session
from ultimate_notion.config import get_or_create_cfg

from notion_cli.core.config import get_config
from notion_cli.core.errors import AuthError


class NotionSession:
    """Singleton wrapper for Notion API session.

    Manages a single Session instance with lazy initialization
    and automatic authentication handling.
    """

    _instance: Session | None = None

    @classmethod
    def get(cls) -> Session:
        """Get or create the Notion session.

        Returns:
            The Notion Session instance.

        Raises:
            AuthError: If no token is configured.
        """
        if cls._instance is None:
            # Check our own config first
            config = get_config()
            token = config.get_token()
            if not token:
                raise AuthError(
                    "No Notion token found. Run 'notion auth setup' or set NOTION_TOKEN environment variable."
                )

            # Create ultimate_notion config and set the token
            cfg = get_or_create_cfg()
            cfg.ultimate_notion.token = token
            cls._instance = Session(cfg)
        return cls._instance

    @classmethod
    def close(cls) -> None:
        """Close and clear the session."""
        if cls._instance:
            cls._instance.close()
            cls._instance = None

    @classmethod
    def is_authenticated(cls) -> bool:
        """Check if a token is available.

        Returns:
            True if token exists, False otherwise.
        """
        config = get_config()
        return bool(config.get_token())


def get_session() -> Session:
    """Get the Notion session.

    Returns:
        The Notion Session instance.
    """
    return NotionSession.get()


def check_auth() -> bool:
    """Check if authenticated without creating session.

    Returns:
        True if authenticated, False otherwise.
    """
    return NotionSession.is_authenticated()
