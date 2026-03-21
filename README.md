# Notion CLI

A command-line interface for Notion, designed for AI agents and power users. Built on top of the `ultimate-notion` Python library.

**Author:** Christian Chen (christianchen01@gmail.com)

## Features

- **AI-Agent Friendly**: All commands support `--json` output for machine parsing
- **Complete CRUD Operations**: Create, read, update, archive pages and databases
- **Rich Content Support**: Markdown parsing with support for headings, lists, code blocks, and todos
- **Self-Documenting**: Auto-generated SKILLS.md for easy agent discovery
- **Authentication**: Flexible token management via environment variables or config files

## Installation

```bash
pip install git+https://github.com/chen-gdp/notion-cli.git
```

Or install with uv (recommended for development):

```bash
uv pip install git+https://github.com/chen-gdp/notion-cli.git
```

## Quick Start

### 1. Authenticate

Set your Notion token as an environment variable:

```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxx"
```

Or configure via the CLI:

```bash
notion auth setup
# Enter your Notion integration token when prompted
```

### 2. Verify Authentication

```bash
notion auth status
```

### 3. Start Using

```bash
# Search for pages and databases
notion search "meeting"

# Get page details
notion get <page_id>

# Query database
notion db query <database_id>
```

## Development Setup with UV

This project uses [uv](https://docs.astral.sh/uv/) for fast Python package management.

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/chen-gdp/notion-cli.git
cd notion-cli

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Or use uv sync (if using uv's lock file)
uv sync --dev
```

### Running Tests

```bash
# Run all tests with uv
uv run pytest tests/unit/ -v

# Run with coverage
uv run pytest tests/unit/ --cov

# Run integration tests (requires NOTION_TOKEN)
NOTION_TOKEN=xxx uv run pytest tests/integration/ -v
```

### Code Quality

```bash
# Format code
uv run ruff format .

# Run linter
uv run ruff check .

# Type checking
uv run mypy src/notion_cli
```

## Commands

### Authentication

```bash
# Check authentication status
notion auth status

# Interactive setup
notion auth setup

# Remove saved token
notion auth logout
```

### Search & Discovery

```bash
# Search all content
notion search "project"

# Filter by type
notion search "tasks" --type database
notion search "notes" --type page

# Limit results
notion search "test" --limit 10

# Get by ID
notion get <page_id>
notion get <database_id>
```

### Database Operations

```bash
# Get database schema
notion db get <database_id>

# Query entries
notion db query <database_id>

# Query with filter
notion db query <database_id> --filter "Status=Done"

# Query with limit
notion db query <database_id> --limit 50

# Insert new entry
notion db insert <database_id> --title "New Task" --properties "Status=Open,Priority=High"
```

### Page Operations

```bash
# Create a page
notion page create --parent <parent_id> --title "New Page"

# Create in database
notion page create --parent <database_id> --title "New Entry" --properties "Status=Open"

# Append content (supports markdown)
notion page append <page_id> --content "## Heading\n\n- Item 1\n- Item 2"

# Update page
notion page update <page_id> --title "Updated Title"
notion page update <page_id> --properties "Status=Done"

# Archive page
notion page archive <page_id>

# Unarchive page
notion page archive <page_id> --unarchive
```

### Skills Discovery

```bash
# List all available commands
notion skills list

# Show detailed help for a command
notion skills show search
notion skills show page_create
```

## Markdown Support

The `page append` command supports rich markdown:

```bash
notion page append <page_id> --content "## Meeting Notes

### Attendees
- Alice
- Bob
- Carol

### Action Items
- [ ] Review Q1 roadmap
- [ ] Schedule follow-up
- [x] Send meeting recap

### Code Example

\`\`\`python
def hello():
    return 'world'
\`\`\`

For questions, contact the team."
```

**Supported Markdown:**
- Headings: `#`, `##`, `###`
- Bullet lists: `- item`
- Todo lists: `- [ ] task`, `- [x] done`
- Code blocks: ` ```language\ncode\n``` `
- Paragraphs: Plain text

## JSON Output

All commands support `--json` for programmatic use:

```bash
# Get structured data
notion search "project" --json

# Output format:
{
  "success": true,
  "data": [
    {
      "id": "abc123...",
      "title": "Project Alpha",
      "type": "page",
      "url": "https://notion.so/...",
      "last_edited_time": "2024-03-20T14:30:00Z"
    }
  ],
  "error": null
}

# Errors are also structured:
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "Page not found",
    "details": {"id": "invalid-id"}
  }
}
```

## Configuration

The CLI stores configuration in `~/.config/notion-cli/config.json`:

```json
{
  "token": "secret_xxxxxxxxxxxxx"
}
```

**Priority order for token:**
1. `NOTION_TOKEN` environment variable
2. `~/.config/notion-cli/config.json`

## Use Cases

### Task Management

```bash
# Find tasks database
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')

# Create new task
notion db insert "$DB_ID" --title "Fix bug #123" --properties "Status=Open,Priority=High"

# Query open tasks
notion db query "$DB_ID" --filter "Status=Open"

# Mark as done
TASK_ID=$(notion db query "$DB_ID" --filter "Title=Fix bug #123" --json | jq -r '.data[0].id')
notion page update "$TASK_ID" --properties "Status=Done"
```

### Documentation

```bash
# Create documentation page
PAGE_ID=$(notion page create --parent <wiki_id> --title "API Guide" --json | jq -r '.data.id')

# Add structured content
notion page append "$PAGE_ID" --content "## Overview

API endpoints:

- GET /users
- POST /users
- DELETE /users/:id

\`\`\`bash
curl https://api.example.com/users
\`\`\`"
```

### Research Notes

```bash
# Search existing research
notion search "competitor analysis" --json

# Create new research page
PAGE_ID=$(notion page create --parent <research_db> --title "Q2 Competitor Analysis" --json | jq -r '.data.id')

# Add findings incrementally
notion page append "$PAGE_ID" --content "## Competitor A
- Strengths: Fast, reliable
- Weaknesses: Expensive"

notion page append "$PAGE_ID" --content "## Competitor B
- Strengths: Free tier
- Weaknesses: Limited features"
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NOTION_TOKEN` | Notion integration token | Yes (or via `notion auth setup`) |

## Troubleshooting

### Authentication Issues

```bash
# Check if token is set
notion auth status

# Verify token is valid
notion search "test" --json
```

### Rate Limiting

If you hit rate limits, the CLI will return:
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT",
    "message": "Too many requests. Retry after 60s."
  }
}
```

### Common Errors

| Error Code | Cause | Solution |
|------------|-------|----------|
| `AUTH_ERROR` | No token configured | Set NOTION_TOKEN or run `notion auth setup` |
| `NOT_FOUND` | Page/DB doesn't exist | Check the ID is correct |
| `VALIDATION_ERROR` | Invalid input | Check required parameters |

## Development

### Running Tests

```bash
# Unit tests with uv
uv run pytest tests/unit/ -v

# Integration tests (requires NOTION_TOKEN)
NOTION_TOKEN=xxx uv run pytest tests/integration/ -v
```

### Project Structure

```
notion-cli/
├── src/notion_cli/
│   ├── cli.py              # Main entry point
│   ├── commands/           # Command implementations
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── get.py
│   │   ├── page.py
│   │   ├── search.py
│   │   └── skills.py
│   └── core/               # Core utilities
│       ├── config.py
│       ├── errors.py
│       ├── markdown.py
│       ├── output.py
│       ├── session.py
│       └── skills_registry.py
├── tests/
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── pyproject.toml         # UV/pip configuration
└── README.md
```

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for your changes
4. Submit a pull request

## Support

- Open an issue on GitHub
- Check the [Notion API documentation](https://developers.notion.com/)
- Review [ultimate-notion docs](https://ultimate-notion.com/)

---

**Author:** Christian Chen (christianchen01@gmail.com)  
**License:** MIT  
**Built with:** [uv](https://docs.astral.sh/uv/) + [ultimate-notion](https://ultimate-notion.com/)
