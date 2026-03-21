# Notion CLI Skills

Command-line interface for Notion, designed for AI agents and power users.

## Quick Reference

| Command | Description | Use When |
|---------|-------------|----------|
| `notion auth setup` | Configure authentication | First time setup |
| `notion auth status` | Check authentication | Troubleshooting |
| `notion search <query>` | Find pages/databases | Looking for content |
| `notion get <id>` | Get page/database details | Need full object |
| `notion db get <id>` | Get database schema | Need property types |
| `notion db query <id>` | Query database entries | Reading data |
| `notion db insert <id>` | Create database entry | Adding records |
| `notion page create` | Create new page | New content |
| `notion page append <id>` | Add markdown content | Updating pages |
| `notion page update <id>` | Update properties | Modifying entries |
| `notion page archive <id>` | Archive/unarchive | Cleanup |
| `notion skills list` | List all commands | Discovery |
| `notion skills show <name>` | Command details | Need help |

## Documentation

- **[COMMANDS.md](docs/COMMANDS.md)** - Complete command reference with all arguments and options
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Common usage patterns and one-liners
- **[WORKFLOWS.md](docs/WORKFLOWS.md)** - Task-oriented guides (task management, documentation, research)
- **[MARKDOWN.md](docs/MARKDOWN.md)** - Supported markdown syntax for `page append`
- **[OUTPUT.md](docs/OUTPUT.md)** - JSON output schemas and error codes

## Authentication

**Environment Variable (Recommended):**
```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxx"
```

**Config File:**
```bash
notion auth setup  # Interactive prompt
```

Configuration stored in `~/.config/notion-cli/config.json`.

## Key Features

- **AI-Agent Friendly**: All commands support `--json` for machine parsing
- **Complete CRUD**: Create, read, update, archive pages and databases
- **Rich Content**: Markdown support for headings, lists, code blocks, todos
- **Flexible Auth**: Environment variable or config file

## Common Patterns

### Find and Query
```bash
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')
notion db query "$DB_ID" --filter "Status=Open"
```

### Create with Content
```bash
PAGE_ID=$(notion page create --parent "$DB_ID" --title "New Task" --json | jq -r '.data.id')
notion page append "$PAGE_ID" --content "## Description

- [ ] Step 1
- [ ] Step 2"
```

### Update and Archive
```bash
notion page update "$PAGE_ID" --properties "Status=Done"
notion page archive "$PAGE_ID"
```

## Error Handling

All commands return structured JSON with `--json`:

```json
{
  "success": false,
  "error": {
    "code": "AUTH_ERROR",
    "message": "No token configured"
  }
}
```

Common codes: `AUTH_ERROR`, `NOT_FOUND`, `VALIDATION_ERROR`, `RATE_LIMIT`

---

*For detailed documentation, see the `docs/` directory.*
