# Usage Examples

Common patterns and one-liners for the Notion CLI.

## Table of Contents

- [Authentication](#authentication)
- [Finding Content](#finding-content)
- [Task Management](#task-management)
- [Documentation](#documentation)
- [Research Notes](#research-notes)
- [Database Operations](#database-operations)
- [Page Operations](#page-operations)
- [Chaining Commands](#chaining-commands)

---

## Authentication

### Check if authenticated

```bash
notion auth status
```

### Set up authentication

```bash
notion auth setup
# Enter your Notion integration token when prompted
```

### Use environment variable (CI/CD)

```bash
export NOTION_TOKEN="secret_xxxxxxxxxxxxx"
notion auth status --json
```

---

## Finding Content

### List all content (no search query needed)

```bash
notion ls              # List everything
notion ls --type page  # List only pages
notion ls --type database  # List only databases
```

### Search everything

```bash
notion search "meeting"
```

### Search only databases

```bash
notion search "tasks" --type database
```

### Search only pages

```bash
notion search "notes" --type page
```

### Limit results

```bash
notion search "project" --limit 10
```

### Get by ID

```bash
notion get abc123-def456
notion get abc123-def456 --blocks  # Include content
```

---

## Task Management

### Find tasks database

```bash
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')
echo "Database ID: $DB_ID"
```

### View database schema

```bash
notion db get "$DB_ID"
```

### Query all open tasks

```bash
notion db query "$DB_ID" --filter "Status=Open"
```

### Query high priority open tasks

```bash
notion db query "$DB_ID" --filter "Status=Open,Priority=High"
```

### Create new task

```bash
notion db insert "$DB_ID" --title "Fix bug #123" --properties "Status=Open,Priority=High"
```

### Create task with due date

```bash
notion db insert "$DB_ID" --title "Review PR" --properties "Status=Open,Due Date=2024-03-25"
```

### Mark task as done

```bash
TASK_ID=$(notion db query "$DB_ID" --filter "Title=Fix bug #123" --json | jq -r '.data[0].id')
notion page update "$TASK_ID" --properties "Status=Done"
```

### Archive completed tasks

```bash
for task_id in $(notion db query "$DB_ID" --filter "Status=Done" --json | jq -r '.data[].id'); do
    notion page archive "$task_id"
done
```

---

## Documentation

### Create documentation page

```bash
PAGE_ID=$(notion page create --parent <wiki_id> --title "API Guide" --json | jq -r '.data.id')
```

### Add structured content

```bash
notion page append "$PAGE_ID" --content "## Overview

API endpoints:

- GET /users
- POST /users
- DELETE /users/:id

\`\`\`bash
curl https://api.example.com/users
\`\`\`"
```

### Add code examples

```bash
notion page append "$PAGE_ID" --content "## Python Example

\`\`\`python
import requests

response = requests.get('https://api.example.com/users')
data = response.json()
\`\`\`"
```

### Add todo list

```bash
notion page append "$PAGE_ID" --content "## Implementation Checklist

- [ ] Set up authentication
- [ ] Implement GET endpoint
- [ ] Add rate limiting
- [ ] Write tests
- [ ] Deploy to staging"
```

### Update page title

```bash
notion page update "$PAGE_ID" --title "API Guide v2"
```

---

## Research Notes

### Search existing research

```bash
notion search "competitor analysis" --json | jq '.data[] | {title, id, url}'
```

### Create new research page

```bash
PAGE_ID=$(notion page create --parent <research_db> --title "Q2 Competitor Analysis" --json | jq -r '.data.id')
```

### Add findings incrementally

```bash
notion page append "$PAGE_ID" --content "## Competitor A

**Strengths:**
- Fast and reliable
- Good documentation
- Active community

**Weaknesses:**
- Expensive pricing
- Limited integrations"
```

```bash
notion page append "$PAGE_ID" --content "## Competitor B

**Strengths:**
- Free tier available
- Easy to use

**Weaknesses:**
- Limited features
- Slow support"
```

### Add structured comparison

```bash
notion page append "$PAGE_ID" --content "## Comparison Table

| Feature | Competitor A | Competitor B |
|---------|--------------|--------------|
| Price | $$$ | $ |
| Speed | Fast | Medium |
| Support | 24/7 | Email only |"
```

---

## Database Operations

### Get database schema

```bash
notion db get <database_id>
```

### Query all entries

```bash
notion db query <database_id>
```

### Query with filter

```bash
notion db query <database_id> --filter "Status=Done"
notion db query <database_id> --filter "Priority=High,Status=Open"
```

### Query with limit

```bash
notion db query <database_id> --limit 50
```

### Insert new entry

```bash
notion db insert <database_id> --title "New Item" --properties "Status=Open"
```

### Insert with multiple properties

```bash
notion db insert <database_id> --title "Complex Task" --properties "Status=Open,Priority=High,Tags=urgent,important"
```

---

## Page Operations

### Create page

```bash
notion page create --parent <parent_id> --title "New Page"
```

### Create page and get ID

```bash
PAGE_ID=$(notion page create --parent <parent_id> --title "New Page" --json | jq -r '.data.id')
```

### Append markdown content

```bash
notion page append <page_id> --content "## Section\n\nContent here"
```

### Append multi-line content

```bash
notion page append <page_id> --content "## Heading 1

Paragraph with **bold** and *italic* text.

### Subheading

- Bullet 1
- Bullet 2
- Bullet 3"
```

### Update page title

```bash
notion page update <page_id> --title "New Title"
```

### Update properties

```bash
notion page update <page_id> --properties "Status=Done"
```

### Archive page

```bash
notion page archive <page_id>
```

### Unarchive page

```bash
notion page archive <page_id> --unarchive
```

---

## Chaining Commands

### Find database and query it

```bash
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id') && \
notion db query "$DB_ID" --filter "Status=Open"
```

### Create page and add content

```bash
PAGE_ID=$(notion page create --parent <parent_id> --title "Meeting Notes" --json | jq -r '.data.id') && \
notion page append "$PAGE_ID" --content "## Attendees\n\n- Alice\n- Bob\n- Carol"
```

### Create task and mark urgent

```bash
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id') && \
TASK_ID=$(notion db insert "$DB_ID" --title "Urgent Bug" --json | jq -r '.data.id') && \
notion page update "$TASK_ID" --properties "Priority=High,Status=Open"
```

### Export database to JSON

```bash
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id') && \
notion db query "$DB_ID" --json > tasks_export.json
```

### Find and archive old pages

```bash
notion search "old project" --json | jq -r '.data[].id' | while read -r page_id; do
    notion page archive "$page_id"
done
```

---

## JSON Output Examples

### Pretty print search results

```bash
notion search "meeting" --json | jq '.data[] | {title, type, url}'
```

### Extract just IDs

```bash
notion db query <database_id> --json | jq -r '.data[].id'
```

### Filter by property value

```bash
notion db query <database_id> --json | jq '.data[] | select(.properties.Status.value == "Done")'
```

### Count results

```bash
notion db query <database_id> --json | jq '.data | length'
```

---

*See [WORKFLOWS.md](WORKFLOWS.md) for complete task-oriented guides.*
