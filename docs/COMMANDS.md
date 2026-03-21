# Command Reference

Complete reference for all Notion CLI commands.

## Table of Contents

- [Authentication](#authentication)
- [Search & Discovery](#search--discovery)
- [Database Operations](#database-operations)
- [Page Operations](#page-operations)
- [Utility](#utility)

---

## Authentication

### auth status

Check authentication status and configuration.

**Usage:**

```bash
notion auth status [options]
```

**Options:**

- `--json`: Output as JSON

**Examples:**

```bash
notion auth status
notion auth status --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "authenticated": true,
    "source": "env|config",
    "config_path": "~/.config/notion-cli/config.json"
  }
}
```

---

### auth setup

Interactive setup for Notion authentication.

**Usage:**

```bash
notion auth setup
```

**Examples:**

```bash
notion auth setup
# Prompts for token and saves to config
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "message": "Authentication configured",
    "config_path": "~/.config/notion-cli/config.json"
  }
}
```

---

### auth logout

Remove saved authentication token.

**Usage:**

```bash
notion auth logout
```

**Examples:**

```bash
notion auth logout
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "message": "Authentication removed"
  }
}
```

---

## Search & Discovery

### search

Search for pages and databases in Notion.

**Usage:**

```bash
notion search <query> [options]
```

**Arguments:**

- `query` (required): Search query string

**Options:**

- `--type`: Filter by type (`page` or `database`)
- `--limit`: Maximum results (default: 100)
- `--json`: Output as JSON

**Examples:**

```bash
notion search "meeting"
notion search "tasks" --type database
notion search "notes" --type page --limit 10
notion search "project" --json
```

**Returns:**

```json
{
  "success": true,
  "data": [
    {
      "id": "abc123...",
      "title": "Meeting Notes",
      "type": "page",
      "url": "https://notion.so/...",
      "last_edited_time": "2024-03-20T14:30:00Z"
    }
  ]
}
```

---

### get

Get a page or database by ID.

**Usage:**

```bash
notion get <id> [options]
```

**Arguments:**

- `id` (required): Page or database ID

**Options:**

- `--blocks`: Include block content for pages
- `--json`: Output as JSON

**Examples:**

```bash
notion get abc123-def456
notion get abc123-def456 --blocks
notion get abc123-def456 --json
```

**Returns:**

Page object:
```json
{
  "success": true,
  "data": {
    "id": "abc123...",
    "title": "Page Title",
    "type": "page",
    "url": "https://notion.so/...",
    "properties": {...},
    "blocks": [...]  // if --blocks
  }
}
```

Database object:
```json
{
  "success": true,
  "data": {
    "id": "abc123...",
    "title": "Database Name",
    "type": "database",
    "url": "https://notion.so/...",
    "properties": {...}  // schema
  }
}
```

---

## Database Operations

### db get

Get database schema and properties.

**Usage:**

```bash
notion db get <database_id> [options]
```

**Arguments:**

- `database_id` (required): Database ID

**Options:**

- `--json`: Output as JSON

**Examples:**

```bash
notion db get abc123-def456
notion db get abc123-def456 --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "id": "abc123...",
    "title": "Tasks",
    "properties": {
      "Name": {"type": "title"},
      "Status": {"type": "select", "options": [...]},
      "Priority": {"type": "select"},
      "Due Date": {"type": "date"}
    }
  }
}
```

---

### db query

Query database entries with optional filters.

**Usage:**

```bash
notion db query <database_id> [options]
```

**Arguments:**

- `database_id` (required): Database ID

**Options:**

- `--filter`: Filter criteria (`key=value,key2=value2`)
- `--limit`: Maximum results (default: 100)
- `--json`: Output as JSON

**Filter Syntax:**

- Simple equality: `Status=Done`
- Multiple filters: `Status=Open,Priority=High`
- Supports: `title`, `select`, `multi_select`, `status`, `checkbox`, `number`, `date`

**Examples:**

```bash
notion db query abc123-def456
notion db query abc123-def456 --filter "Status=Done"
notion db query abc123-def456 --filter "Status=Open,Priority=High"
notion db query abc123-def456 --limit 50 --json
```

**Returns:**

```json
{
  "success": true,
  "data": [
    {
      "id": "entry123...",
      "title": "Task Name",
      "url": "https://notion.so/...",
      "properties": {
        "Status": {"type": "select", "value": "Done"},
        "Priority": {"type": "select", "value": "High"}
      }
    }
  ]
}
```

---

### db insert

Insert a new entry into a database.

**Usage:**

```bash
notion db insert <database_id> [options]
```

**Arguments:**

- `database_id` (required): Database ID

**Options:**

- `--title` (required): Entry title
- `--properties`: Properties (`key=value,key2=value2`)
- `--json`: Output as JSON

**Property Types:**

- `select`: Use option name
- `multi_select`: Comma-separated values
- `status`: Use status name
- `checkbox`: `true` or `false`
- `number`: Numeric value
- `date`: ISO 8601 date (`2024-03-20` or `2024-03-20T14:30:00`)
- `url`: URL string
- `email`: Email address
- `phone`: Phone number

**Examples:**

```bash
notion db insert abc123-def456 --title "New Task"
notion db insert abc123-def456 --title "New Task" --properties "Status=Open,Priority=High"
notion db insert abc123-def456 --title "New Task" --properties "Due Date=2024-03-20,Done=false"
notion db insert abc123-def456 --title "New Task" --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "id": "entry123...",
    "title": "New Task",
    "url": "https://notion.so/..."
  }
}
```

---

## Page Operations

### page create

Create a new page in Notion.

**Usage:**

```bash
notion page create [options]
```

**Options:**

- `--parent` (required): Parent page or database ID
- `--title` (required): Page title
- `--properties`: Properties for database entries
- `--json`: Output as JSON

**Examples:**

```bash
# Create in a page
notion page create --parent abc123-def456 --title "New Page"

# Create in a database
notion page create --parent db123-def456 --title "New Entry" --properties "Status=Open,Priority=High"

# Get ID for chaining
notion page create --parent abc123-def456 --title "New Page" --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "id": "page123...",
    "title": "New Page",
    "url": "https://notion.so/..."
  }
}
```

---

### page append

Append blocks to a page with markdown content.

**Usage:**

```bash
notion page append <page_id> [options]
```

**Arguments:**

- `page_id` (required): Page ID

**Options:**

- `--content` (required): Content to append (markdown)
- `--json`: Output as JSON

**Markdown Support:**

- Headings: `#`, `##`, `###`
- Bullet lists: `- item`
- Numbered lists: `1. item`
- Todo lists: `- [ ] task`, `- [x] done`
- Code blocks: ` ```language\ncode\n``` `
- Paragraphs: Plain text

See [MARKDOWN.md](MARKDOWN.md) for full syntax.

**Examples:**

```bash
notion page append abc123-def456 --content "## Heading\n\nParagraph text"
notion page append abc123-def456 --content "- Item 1\n- Item 2"
notion page append abc123-def456 --content "## Meeting Notes\n\n- [ ] Action item" --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "page_id": "abc123...",
    "blocks_added": 5
  }
}
```

---

### page update

Update page properties.

**Usage:**

```bash
notion page update <page_id> [options]
```

**Arguments:**

- `page_id` (required): Page ID

**Options:**

- `--title`: New title
- `--properties`: Properties to update
- `--json`: Output as JSON

**Examples:**

```bash
notion page update abc123-def456 --title "Updated Title"
notion page update abc123-def456 --properties "Status=Done"
notion page update abc123-def456 --title "New Title" --properties "Status=Done" --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "id": "abc123...",
    "updated_fields": ["title", "Status"]
  }
}
```

---

### page archive

Archive or unarchive a page.

**Usage:**

```bash
notion page archive <page_id> [options]
```

**Arguments:**

- `page_id` (required): Page ID

**Options:**

- `--unarchive`: Unarchive instead of archive
- `--json`: Output as JSON

**Examples:**

```bash
notion page archive abc123-def456
notion page archive abc123-def456 --unarchive
notion page archive abc123-def456 --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "id": "abc123...",
    "action": "archive",
    "archived": true
  }
}
```

---

## Utility

### skills list

List all available CLI skills/commands.

**Usage:**

```bash
notion skills list [options]
```

**Options:**

- `--json`: Output as JSON

**Examples:**

```bash
notion skills list
notion skills list --json
```

**Returns:**

```json
{
  "success": true,
  "data": [
    {
      "name": "search",
      "description": "Search for pages and databases",
      "category": "discovery"
    }
  ]
}
```

---

### skills show

Show detailed information about a skill.

**Usage:**

```bash
notion skills show <name> [options]
```

**Arguments:**

- `name` (required): Skill name

**Options:**

- `--json`: Output as JSON

**Examples:**

```bash
notion skills show search
notion skills show page_create
notion skills show db_query --json
```

**Returns:**

```json
{
  "success": true,
  "data": {
    "name": "search",
    "description": "Search for pages and databases",
    "usage": "notion search <query> [options]",
    "arguments": [...],
    "options": [...],
    "examples": [...]
  }
}
```

---

*See [EXAMPLES.md](EXAMPLES.md) for common usage patterns.*
