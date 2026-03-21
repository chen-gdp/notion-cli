# Notion CLI Command Samples

## 0. notion auth

### Command
```bash
notion auth setup
```

### Interactive Prompt (human mode)
```
Notion CLI Authentication

To use this CLI, you need a Notion integration token.
1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Give it a name (e.g., "Notion CLI")
4. Copy the "Internal Integration Token"
5. Paste it below

Enter your Notion token: secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

✓ Token saved to ~/.config/notion-cli/config.json

To verify your setup, run: notion auth status
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "config_file": "/home/user/.config/notion-cli/config.json",
    "token_saved": true,
    "message": "Authentication configured successfully"
  },
  "error": null
}
```

---

### Command
```bash
notion auth status
```

### Human Output
```
Authentication Status: ✓ Authenticated

Config file:     /home/user/.config/notion-cli/config.json
Token source:    config file
Workspace:       Acme Corp
Integration:     Notion CLI

To logout, run: notion auth logout
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "authenticated": true,
    "config_file": "/home/user/.config/notion-cli/config.json",
    "token_source": "config",
    "workspace": {
      "name": "Acme Corp",
      "id": "abc123..."
    }
  },
  "error": null
}
```

### Not Authenticated (--json)
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_AUTHENTICATED",
    "message": "No Notion token found. Run 'notion auth setup' or set NOTION_TOKEN environment variable."
  }
}
```

---

### Command
```bash
notion auth logout
```

### Human Output
```
✓ Token removed from /home/user/.config/notion-cli/config.json

You are now logged out.
To authenticate again, run: notion auth setup
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "token_removed": true,
    "config_file": "/home/user/.config/notion-cli/config.json"
  },
  "error": null
}
```

---

## 1. notion search

### Command
```bash
notion search "meeting"
```

### Human Output (default)
```
Found 3 results for "meeting":

┌─────────────────────────┬──────────┬──────────────────────────────────────┬─────────────────────────┐
│ Title                   │ Type     │ ID                                   │ Last Edited            │
├─────────────────────────┼──────────┼──────────────────────────────────────┼─────────────────────────┤
│ Team Meeting Notes      │ page     │ 8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f │ 2026-03-20 14:30:00    │
│ Project Meetings DB     │ database │ a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d │ 2026-03-19 09:15:00    │
│ Weekly Sync Template    │ page     │ b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e │ 2026-03-18 16:45:00    │
└─────────────────────────┴──────────┴──────────────────────────────────────┴─────────────────────────┘
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": [
    {
      "id": "8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f",
      "title": "Team Meeting Notes",
      "type": "page",
      "url": "https://www.notion.so/Team-Meeting-Notes-8c9d6f7e3a2b4c5d6e7f8a9b0c1d2e3f",
      "last_edited_time": "2026-03-20T14:30:00.000Z"
    },
    {
      "id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "title": "Project Meetings DB",
      "type": "database",
      "url": "https://www.notion.so/Project-Meetings-DB-a1b2c3d4e5f67a8b9c0d1e2f3a4b5c6d",
      "last_edited_time": "2026-03-19T09:15:00.000Z"
    },
    {
      "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
      "title": "Weekly Sync Template",
      "type": "page",
      "url": "https://www.notion.so/Weekly-Sync-Template-b2c3d4e5f6a78b9c0d1e2f3a4b5c6d7e",
      "last_edited_time": "2026-03-18T16:45:00.000Z"
    }
  ],
  "error": null
}
```

---

## 2. notion get (Page)

### Command
```bash
notion get 8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f
```

### Human Output (default)
```
Page: Team Meeting Notes
┌─────────────────────────────────────────────────────────────┐
│ Property          │ Value                                   │
├─────────────────────────────────────────────────────────────┤
│ ID                │ 8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f    │
│ Title             │ Team Meeting Notes                      │
│ URL               │ https://www.notion.so/...               │
│ Created           │ 2026-03-15 10:00:00                     │
│ Last Edited       │ 2026-03-20 14:30:00                     │
│ Archived          │ No                                      │
│ Parent            │ page: Projects (1a2b3c4d...)            │
└─────────────────────────────────────────────────────────────┘
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "id": "8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f",
    "title": "Team Meeting Notes",
    "type": "page",
    "url": "https://www.notion.so/Team-Meeting-Notes-8c9d6f7e3a2b4c5d6e7f8a9b0c1d2e3f",
    "created_time": "2026-03-15T10:00:00.000Z",
    "last_edited_time": "2026-03-20T14:30:00.000Z",
    "archived": false,
    "parent": {
      "type": "page_id",
      "page_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
      "title": "Projects"
    },
    "properties": {
      "title": {
        "id": "title",
        "type": "title",
        "title": [{"text": {"content": "Team Meeting Notes"}}]
      }
    }
  },
  "error": null
}
```

---

## 3. notion page create

### Command
```bash
notion page create --parent 1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d --title "New Project Plan"
```

### Human Output (default)
```
✓ Page created successfully

Page ID:    9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a
Title:      New Project Plan
URL:        https://www.notion.so/New-Project-Plan-9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "id": "9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a",
    "title": "New Project Plan",
    "type": "page",
    "url": "https://www.notion.so/New-Project-Plan-9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a",
    "created_time": "2026-03-20T15:00:00.000Z",
    "last_edited_time": "2026-03-20T15:00:00.000Z",
    "archived": false
  },
  "error": null
}
```

### Error Case (parent not found)
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "PARENT_NOT_FOUND",
    "message": "Parent page with ID '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d' not found",
    "details": {
      "parent_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
    }
  }
}
```

---

## 4. notion page append

### Command
```bash
notion page append 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a --content "## Project Goals

1. Launch MVP by Q2
2. Acquire 1000 users
3. Raise Series A

```python
# Sample code
def hello():
    return 'world'
```"
```

### Human Output (default)
```
✓ Appended 4 blocks to page "New Project Plan"

Blocks added:
  • Heading 2: Project Goals
  • Bulleted list: Launch MVP by Q2
  • Bulleted list: Acquire 1000 users
  • Bulleted list: Raise Series A
  • Code block (python)
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "page_id": "9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a",
    "blocks_added": 5,
    "blocks": [
      {
        "id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
        "type": "heading_2",
        "text": "Project Goals"
      },
      {
        "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
        "type": "bulleted_list_item",
        "text": "Launch MVP by Q2"
      },
      {
        "id": "c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f",
        "type": "bulleted_list_item",
        "text": "Acquire 1000 users"
      },
      {
        "id": "d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a",
        "type": "bulleted_list_item",
        "text": "Raise Series A"
      },
      {
        "id": "e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b",
        "type": "code",
        "language": "python",
        "text": "def hello():\n    return 'world'"
      }
    ]
  },
  "error": null
}
```

---

## 5. notion page update

### Command
```bash
notion page update 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a --title "Updated Project Plan"
```

### Human Output (default)
```
✓ Page updated successfully

Page ID:    9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a
New Title:  Updated Project Plan
URL:        https://www.notion.so/Updated-Project-Plan-9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "id": "9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a",
    "title": "Updated Project Plan",
    "type": "page",
    "url": "https://www.notion.so/Updated-Project-Plan-9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a",
    "last_edited_time": "2026-03-20T15:05:00.000Z",
    "updated_fields": ["title"]
  },
  "error": null
}
```

---

## 6. notion page archive

### Command
```bash
notion page archive 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a
```

### Human Output (default)
```
✓ Page archived successfully

Page ID:     9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a
Title:       Updated Project Plan
Status:      Archived
```

### Unarchive Command
```bash
notion page archive 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a --unarchive
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "id": "9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a",
    "title": "Updated Project Plan",
    "archived": true,
    "last_edited_time": "2026-03-20T15:10:00.000Z"
  },
  "error": null
}
```

---

## 7. notion db get

### Command
```bash
notion db get a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d
```

### Human Output (default)
```
Database: Project Meetings DB
┌─────────────────────────────────────────────────────────────┐
│ Property          │ Type      │ Options / Notes            │
├─────────────────────────────────────────────────────────────┤
│ Title             │ title     │ Required                    │
│ Status            │ select    │ Not started, In progress,   │
│                   │           │ Done                         │
│ Priority          │ select    │ Low, Medium, High            │
│ Assignee          │ people    │                             │
│ Due Date          │ date      │                             │
│ Tags              │ multi_select│                          │
└─────────────────────────────────────────────────────────────┘

Total entries: 42
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "title": "Project Meetings DB",
    "type": "database",
    "url": "https://www.notion.so/Project-Meetings-DB-a1b2c3d4e5f67a8b9c0d1e2f3a4b5c6d",
    "properties": {
      "title": {
        "id": "title",
        "name": "Title",
        "type": "title"
      },
      "status": {
        "id": "status",
        "name": "Status",
        "type": "select",
        "select": {
          "options": [
            {"name": "Not started", "color": "gray"},
            {"name": "In progress", "color": "yellow"},
            {"name": "Done", "color": "green"}
          ]
        }
      },
      "priority": {
        "id": "priority",
        "name": "Priority",
        "type": "select",
        "select": {
          "options": [
            {"name": "Low", "color": "blue"},
            {"name": "Medium", "color": "orange"},
            {"name": "High", "color": "red"}
          ]
        }
      },
      "due_date": {
        "id": "due_date",
        "name": "Due Date",
        "type": "date"
      }
    }
  },
  "error": null
}
```

---

## 8. notion db query

### Command
```bash
notion db query a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d --filter "status=In progress" --limit 5
```

### Human Output (default)
```
Query results for "Project Meetings DB" (showing 5 of 12):

┌─────────────────────────┬───────────────┬──────────┬─────────────────────────┐
│ Title                   │ Status        │ Priority │ Due Date                │
├─────────────────────────┼───────────────┼──────────┼─────────────────────────┤
│ Q1 Planning Meeting     │ In progress   │ High     │ 2026-03-25              │
│ Sprint Review #12       │ In progress   │ Medium   │ 2026-03-22              │
│ Budget Discussion       │ In progress   │ High     │ 2026-03-28              │
│ Team Onboarding         │ In progress   │ Low      │ 2026-04-01              │
└─────────────────────────┴───────────────┴──────────┴─────────────────────────┘
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "database_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "total_results": 12,
    "has_more": true,
    "next_cursor": "c2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
    "results": [
      {
        "id": "f1e2d3c4-b5a6-7c8d-9e0f-1a2b3c4d5e6f",
        "title": "Q1 Planning Meeting",
        "url": "https://www.notion.so/Q1-Planning-Meeting-f1e2d3c4b5a67c8d9e0f1a2b3c4d5e6f",
        "properties": {
          "title": {"text": [{"content": "Q1 Planning Meeting"}]},
          "status": {"select": {"name": "In progress"}},
          "priority": {"select": {"name": "High"}},
          "due_date": {"date": {"start": "2026-03-25"}}
        },
        "created_time": "2026-03-10T09:00:00.000Z",
        "last_edited_time": "2026-03-20T14:00:00.000Z"
      }
    ]
  },
  "error": null
}
```

---

## 9. notion db insert

### Command
```bash
notion db insert a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d --title "New Meeting" --properties "status=In progress,priority=High,due_date=2026-03-30"
```

### Human Output (default)
```
✓ Entry created in database "Project Meetings DB"

Entry ID:    b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e
Title:       New Meeting
Status:      In progress
Priority:    High
Due Date:    2026-03-30
URL:         https://www.notion.so/New-Meeting-b2c3d4e5f6a78b9c0d1e2f3a4b5c6d7e
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
    "title": "New Meeting",
    "type": "page",
    "url": "https://www.notion.so/New-Meeting-b2c3d4e5f6a78b9c0d1e2f3a4b5c6d7e",
    "properties": {
      "title": {"text": [{"content": "New Meeting"}]},
      "status": {"select": {"name": "In progress"}},
      "priority": {"select": {"name": "High"}},
      "due_date": {"date": {"start": "2026-03-30"}}
    },
    "created_time": "2026-03-20T15:30:00.000Z",
    "last_edited_time": "2026-03-20T15:30:00.000Z"
  },
  "error": null
}
```

---

## 10. notion skills list

### Command
```bash
notion skills list
```

### Human Output (default)
```
Available Skills (12 total):

┌──────────────────────────┬──────────────────────────────────────────────────┬─────────────┐
│ Skill                    │ Description                                      │ Category    │
├──────────────────────────┼──────────────────────────────────────────────────┼─────────────┤
│ search                   │ Search for pages and databases                   │ discovery   │
│ get                      │ Get page or database by ID                       │ discovery   │
│ page_create              │ Create a new page in Notion                      │ content     │
│ page_append              │ Append blocks to a page                          │ content     │
│ page_update              │ Update page properties                           │ content     │
│ page_archive             │ Archive or unarchive a page                      │ content     │
│ db_get                   │ Get database schema                              │ discovery   │
│ db_query                 │ Query database entries                           │ content     │
│ db_insert                │ Insert entry into database                       │ content     │
│ skills_list              │ List all available skills                        │ meta        │
│ skills_show              │ Show detailed skill information                  │ meta        │
└──────────────────────────┴──────────────────────────────────────────────────┴─────────────┘

Use 'notion skills show <skill>' for detailed usage.
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "total_skills": 11,
    "skills": [
      {
        "name": "search",
        "description": "Search for pages and databases",
        "category": "discovery"
      },
      {
        "name": "get",
        "description": "Get page or database by ID",
        "category": "discovery"
      },
      {
        "name": "page_create",
        "description": "Create a new page in Notion",
        "category": "content"
      },
      {
        "name": "page_append",
        "description": "Append blocks to a page",
        "category": "content"
      },
      {
        "name": "page_update",
        "description": "Update page properties",
        "category": "content"
      },
      {
        "name": "page_archive",
        "description": "Archive or unarchive a page",
        "category": "content"
      },
      {
        "name": "db_get",
        "description": "Get database schema",
        "category": "discovery"
      },
      {
        "name": "db_query",
        "description": "Query database entries",
        "category": "content"
      },
      {
        "name": "db_insert",
        "description": "Insert entry into database",
        "category": "content"
      },
      {
        "name": "skills_list",
        "description": "List all available skills",
        "category": "meta"
      },
      {
        "name": "skills_show",
        "description": "Show detailed skill information",
        "category": "meta"
      }
    ]
  },
  "error": null
}
```

---

## 11. notion skills show

### Command
```bash
notion skills show page_append
```

### Human Output (default)
```
Skill: page_append

Description:
  Append blocks to a Notion page. Supports markdown formatting including
  headings, lists, code blocks, and rich text.

Usage:
  notion page append <page_id> [options]

Arguments:
  page_id                   The ID or URL of the page to append to

Options:
  --content, -c TEXT        Content to append (supports markdown)  [required]
  --json                    Output as JSON
  --help                    Show this message and exit

Examples:
  # Append simple text
  notion page append 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a --content "Hello World"

  # Append formatted markdown
  notion page append 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a --content "## Heading

  - Item 1
  - Item 2

  \`\`\`python
  print('hello')
  \`\`\`"

Returns:
  • blocks_added: Number of blocks created
  • blocks: Array of created block objects with IDs and types

Category: content
```

### JSON Output (--json)
```json
{
  "success": true,
  "data": {
    "name": "page_append",
    "description": "Append blocks to a Notion page. Supports markdown formatting including headings, lists, code blocks, and rich text.",
    "category": "content",
    "usage": "notion page append <page_id> [options]",
    "arguments": [
      {
        "name": "page_id",
        "description": "The ID or URL of the page to append to",
        "required": true
      }
    ],
    "options": [
      {
        "name": "--content",
        "short": "-c",
        "description": "Content to append (supports markdown)",
        "type": "TEXT",
        "required": true
      },
      {
        "name": "--json",
        "description": "Output as JSON",
        "type": "boolean",
        "required": false
      }
    ],
    "examples": [
      "notion page append 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a --content \"Hello World\"",
      "notion page append 9d8e7f6a-5b4c-3d2e-1f0a-9b8c7d6e5f4a --content \"## Heading\\n\\n- Item 1\\n- Item 2\""
    ],
    "returns": {
      "description": "Object containing blocks_added count and array of created blocks",
      "fields": [
        {"name": "blocks_added", "type": "integer"},
        {"name": "blocks", "type": "array", "items": {"id": "string", "type": "string", "text": "string"}}
      ]
    }
  },
  "error": null
}
```

---

## Common Error Examples

### Authentication Error
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "AUTH_ERROR",
    "message": "Notion token not found. Set NOTION_TOKEN environment variable."
  }
}
```

### Rate Limit Error
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded. Retry after 60 seconds.",
    "retry_after": 60
  }
}
```

### Not Found Error
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "Page with ID 'xyz' not found or you don't have access",
    "details": {
      "id": "xyz",
      "type": "page"
    }
  }
}
```
