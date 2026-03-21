# Notion CLI Skills

Auto-generated documentation of available CLI commands.

## Table of Contents

- [Authentication](#authentication)
- [Search & Discovery](#search--discovery)
- [Database Operations](#database-operations)
- [Page Operations](#page-operations)
- [Utility](#utility)

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

- `--type`: Filter by type (page or database)
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

List of objects with id, title, type, url, and last_edited_time.

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

Page or database object with all properties.

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

Database object with id, title, and properties schema.

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

- `--filter`: Filter criteria (key=value,key2=value2)
- `--limit`: Maximum results (default: 100)
- `--json`: Output as JSON

**Examples:**

```bash
notion db query abc123-def456
notion db query abc123-def456 --filter "Status=Done"
notion db query abc123-def456 --limit 50 --json
```

**Returns:**

List of database entries with id, title, and properties.

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
- `--properties`: Properties (key=value,key2=value2)
- `--json`: Output as JSON

**Examples:**

```bash
notion db insert abc123-def456 --title "New Task"
notion db insert abc123-def456 --title "New Task" --properties "Status=Open,Priority=High"
notion db insert abc123-def456 --title "New Task" --json
```

**Returns:**

Created entry with id, title, and url.

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
notion page create --parent abc123-def456 --title "New Page"
notion page create --parent abc123-def456 --title "New Entry" --properties "Status=Open"
notion page create --parent abc123-def456 --title "New Page" --json
```

**Returns:**

Created page with id, title, and url.

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

**Examples:**

```bash
notion page append abc123-def456 --content "## Heading\n\nParagraph text"
notion page append abc123-def456 --content "- Item 1\n- Item 2"
notion page append abc123-def456 --content "## Meeting Notes\n\n- [ ] Action item" --json
```

**Returns:**

Object with page_id and blocks_added count.

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

Object with id and updated_fields list.

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

Object with id, action, and archived status.

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

List of skills with name, description, and category.

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

Skill details with name, description, usage, arguments, options, and examples.

---

## Markdown Support

The `page append` command supports rich markdown formatting:

### Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Lists

```markdown
- Bullet item 1
- Bullet item 2

1. Numbered item 1
2. Numbered item 2
```

### Todo Lists

```markdown
- [ ] Unchecked todo
- [x] Checked todo
```

### Code Blocks

```markdown
```python
def hello():
    return "world"
```
```

### Paragraphs

Plain text is automatically converted to paragraphs.

---

## JSON Output Format

All commands support `--json` for machine-readable output:

### Success Response

```json
{
  "success": true,
  "data": {
    // Command-specific data
  },
  "error": null
}
```

### Error Response

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional error context
    }
  }
}
```

### Common Error Codes

- `AUTH_ERROR`: Authentication failed or no token configured
- `NOT_FOUND`: Resource not found
- `VALIDATION_ERROR`: Invalid input parameters
- `RATE_LIMIT`: Too many requests, retry after delay
- `API_ERROR`: Notion API returned an error

---

## Authentication

The CLI supports two methods of authentication:

### Environment Variable (Recommended)

```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxx"
```

### Config File

```bash
notion auth setup
# Enter token when prompted
```

Configuration is stored in `~/.config/notion-cli/config.json`.

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NOTION_TOKEN` | Notion integration token | Yes* |

*Required unless configured via `notion auth setup`

---

*This documentation was auto-generated for notion-cli v0.1.0*
