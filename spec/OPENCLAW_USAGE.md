# OpenClaw Usage Examples

Real-world scenarios showing how an AI agent (OpenClaw) would use the Notion CLI.

---

## Scenario 1: Agent Needs to Find and Update a Meeting Note

**Context:** User asks OpenClaw: "Find yesterday's team meeting notes and add action items."

### Step 1: Agent discovers available commands
```bash
$ notion skills list --json
{
  "success": true,
  "data": {
    "skills": [
      {"name": "search", "description": "Search for pages and databases", "category": "discovery"},
      {"name": "get", "description": "Get page or database by ID", "category": "discovery"},
      {"name": "page_append", "description": "Append blocks to a page", "category": "content"}
    ]
  }
}
```

### Step 2: Agent searches for meeting notes
```bash
$ notion search "team meeting" --json
{
  "success": true,
  "data": [
    {
      "id": "8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f",
      "title": "Team Meeting - March 19, 2026",
      "type": "page",
      "last_edited_time": "2026-03-19T16:00:00.000Z"
    },
    {
      "id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "title": "Team Meeting Notes Template",
      "type": "page",
      "last_edited_time": "2026-01-15T10:00:00.000Z"
    }
  ]
}
```

Agent logic: "March 19 is yesterday's meeting. I'll use ID 8c9d6f7e..."

### Step 3: Agent gets the page to verify it's the right one
```bash
$ notion get 8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f --json
{
  "success": true,
  "data": {
    "id": "8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f",
    "title": "Team Meeting - March 19, 2026",
    "url": "https://www.notion.so/...",
    "archived": false,
    "last_edited_time": "2026-03-19T16:00:00.000Z"
  }
}
```

### Step 4: Agent appends action items
```bash
$ notion page append 8c9d6f7e-3a2b-4c5d-6e7f-8a9b0c1d2e3f \
  --content "## Action Items\n\n- [ ] Review Q1 roadmap\n- [ ] Schedule follow-up with design team\n- [ ] Update project documentation" \
  --json
{
  "success": true,
  "data": {
    "blocks_added": 4,
    "blocks": [
      {"id": "...", "type": "heading_2", "text": "Action Items"},
      {"id": "...", "type": "to_do", "text": "Review Q1 roadmap", "checked": false},
      {"id": "...", "type": "to_do", "text": "Schedule follow-up with design team", "checked": false},
      {"id": "...", "type": "to_do", "text": "Update project documentation", "checked": false}
    ]
  }
}
```

### Step 5: Agent reports success to user
"I've added 3 action items to yesterday's team meeting notes (Team Meeting - March 19, 2026)."

---

## Scenario 2: Agent Creates a New Project Page

**Context:** User asks OpenClaw: "Create a project page for the new API redesign initiative."

### Step 1: Agent searches for existing project database
```bash
$ notion search "projects" --type database --json
{
  "success": true,
  "data": [
    {
      "id": "db123456-7890-1234-5678-901234567890",
      "title": "Projects Database",
      "type": "database"
    }
  ]
}
```

### Step 2: Agent gets database schema to understand required fields
```bash
$ notion db get db123456-7890-1234-5678-901234567890 --json
{
  "success": true,
  "data": {
    "id": "db123456-7890-1234-5678-901234567890",
    "title": "Projects Database",
    "properties": {
      "title": {"type": "title", "name": "Project Name"},
      "status": {"type": "select", "options": ["Not started", "In progress", "Done"]},
      "priority": {"type": "select", "options": ["Low", "Medium", "High"]},
      "owner": {"type": "people"},
      "due_date": {"type": "date"}
    }
  }
}
```

### Step 3: Agent inserts new project into database
```bash
$ notion db insert db123456-7890-1234-5678-901234567890 \
  --title "API Redesign Initiative" \
  --properties "status=Not started,priority=High,due_date=2026-06-30" \
  --json
{
  "success": true,
  "data": {
    "id": "proj7890-abcd-efgh-ijkl-mnopqrstuvwx",
    "title": "API Redesign Initiative",
    "url": "https://www.notion.so/API-Redesign-Initiative-proj7890...",
    "properties": {
      "status": {"select": {"name": "Not started"}},
      "priority": {"select": {"name": "High"}},
      "due_date": {"date": {"start": "2026-06-30"}}
    }
  }
}
```

### Step 4: Agent populates the project page with initial content
```bash
$ notion page append proj7890-abcd-efgh-ijkl-mnopqrstuvwx \
  --content "## Overview\n\nThis project focuses on redesigning our core API for better performance and developer experience.\n\n## Goals\n\n1. Improve response times by 50%\n2. Implement GraphQL support\n3. Better error handling and documentation\n\n## Timeline\n\n- **Q2**: Research and planning\n- **Q3**: Implementation\n- **Q4**: Testing and rollout" \
  --json
{
  "success": true,
  "data": {
    "blocks_added": 10
  }
}
```

### Step 5: Agent reports to user
"Created 'API Redesign Initiative' project in the Projects Database. Set status to 'Not started' with High priority and due date of June 30, 2026. Added overview, goals, and timeline sections to the project page."

---

## Scenario 3: Agent Queries Database and Updates Multiple Items

**Context:** User asks OpenClaw: "Show me all high priority tasks that are in progress."

### Step 1: Agent finds the tasks database
```bash
$ notion search "tasks" --type database --json
{
  "success": true,
  "data": [
    {
      "id": "tasks-db-1234-5678-abcd-efgh",
      "title": "Tasks",
      "type": "database"
    }
  ]
}
```

### Step 2: Agent queries with filters
```bash
$ notion db query tasks-db-1234-5678-abcd-efgh \
  --filter "priority=High,status=In progress" \
  --json
{
  "success": true,
  "data": {
    "total_results": 5,
    "results": [
      {
        "id": "task-001-aaaa-bbbb-cccc",
        "title": "Fix authentication bug",
        "properties": {
          "status": {"select": {"name": "In progress"}},
          "priority": {"select": {"name": "High"}},
          "assignee": {"people": [{"name": "Alice"}]},
          "due_date": {"date": {"start": "2026-03-22"}}
        }
      },
      {
        "id": "task-002-dddd-eeee-ffff",
        "title": "Update API documentation",
        "properties": {
          "status": {"select": {"name": "In progress"}},
          "priority": {"select": {"name": "High"}},
          "assignee": {"people": [{"name": "Bob"}]},
          "due_date": {"date": {"start": "2026-03-25"}}
        }
      }
    ]
  }
}
```

### Step 3: Agent formats results for user
Found 5 high priority tasks in progress:

1. **Fix authentication bug** (Alice) - Due Mar 22
2. **Update API documentation** (Bob) - Due Mar 25
3. ... (and 3 more)

**User then says:** "Mark the authentication bug as done."

### Step 4: Agent updates the task
```bash
$ notion page update task-001-aaaa-bbbb-cccc \
  --properties "status=Done" \
  --json
{
  "success": true,
  "data": {
    "id": "task-001-aaaa-bbbb-cccc",
    "title": "Fix authentication bug",
    "updated_fields": ["status"]
  }
}
```

### Step 5: Agent confirms
"Marked 'Fix authentication bug' as Done."

---

## Scenario 4: Agent Discovers New Capabilities

**Context:** User asks OpenClaw: "Can this tool create databases?"

### Step 1: Agent searches for database-related skills
```bash
$ notion skills list | grep -i database
```

Or using JSON:
```bash
$ notion skills list --json | jq '.data.skills[] | select(.name | contains("db"))'
{
  "name": "db_get",
  "description": "Get database schema",
  "category": "discovery"
}
{
  "name": "db_query",
  "description": "Query database entries",
  "category": "content"
}
{
  "name": "db_insert",
  "description": "Insert entry into database",
  "category": "content"
}
```

### Step 2: Agent checks if there's a database creation skill
Agent notices there's no `db_create` skill listed.

### Step 3: Agent gets detailed info on available database skills
```bash
$ notion skills show db_insert --json
{
  "success": true,
  "data": {
    "name": "db_insert",
    "description": "Insert entry into database",
    "category": "content"
    // ... details show this is for inserting rows, not creating databases
  }
}
```

### Step 4: Agent reports to user
"The Notion CLI can query existing databases (`db_query`), get schema (`db_get`), and insert entries (`db_insert`), but database creation is not currently supported in this version."

---

## Scenario 5: Agent Handles Errors Gracefully

**Context:** User asks OpenClaw: "Update the page called 'Budget' with new numbers."

### Step 1: Agent searches for Budget page
```bash
$ notion search "Budget" --json
{
  "success": true,
  "data": [
    {
      "id": "budget-2024-aaaa-bbbb",
      "title": "Budget 2024",
      "type": "page"
    },
    {
      "id": "budget-2025-cccc-dddd",
      "title": "Budget 2025",
      "type": "page"
    }
  ]
}
```

### Step 2: Agent detects ambiguity and asks for clarification
"I found 2 pages with 'Budget' in the title:
1. Budget 2024 (ID: budget-2024-aaaa-bbbb)
2. Budget 2025 (ID: budget-2025-cccc-dddd)

Which one would you like to update?"

**User says:** "The 2025 one."

### Step 3: Agent attempts to update but encounters permission error
```bash
$ notion page update budget-2025-cccc-dddd --properties "total=100000" --json
{
  "success": false,
  "data": null,
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to edit this page",
    "details": {
      "page_id": "budget-2025-cccc-dddd",
      "required_permission": "write"
    }
  }
}
```

### Step 4: Agent reports the issue
"I wasn't able to update the Budget 2025 page. The error indicates I don't have write permission. You may need to:
1. Share the page with the Notion integration
2. Check if the page is locked
3. Verify the integration token has the necessary permissions"

---

## Scenario 6: Agent Creates Structured Documentation

**Context:** User asks OpenClaw: "Create a new page for the onboarding guide with sections for setup, tools, and first day."

### Step 1: Agent finds where to create the page
```bash
$ notion search "Wiki" --type database --json
{
  "success": true,
  "data": [
    {
      "id": "wiki-db-1234-abcd",
      "title": "Team Wiki",
      "type": "database"
    }
  ]
}
```

### Step 2: Agent inserts the new page
```bash
$ notion db insert wiki-db-1234-abcd \
  --title "New Hire Onboarding Guide" \
  --properties "category=Documentation" \
  --json
{
  "success": true,
  "data": {
    "id": "onboard-page-5678-efgh",
    "title": "New Hire Onboarding Guide",
    "url": "https://www.notion.so/..."
  }
}
```

### Step 3: Agent appends structured content with multiple block types
```bash
$ notion page append onboard-page-5678-efgh \
  --content "# New Hire Onboarding Guide\n\nWelcome to the team! This guide will help you get up and running.\n\n## Setup\n\nFirst, let's get your development environment configured:\n\n1. Install required software\n2. Clone the repository\n3. Run the setup script\n\n### Required Accounts\n\n- GitHub\n- Slack\n- Notion\n- Figma\n\n## Tools We Use\n\n| Tool | Purpose | Link |\n|------|---------|------|\n| Slack | Communication | slack.company.com |\n| GitHub | Code repository | github.com/company |\n| Figma | Design | figma.com |\n\n## First Day Checklist\n\n- [ ] Meet your buddy\n- [ ] Set up your workspace\n- [ ] Join team channels\n- [ ] Schedule 1:1s\n\n```bash\n# Quick start\nnpm install\nnpm run dev\n```\n\n---\n\n**Questions?** Ask in #new-hires Slack channel." \
  --json
{
  "success": true,
  "data": {
    "blocks_added": 25
  }
}
```

### Step 4: Agent reports completion
"Created 'New Hire Onboarding Guide' in the Team Wiki with:
- Welcome section
- Setup instructions with numbered list
- Tools table
- First day checklist with todos
- Code block for quick start
- Callout for questions"

---

## Key Design Patterns Observed

1. **Discovery First**: Agent always starts with `skills list` or `search` to understand what's available
2. **JSON Mode**: Agent uses `--json` for all programmatic calls to parse results reliably
3. **Verification**: Agent often does `get` after `search` to verify the right object
4. **Incremental Building**: Agent creates structure first, then populates content
5. **Error Handling**: Agent checks `success` field and reports meaningful errors to user
6. **Ambiguity Resolution**: When search returns multiple results, agent asks for clarification rather than guessing
