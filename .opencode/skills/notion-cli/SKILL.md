---
name: notion-cli
description: Command-line interface for Notion - search, create, update, and manage Notion pages and databases with JSON output for machine parsing. Use when working with Notion workspaces, creating documentation, managing tasks, or querying databases.
---

# Notion CLI

Interact with your Notion workspace from the terminal. Designed for AI agents and power users.

## Prerequisites

- `notion` CLI installed: `pip install notion-cli`
- Token configured via one of:
  - `NOTION_TOKEN` environment variable
  - `.env` file with `NOTION_TOKEN="..."`
  - `notion auth setup`

## Quick Start

```bash
# Check authentication
notion auth status

# Search for content
notion search "meeting notes" --json

# Query a database
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')
notion db query "$DB_ID" --filter "Status=Open" --json

# Create a page
notion page create --parent "$DB_ID" --title "New Task" --json
```

## Commands

### Authentication
- `notion auth status` - Check if authenticated
- `notion auth setup` - Interactive setup
- `notion auth logout` - Remove token

### Search & Discovery
- `notion ls` - List all pages and databases
- `notion ls --type page` - List only pages
- `notion ls --type database` - List only databases
- `notion search <query>` - Find pages and databases
- `notion search <query> --type database` - Search only databases
- `notion search <query> --type page` - Search only pages
- `notion get <id>` - Get full page/database details

### Database Operations
- `notion db get <id>` - Get database schema
- `notion db query <id>` - Query all entries
- `notion db query <id> --filter "Status=Open"` - Filtered query
- `notion db insert <id> --title "..." --properties "..."` - Create entry

### Page Operations
- `notion page create --parent <id> --title "..."` - Create page
- `notion page append <id> --content "..."` - Add markdown content
- `notion page update <id> --title "..."` - Update title
- `notion page update <id> --properties "..."` - Update properties
- `notion page archive <id>` - Archive page

### Skills Discovery
- `notion skills list` - List all commands
- `notion skills show <name>` - Show command details

## Usage Patterns

### Always Use `--json` for Parsing
```bash
# Get structured output
notion search "project" --json | jq '.data[0].id'

# Extract IDs
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')
```

### Chain Commands
```bash
# Find database, then query it
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id') && \
notion db query "$DB_ID" --filter "Status=Open" --json

# Create page and add content
PAGE_ID=$(notion page create --parent "$DB_ID" --title "New Task" --json | jq -r '.data.id') && \
notion page append "$PAGE_ID" --content "## Description\n\n- [ ] Step 1"
```

### Filter Syntax
```bash
# Single filter
notion db query "$DB_ID" --filter "Status=Done"

# Multiple filters
notion db query "$DB_ID" --filter "Status=Open,Priority=High"

# Date filters
notion db query "$DB_ID" --filter "Due Date=2024-03-25"
```

## Markdown Support for Page Append

The `--content` flag supports:
- Headings: `#`, `##`, `###`
- Bullet lists: `- item`
- Numbered lists: `1. item`
- Todo lists: `- [ ] task`, `- [x] done`
- Code blocks: ` ```language\ncode\n``` `

Example:
```bash
notion page append "$PAGE_ID" --content "## Meeting Notes

### Attendees
- Alice
- Bob

### Action Items
- [ ] Review Q1 roadmap
- [ ] Schedule follow-up"
```

## Error Handling

All commands return JSON with `--json`:

```json
{
  "success": false,
  "error": {
    "code": "AUTH_ERROR",
    "message": "No token configured"
  }
}
```

Common codes:
- `AUTH_ERROR` - Not authenticated
- `NOT_FOUND` - Resource not found
- `VALIDATION_ERROR` - Invalid parameters
- `RATE_LIMIT` - Too many requests

## Best Practices

1. **Use `--json`** for all programmatic calls
2. **Check `success` field** before processing
3. **Use environment variables** for auth in automation
4. **Verify IDs** before destructive operations
5. **Quote content** with special characters
6. **Use filters** to narrow queries

## Full Documentation

- COMMANDS.md - Complete command reference
- EXAMPLES.md - Usage patterns
- WORKFLOWS.md - Task guides
- MARKDOWN.md - Syntax reference
- OUTPUT.md - JSON schemas

## Links

- Repository: https://github.com/chen-gdp/notion-cli
- PyPI: https://pypi.org/project/notion-cli/
