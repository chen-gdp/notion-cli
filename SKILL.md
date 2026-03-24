---
name: notion-cli
description: Command-line interface for Notion, designed for AI agents and power users. Search, create, update, and manage Notion pages and databases with JSON output for machine parsing.
version: 0.0.1
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["notion"],"env":["NOTION_TOKEN"]},"primaryEnv":"NOTION_TOKEN","homepage":"https://github.com/chen-gdp/notion-cli","install":{"pip":"pip install notion-cli","uv":"uv pip install notion-cli"}}}
---

# Notion CLI

Command-line interface for Notion, designed for AI agents and power users. Built on top of the `ultimate-notion` Python library.

## Authentication

**Required:** Set `NOTION_TOKEN` environment variable or run interactive setup.

```bash
# Option 1: Environment variable (recommended for agents)
export NOTION_TOKEN="secret_xxxxxxxxxxxxx"

# Option 2: Interactive setup
notion auth setup
```

## Quick Reference

| Command | Description | Use When |
|---------|-------------|----------|
| `notion auth status` | Check authentication | Verifying setup |
| `notion search <query>` | Find pages/databases | Discovery |
| `notion get <id>` | Get page/database details | Need full object |
| `notion db get <id>` | Get database schema | Understanding properties |
| `notion db query <id>` | Query database entries | Reading data |
| `notion db insert <id>` | Create database entry | Adding records |
| `notion page create` | Create new page | New content |
| `notion page append <id>` | Add markdown content | Updating pages |
| `notion page update <id>` | Update properties | Modifying entries |
| `notion page archive <id>` | Archive/unarchive | Cleanup |
| `notion skills list` | List all commands | Discovery |

## Usage Patterns

### Always Use `--json` for Machine Parsing

```bash
# Get structured output
notion search "meeting" --json

# Extract specific fields with jq
notion search "Tasks" --type database --json | jq -r '.data[0].id'
```

### Find and Query Workflow

```bash
# 1. Find the database
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')

# 2. Query with filters
notion db query "$DB_ID" --filter "Status=Open" --json
```

### Create and Populate Content

```bash
# 1. Create page
PAGE_ID=$(notion page create --parent "$DB_ID" --title "New Task" --json | jq -r '.data.id')

# 2. Add content
notion page append "$PAGE_ID" --content "## Description

- [ ] Step 1
- [ ] Step 2" --json
```

### Update and Archive

```bash
# Update properties
notion page update "$PAGE_ID" --properties "Status=Done" --json

# Archive when complete
notion page archive "$PAGE_ID" --json
```

## Error Handling

All commands return structured JSON:

```json
{
  "success": false,
  "error": {
    "code": "AUTH_ERROR",
    "message": "No token configured"
  }
}
```

Common error codes:
- `AUTH_ERROR` - Authentication failed or no token
- `NOT_FOUND` - Resource not found
- `VALIDATION_ERROR` - Invalid input parameters
- `RATE_LIMIT` - Too many requests

## Command Details

### Authentication Commands

```bash
# Check status
notion auth status --json

# Setup interactively
notion auth setup

# Remove authentication
notion auth logout
```

### Search and Discovery

```bash
# Search all content
notion search "project" --json

# Filter by type
notion search "tasks" --type database --json
notion search "notes" --type page --json

# Limit results
notion search "test" --limit 10 --json

# Get by ID
notion get <page_id> --json
notion get <database_id> --blocks --json
```

### Database Operations

```bash
# Get schema
notion db get <database_id> --json

# Query all entries
notion db query <database_id> --json

# Query with filters
notion db query <database_id> --filter "Status=Done" --json
notion db query <database_id> --filter "Status=Open,Priority=High" --json

# Insert new entry
notion db insert <database_id> --title "New Task" --properties "Status=Open" --json
```

### Page Operations

```bash
# Create page
notion page create --parent <parent_id> --title "New Page" --json

# Create in database with properties
notion page create --parent <database_id> --title "New Entry" --properties "Status=Open" --json

# Append markdown content
notion page append <page_id> --content "## Heading\n\nContent" --json

# Update properties
notion page update <page_id> --title "Updated Title" --json
notion page update <page_id> --properties "Status=Done" --json

# Archive/unarchive
notion page archive <page_id> --json
notion page archive <page_id> --unarchive --json
```

### Skills Discovery

```bash
# List all commands
notion skills list --json

# Show command details
notion skills show search --json
notion skills show db_query --json
```

## Markdown Support

The `page append` command supports:
- Headings: `#`, `##`, `###`
- Bullet lists: `- item`
- Numbered lists: `1. item`
- Todo lists: `- [ ] task`, `- [x] done`
- Code blocks: ` ```language\ncode\n``` `
- Paragraphs: Plain text

Example:
```bash
notion page append <page_id> --content "## Meeting Notes

### Attendees
- Alice
- Bob

### Action Items
- [ ] Review Q1 roadmap
- [ ] Schedule follow-up" --json
```

## Best Practices

1. **Always use `--json`** for programmatic access
2. **Check `success` field** before processing data
3. **Handle errors gracefully** - report meaningful messages to users
4. **Use environment variables** for authentication in automated workflows
5. **Verify IDs** with `get` command before destructive operations
6. **Use filters** to narrow database queries
7. **Quote content** properly when using special characters

## Documentation

- **COMMANDS.md** - Complete command reference
- **EXAMPLES.md** - Common usage patterns
- **WORKFLOWS.md** - Task-oriented guides
- **MARKDOWN.md** - Supported markdown syntax
- **OUTPUT.md** - JSON output schemas

## Links

- Repository: https://github.com/chen-gdp/notion-cli
- Issues: https://github.com/chen-gdp/notion-cli/issues
- PyPI: https://pypi.org/project/notion-cli/
