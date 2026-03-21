# JSON Output Format

Complete reference for JSON output schemas used by all CLI commands.

## Table of Contents

- [Response Structure](#response-structure)
- [Success Response](#success-response)
- [Error Response](#error-response)
- [Common Data Types](#common-data-types)
- [Command-Specific Schemas](#command-specific-schemas)
- [Error Codes](#error-codes)

---

## Response Structure

All commands return a consistent JSON structure when using `--json` flag:

```json
{
  "success": boolean,
  "data": object | array | null,
  "error": object | null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | `true` if command succeeded, `false` if error |
| `data` | object/array/null | Command-specific data (null if error) |
| `error` | object/null | Error details (null if success) |

---

## Success Response

When `success: true`, the `data` field contains command-specific output.

```json
{
  "success": true,
  "data": {
    // Command-specific data structure
  },
  "error": null
}
```

---

## Error Response

When `success: false`, the `error` field contains error details.

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

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | Machine-readable error code |
| `message` | string | Human-readable error description |
| `details` | object | Additional context (optional) |

---

## Common Data Types

### Page Object

```json
{
  "id": "abc123-def456-ghi789",
  "title": "Page Title",
  "type": "page",
  "url": "https://notion.so/abc123-def456-ghi789",
  "created_time": "2024-03-20T10:00:00Z",
  "last_edited_time": "2024-03-20T14:30:00Z",
  "properties": {
    // Page-specific properties
  },
  "blocks": [
    // Only included with --blocks flag
  ]
}
```

### Database Object

```json
{
  "id": "abc123-def456-ghi789",
  "title": "Database Name",
  "type": "database",
  "url": "https://notion.so/abc123-def456-ghi789",
  "created_time": "2024-03-20T10:00:00Z",
  "last_edited_time": "2024-03-20T14:30:00Z",
  "properties": {
    "Name": {
      "type": "title"
    },
    "Status": {
      "type": "select",
      "options": [
        {"name": "Open", "color": "green"},
        {"name": "Done", "color": "blue"}
      ]
    }
  }
}
```

### Database Entry Object

```json
{
  "id": "entry123-def456",
  "title": "Entry Title",
  "url": "https://notion.so/entry123-def456",
  "properties": {
    "Status": {
      "type": "select",
      "value": "Open"
    },
    "Priority": {
      "type": "select",
      "value": "High"
    }
  }
}
```

### Property Types

#### Title

```json
{
  "type": "title",
  "value": "Page Title"
}
```

#### Select

```json
{
  "type": "select",
  "value": "Option Name"
}
```

#### Multi-Select

```json
{
  "type": "multi_select",
  "value": ["Tag1", "Tag2"]
}
```

#### Status

```json
{
  "type": "status",
  "value": "In Progress"
}
```

#### Checkbox

```json
{
  "type": "checkbox",
  "value": true
}
```

#### Number

```json
{
  "type": "number",
  "value": 42.5
}
```

#### Date

```json
{
  "type": "date",
  "value": "2024-03-20"
}
```

#### Date with Time

```json
{
  "type": "date",
  "value": "2024-03-20T14:30:00"
}
```

#### URL

```json
{
  "type": "url",
  "value": "https://example.com"
}
```

#### Email

```json
{
  "type": "email",
  "value": "user@example.com"
}
```

#### Phone

```json
{
  "type": "phone",
  "value": "+1-555-123-4567"
}
```

#### Rich Text

```json
{
  "type": "rich_text",
  "value": "Text content with formatting"
}
```

---

## Command-Specific Schemas

### auth status

```json
{
  "success": true,
  "data": {
    "authenticated": true,
    "source": "env",
    "config_path": "~/.config/notion-cli/config.json"
  },
  "error": null
}
```

**Fields:**
- `authenticated` (boolean): Whether token is configured
- `source` (string): `"env"` or `"config"`
- `config_path` (string): Path to config file

### auth setup

```json
{
  "success": true,
  "data": {
    "message": "Authentication configured successfully",
    "config_path": "~/.config/notion-cli/config.json"
  },
  "error": null
}
```

### auth logout

```json
{
  "success": true,
  "data": {
    "message": "Authentication removed"
  },
  "error": null
}
```

### search

```json
{
  "success": true,
  "data": [
    {
      "id": "abc123-def456",
      "title": "Meeting Notes",
      "type": "page",
      "url": "https://notion.so/abc123-def456",
      "last_edited_time": "2024-03-20T14:30:00Z"
    },
    {
      "id": "def456-ghi789",
      "title": "Tasks",
      "type": "database",
      "url": "https://notion.so/def456-ghi789",
      "last_edited_time": "2024-03-19T10:00:00Z"
    }
  ],
  "error": null
}
```

### get (page)

```json
{
  "success": true,
  "data": {
    "id": "abc123-def456",
    "title": "Page Title",
    "type": "page",
    "url": "https://notion.so/abc123-def456",
    "created_time": "2024-03-20T10:00:00Z",
    "last_edited_time": "2024-03-20T14:30:00Z",
    "properties": {
      "title": {
        "type": "title",
        "value": "Page Title"
      }
    },
    "blocks": [
      // Only with --blocks flag
      {
        "type": "heading_1",
        "text": "Heading"
      },
      {
        "type": "paragraph",
        "text": "Paragraph content"
      }
    ]
  },
  "error": null
}
```

### get (database)

```json
{
  "success": true,
  "data": {
    "id": "abc123-def456",
    "title": "Database Name",
    "type": "database",
    "url": "https://notion.so/abc123-def456",
    "created_time": "2024-03-20T10:00:00Z",
    "last_edited_time": "2024-03-20T14:30:00Z",
    "properties": {
      "Name": {
        "type": "title"
      },
      "Status": {
        "type": "select",
        "options": [
          {"name": "Open", "color": "green"},
          {"name": "In Progress", "color": "yellow"},
          {"name": "Done", "color": "blue"}
        ]
      },
      "Priority": {
        "type": "select",
        "options": [
          {"name": "Low", "color": "gray"},
          {"name": "Medium", "color": "orange"},
          {"name": "High", "color": "red"}
        ]
      }
    }
  },
  "error": null
}
```

### db get

Same schema as `get` for databases.

### db query

```json
{
  "success": true,
  "data": [
    {
      "id": "entry123-def456",
      "title": "Task Name",
      "url": "https://notion.so/entry123-def456",
      "properties": {
        "Status": {
          "type": "select",
          "value": "Open"
        },
        "Priority": {
          "type": "select",
          "value": "High"
        },
        "Due Date": {
          "type": "date",
          "value": "2024-03-25"
        }
      }
    }
  ],
  "error": null
}
```

### db insert

```json
{
  "success": true,
  "data": {
    "id": "entry123-def456",
    "title": "New Task",
    "url": "https://notion.so/entry123-def456"
  },
  "error": null
}
```

### page create

```json
{
  "success": true,
  "data": {
    "id": "page123-def456",
    "title": "New Page",
    "url": "https://notion.so/page123-def456"
  },
  "error": null
}
```

### page append

```json
{
  "success": true,
  "data": {
    "page_id": "abc123-def456",
    "blocks_added": 5
  },
  "error": null
}
```

**Fields:**
- `page_id` (string): ID of the page that was updated
- `blocks_added` (number): Number of blocks added

### page update

```json
{
  "success": true,
  "data": {
    "id": "abc123-def456",
    "updated_fields": ["title", "Status"]
  },
  "error": null
}
```

**Fields:**
- `id` (string): ID of the updated page
- `updated_fields` (array): List of fields that were modified

### page archive

```json
{
  "success": true,
  "data": {
    "id": "abc123-def456",
    "action": "archive",
    "archived": true
  },
  "error": null
}
```

**Fields:**
- `id` (string): ID of the page
- `action` (string): `"archive"` or `"unarchive"`
- `archived` (boolean): New archived status

### skills list

```json
{
  "success": true,
  "data": [
    {
      "name": "search",
      "description": "Search for pages and databases",
      "category": "discovery"
    },
    {
      "name": "db_query",
      "description": "Query database entries",
      "category": "database"
    }
  ],
  "error": null
}
```

### skills show

```json
{
  "success": true,
  "data": {
    "name": "search",
    "description": "Search for pages and databases",
    "category": "discovery",
    "usage": "notion search <query> [options]",
    "arguments": [
      {
        "name": "query",
        "required": true,
        "description": "Search query string"
      }
    ],
    "options": [
      {
        "name": "--type",
        "description": "Filter by type (page or database)"
      },
      {
        "name": "--limit",
        "description": "Maximum results (default: 100)"
      },
      {
        "name": "--json",
        "description": "Output as JSON"
      }
    ],
    "examples": [
      "notion search 'meeting'",
      "notion search 'tasks' --type database"
    ]
  },
  "error": null
}
```

---

## Error Codes

### AUTH_ERROR

Authentication failed or no token configured.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "AUTH_ERROR",
    "message": "No authentication token configured. Set NOTION_TOKEN environment variable or run 'notion auth setup'.",
    "details": {}
  }
}
```

**Resolution:** Set `NOTION_TOKEN` environment variable or run `notion auth setup`.

### NOT_FOUND

Resource not found.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "Page not found: abc123-def456",
    "details": {
      "id": "abc123-def456",
      "type": "page"
    }
  }
}
```

**Resolution:** Verify the ID is correct and the resource exists.

### VALIDATION_ERROR

Invalid input parameters.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Missing required argument: --title",
    "details": {
      "field": "title",
      "reason": "required"
    }
  }
}
```

**Resolution:** Check command usage with `notion skills show <command>`.

### RATE_LIMIT

Too many requests.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "RATE_LIMIT",
    "message": "Rate limit exceeded. Retry after 60 seconds.",
    "details": {
      "retry_after": 60
    }
  }
}
```

**Resolution:** Wait before retrying. Consider adding delays between requests.

### API_ERROR

Notion API returned an error.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "API_ERROR",
    "message": "Invalid request body",
    "details": {
      "notion_error": "validation_error",
      "message": "body failed validation"
    }
  }
}
```

**Resolution:** Check the Notion API documentation for valid request formats.

### NETWORK_ERROR

Network connectivity issue.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NETWORK_ERROR",
    "message": "Failed to connect to Notion API",
    "details": {
      "url": "https://api.notion.com/v1/..."
    }
  }
}
```

**Resolution:** Check internet connection and try again.

### CONFIG_ERROR

Configuration file issue.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "CONFIG_ERROR",
    "message": "Failed to read config file",
    "details": {
      "path": "~/.config/notion-cli/config.json"
    }
  }
}
```

**Resolution:** Run `notion auth setup` to recreate configuration.

### UNKNOWN_ERROR

Unexpected error occurred.

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "UNKNOWN_ERROR",
    "message": "An unexpected error occurred",
    "details": {}
  }
}
```

**Resolution:** Check logs and report the issue.

---

## JQ Examples

### Extract IDs from search results

```bash
notion search "tasks" --json | jq -r '.data[].id'
```

### Filter by type

```bash
notion search "project" --json | jq '.data[] | select(.type == "database")'
```

### Get first result

```bash
notion search "meeting" --json | jq '.data[0]'
```

### Count results

```bash
notion db query <database_id> --json | jq '.data | length'
```

### Extract specific fields

```bash
notion db query <database_id> --json | jq '.data[] | {id, title}'
```

### Filter by property value

```bash
notion db query <database_id> --json | jq '.data[] | select(.properties.Status.value == "Done")'
```

### Chain commands

```bash
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')
notion db query "$DB_ID" --json | jq '.data[] | select(.properties.Priority.value == "High") | .id'
```

---

*See [COMMANDS.md](COMMANDS.md) for command usage details.*
