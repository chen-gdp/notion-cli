# Agent Use Cases with Notion CLI

What an AI agent (OpenClaw) can accomplish with the 11 MVP commands.

---

## Use Case 1: Intelligent Meeting Assistant

**Capabilities:**
- Search for existing meeting notes by date/topic
- Create new meeting pages in the correct database
- Append structured notes with action items (todo blocks)
- Update meeting status (in progress → done)
- Query for follow-up tasks from previous meetings

**Example Workflow:**
```
User: "Schedule a design review for tomorrow and add it to the calendar"

Agent:
1. search "Design Reviews" --type database → finds Design Reviews DB
2. db get <db_id> → sees it has Date, Attendees, Status fields
3. db insert <db_id> --title "Design Review - March 21" --properties "Date=2026-03-21,Status=Scheduled"
4. page append <new_page_id> --content "## Agenda\n- [ ] Review mockups\n- [ ] Discuss timeline"

Result: Meeting scheduled with template and agenda
```

---

## Use Case 2: Project Status Reporter

**Capabilities:**
- Query project database for all active projects
- Get detailed info on each project page
- Summarize status across multiple projects
- Update project statuses based on user input
- Archive completed projects

**Example Workflow:**
```
User: "Give me a summary of all projects due this quarter"

Agent:
1. search "Projects" --type database → finds Projects DB
2. db query <db_id> --filter "Due Date<2026-06-30" --json
3. For each project:
   - get <project_id> --json → extracts status, owner, completion %
4. Compiles summary table

Result: Executive summary of Q2 projects with status and risks
```

---

## Use Case 3: Documentation Maintainer

**Capabilities:**
- Search for outdated documentation
- Create new docs with consistent structure
- Append sections to existing docs
- Update doc properties (last reviewed date, owner)
- Archive obsolete docs

**Example Workflow:**
```
User: "Create a troubleshooting guide for the API"

Agent:
1. search "Troubleshooting" → check if exists
2. search "API Documentation" --type database → finds API Docs DB
3. db insert <db_id> --title "API Troubleshooting Guide" --properties "Category=Reference"
4. page append <page_id> --content "## Common Issues\n\n### 401 Unauthorized\n...\n\n### Rate Limiting\n..."

Result: Searchable troubleshooting guide in the right location
```

---

## Use Case 4: Task & Issue Tracker

**Capabilities:**
- Query tasks by status, priority, assignee
- Create new tasks with proper categorization
- Update task status as work progresses
- Archive completed tasks
- Link tasks to related pages

**Example Workflow:**
```
User: "What high priority bugs are assigned to me?"

Agent:
1. search "Bugs" --type database → finds Bugs DB
2. db get <db_id> → sees schema (Assignee, Priority, Status)
3. db query <db_id> --filter "Priority=High,Assignee=User,Status!=Done" --json
4. Formats results with links

User: "Mark the auth bug as fixed"
Agent:
5. page update <auth_bug_id> --properties "Status=Fixed" --json
```

---

## Use Case 5: Knowledge Base Curator

**Capabilities:**
- Search for related pages when answering questions
- Create FAQ pages from common queries
- Organize content with proper tagging
- Update existing pages with new information
- Cross-reference related documents

**Example Workflow:**
```
User: "How do I set up the dev environment? I couldn't find it"

Agent:
1. search "setup" → finds partial matches
2. search "environment" → finds "Environment Setup" page (outdated)
3. page get <page_id> → sees last edited 6 months ago
4. "The existing doc is outdated. Should I update it or create a new one?"

User: "Update it"
Agent:
5. page append <page_id> --content "## 2026 Update\nNew Docker-based setup:\n\n```bash\ndocker-compose up -d\n```"
6. page update <page_id> --properties "Last Reviewed=2026-03-20"
```

---

## Use Case 6: Sprint/Iteration Manager

**Capabilities:**
- Create sprint planning pages
- Query backlog for unestimated items
- Update story points and sprint assignments
- Generate sprint reports from database queries
- Archive old sprint pages

**Example Workflow:**
```
User: "Start sprint 15 with the top 5 backlog items"

Agent:
1. search "Sprints" --type database → finds Sprints DB
2. db insert <db_id> --title "Sprint 15" --properties "Status=Planning,Start Date=2026-03-24"
3. search "Backlog" --type database → finds Backlog DB
4. db query <backlog_id> --filter "Status=Backlog,Sprint=Unassigned" --limit 5 --json
5. For each item:
   - page update <item_id> --properties "Sprint=Sprint 15"
6. page append <sprint_page> --content "## Sprint Goals\n...\n\n## Committed Items\n..."

Result: Sprint 15 created with 5 committed items
```

---

## Use Case 7: Content Calendar Manager

**Capabilities:**
- Query content calendar by date range
- Create new content items with deadlines
- Update publish status
- Archive old content ideas
- Append performance metrics after publishing

**Example Workflow:**
```
User: "What's publishing next week?"

Agent:
1. search "Content Calendar" --type database
2. db query <db_id> --filter "Publish Date>=2026-03-24,Publish Date<=2026-03-31,Status=Scheduled" --json
3. Formats content pipeline

User: "Add a blog post about Python tips for next Wednesday"
Agent:
4. db insert <db_id> --title "10 Python Tips for Clean Code" --properties "Type=Blog,Publish Date=2026-03-26,Status=Draft,Owner=User"
5. page append <page_id> --content "# 10 Python Tips\n\n## 1. Use list comprehensions..."
```

---

## Use Case 8: HR/Onboarding Automation

**Capabilities:**
- Create structured onboarding checklists
- Query employee database
- Update onboarding progress
- Archive completed onboarding
- Generate onboarding reports

**Example Workflow:**
```
User: "Start onboarding for Jane who starts Monday"

Agent:
1. search "Onboarding" --type database → finds Onboarding DB
2. db get <db_id> → sees fields: Name, Start Date, Buddy, Checklist
3. db insert <db_id> --title "Jane Doe - Onboarding" --properties "Start Date=2026-03-24,Buddy=Alice,Status=In Progress"
4. page append <page_id> --content "## Week 1 Checklist\n- [ ] Laptop setup\n- [ ] Slack access\n- [ ] Repo access\n\n## Resources\n- [Employee Handbook]\n- [Team Directory]"

Result: Complete onboarding page with checklist and resources
```

---

## Use Case 9: Research & Notes Organizer

**Capabilities:**
- Search across all notes for related content
- Create new research pages with sources
- Append findings as research progresses
- Link related pages together
- Archive obsolete research

**Example Workflow:**
```
User: "I need to research competitors for our API product"

Agent:
1. search "competitor" → finds old research from 2024
2. "Found competitor research from 2024. Should I update it or start fresh?"

User: "Start fresh"
Agent:
3. search "Research" --type database → finds Research DB
4. db insert <db_id> --title "API Competitor Analysis 2026" --properties "Topic=Competitors,Status=Active"
5. page append <page_id> --content "## Competitors\n\n### Competitor A\n- Strengths: ...\n- Weaknesses: ...\n\n### Competitor B\n..."

Result: Structured competitor analysis with room for ongoing updates
```

---

## Use Case 10: Daily Standup Facilitator

**Capabilities:**
- Query yesterday's completed tasks
- Query today's planned tasks
- Query blocked tasks
- Append standup notes to team page
- Update task statuses

**Example Workflow:**
```
User: "Run standup for the backend team"

Agent:
1. search "Backend Tasks" --type database → finds Backend Tasks DB
2. db query <db_id> --filter "Status=Done,Updated Yesterday" --json → Yesterday's completions
3. db query <db_id> --filter "Status=In Progress" --json → Today's work
4. db query <db_id> --filter "Status=Blocked" --json → Blockers
5. search "Standup Notes" → finds team standup page
6. page append <standup_page> --content "## Backend Team - March 20\n\n**Yesterday:**\n- ...\n\n**Today:**\n- ...\n\n**Blockers:**\n- ..."

Result: Standup notes compiled and documented
```

---

## What the Agent CANNOT Do (MVP Limitations)

1. **Upload files** - Can't attach PDFs, images (use existing `uno upload`)
2. **Create databases** - Can only insert into existing DBs
3. **Complex filters** - No AND/OR logic in queries
4. **Move pages** - Can't change parent of existing page
5. **Delete content** - Can only archive, not delete
6. **Batch operations** - Must update items one at a time
7. **Export formats** - No HTML/PDF export (markdown only via blocks)
8. **Comments** - Can't read or add page comments
9. **Permissions** - Can't share pages or manage access
10. **Webhooks** - No real-time notifications

---

## Key Value Propositions

**For Developers:**
- Query bug databases and update statuses
- Create structured documentation with code blocks
- Manage sprint backlogs and generate reports

**For Managers:**
- Query project status across teams
- Generate executive summaries from database
- Track onboarding progress

**For Writers/Content Creators:**
- Manage editorial calendars
- Create structured articles with rich formatting
- Query content performance

**For Operations:**
- Maintain process documentation
- Track task completion across teams
- Create standardized templates

---

## Design Implications

These use cases reveal the CLI needs:

1. **Markdown parsing** - Critical for rich content (tables, code, lists)
2. **Flexible property setting** - Different DBs have different schemas
3. **Date handling** - Queries often need date ranges
4. **Pagination** - Large databases need cursor support
5. **Link resolution** - Mentioning other pages in content
6. **Template support** - Predefined content structures

The 11 commands are actually quite powerful when combined intelligently by an agent.
