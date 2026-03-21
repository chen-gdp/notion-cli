# Workflows

Task-oriented guides for common Notion CLI use cases.

## Table of Contents

- [Task Management Workflow](#task-management-workflow)
- [Documentation Workflow](#documentation-workflow)
- [Research Notes Workflow](#research-notes-workflow)
- [Meeting Notes Workflow](#meeting-notes-workflow)
- [Project Tracking Workflow](#project-tracking-workflow)
- [Content Publishing Workflow](#content-publishing-workflow)

---

## Task Management Workflow

Complete workflow for managing tasks in Notion.

### Setup

1. **Find or create a Tasks database**

```bash
# Search for existing tasks database
notion search "Tasks" --type database

# If not found, create one in your workspace manually
# Then get the database ID
DB_ID=$(notion search "Tasks" --type database --json | jq -r '.data[0].id')
```

2. **View database schema**

```bash
notion db get "$DB_ID"
```

### Daily Workflow

**Morning - Review open tasks:**

```bash
# List all open tasks
notion db query "$DB_ID" --filter "Status=Open"

# List high priority tasks
notion db query "$DB_ID" --filter "Status=Open,Priority=High"
```

**Create new tasks:**

```bash
# Quick task
notion db insert "$DB_ID" --title "Review PR #123"

# Detailed task
notion db insert "$DB_ID" --title "Implement feature X" --properties "Status=Open,Priority=High,Due Date=2024-03-25"

# Task with tags
notion db insert "$DB_ID" --title "Fix bug" --properties "Status=Open,Priority=Medium,Tags=bug,urgent"
```

**Update task status:**

```bash
# Get task ID
TASK_ID=$(notion db query "$DB_ID" --filter "Title=Review PR #123" --json | jq -r '.data[0].id')

# Mark as in progress
notion page update "$TASK_ID" --properties "Status=In Progress"

# Mark as done
notion page update "$TASK_ID" --properties "Status=Done"
```

**End of day - Archive completed:**

```bash
# Find all done tasks
for task_id in $(notion db query "$DB_ID" --filter "Status=Done" --json | jq -r '.data[].id'); do
    notion page archive "$task_id"
done
```

### Advanced Task Management

**Bulk operations:**

```bash
# Update all open bugs to high priority
for task_id in $(notion db query "$DB_ID" --filter "Status=Open,Tags=bug" --json | jq -r '.data[].id'); do
    notion page update "$task_id" --properties "Priority=High"
done
```

**Export tasks:**

```bash
# Export to JSON for reporting
notion db query "$DB_ID" --filter "Status=Open" --json > open_tasks.json

# Count by status
notion db query "$DB_ID" --json | jq -r '.data[].properties.Status.value' | sort | uniq -c
```

---

## Documentation Workflow

Creating and maintaining documentation in Notion.

### Setup

1. **Create a documentation hub**

```bash
# Find your wiki or docs page
WIKI_ID=$(notion search "Documentation" --type page --json | jq -r '.data[0].id')

# Or create a new docs page
WIKI_ID=$(notion page create --parent <workspace_id> --title "Team Documentation" --json | jq -r '.data.id')
```

### Creating Documentation

**Create a new doc:**

```bash
# Create the page
PAGE_ID=$(notion page create --parent "$WIKI_ID" --title "API Reference" --json | jq -r '.data.id')

# Add header and overview
notion page append "$PAGE_ID" --content "# API Reference

This document describes the REST API endpoints."
```

**Add structured content:**

```bash
# Add endpoint documentation
notion page append "$PAGE_ID" --content "## GET /users

Retrieve a list of users.

**Parameters:**
- `limit` (optional): Maximum number of users
- `offset` (optional): Pagination offset

**Response:**
\`\`\`json
{
  \"users\": [...],
  \"total\": 100
}
\`\`\`"
```

**Add code examples:**

```bash
notion page append "$PAGE_ID" --content "## Examples

### cURL

\`\`\`bash
curl -H \"Authorization: Bearer TOKEN\" \\
  https://api.example.com/users
\`\`\`

### Python

\`\`\`python
import requests

response = requests.get('https://api.example.com/users')
users = response.json()
\`\`\`"
```

**Add todo list for tracking:**

```bash
notion page append "$PAGE_ID" --content "## TODO

- [ ] Add authentication section
- [ ] Document error codes
- [ ] Add rate limiting info
- [ ] Review with team"
```

### Maintaining Documentation

**Update existing docs:**

```bash
# Find the page
PAGE_ID=$(notion search "API Reference" --type page --json | jq -r '.data[0].id')

# Update title
notion page update "$PAGE_ID" --title "API Reference v2"

# Append new section
notion page append "$PAGE_ID" --content "## Changelog

### v2.0
- Added new endpoints
- Updated authentication"
```

**Archive outdated docs:**

```bash
# Find old documentation
OLD_PAGE=$(notion search "API v1" --type page --json | jq -r '.data[0].id')

# Archive it
notion page archive "$OLD_PAGE"
```

---

## Research Notes Workflow

Collecting and organizing research in Notion.

### Setup

1. **Create a research database or page**

```bash
# Find existing research database
RESEARCH_DB=$(notion search "Research" --type database --json | jq -r '.data[0].id')

# Or create a research page
RESEARCH_ID=$(notion page create --parent <workspace_id> --title "Research Notes" --json | jq -r '.data.id')
```

### Conducting Research

**Create a new research note:**

```bash
# Create the note
NOTE_ID=$(notion page create --parent "$RESEARCH_ID" --title "Competitor Analysis Q2" --json | jq -r '.data.id')

# Add initial structure
notion page append "$NOTE_ID" --content "# Competitor Analysis Q2

**Date:** $(date +%Y-%m-%d)
**Researcher:** $(whoami)

## Objectives

- Identify key competitors
- Analyze pricing strategies
- Document feature gaps"
```

**Add findings incrementally:**

```bash
# Competitor A
notion page append "$NOTE_ID" --content "## Competitor A

**Website:** https://competitor-a.com

**Strengths:**
- Fast performance
- Good UX
- Strong brand

**Weaknesses:**
- Expensive
- Limited API

**Pricing:** $99/month"
```

```bash
# Competitor B
notion page append "$NOTE_ID" --content "## Competitor B

**Website:** https://competitor-b.com

**Strengths:**
- Free tier
- Open source
- Active community

**Weaknesses:**
- Complex setup
- Limited support

**Pricing:** Freemium"
```

**Add comparison table:**

```bash
notion page append "$NOTE_ID" --content "## Comparison Matrix

| Feature | Us | Competitor A | Competitor B |
|---------|---|--------------|--------------|
| Price | $49 | $99 | Free/$29 |
| API | Yes | Limited | Yes |
| Support | 24/7 | Business hours | Community |
| Setup | Easy | Medium | Complex |"
```

**Add action items:**

```bash
notion page append "$NOTE_ID" --content "## Action Items

- [ ] Review pricing strategy
- [ ] Improve onboarding flow
- [ ] Add missing features: X, Y, Z
- [ ] Schedule competitive review meeting"
```

### Organizing Research

**Tag and categorize:**

```bash
# If using a database with tags
notion db insert "$RESEARCH_DB" --title "Competitor Analysis Q2" --properties "Type=Competitor,Status=Complete,Priority=High"
```

**Link related notes:**

```bash
# Add references to other research
notion page append "$NOTE_ID" --content "## Related Research

- [Previous Q1 Analysis](https://notion.so/...)
- [Market Trends 2024](https://notion.so/...)"
```

---

## Meeting Notes Workflow

Taking and sharing meeting notes in Notion.

### Before the Meeting

**Create meeting notes page:**

```bash
# Find or create meetings database
MEETINGS_DB=$(notion search "Meetings" --type database --json | jq -r '.data[0].id')

# Create meeting entry
MEETING_ID=$(notion db insert "$MEETINGS_DB" --title "Weekly Standup - $(date +%Y-%m-%d)" --properties "Type=Standup,Status=Scheduled" --json | jq -r '.data.id')

# Add template
notion page append "$MEETING_ID" --content "# Weekly Standup - $(date +%Y-%m-%d)

**Date:** $(date +%Y-%m-%d)
**Time:** 10:00 AM
**Attendees:**
- [ ] Alice
- [ ] Bob
- [ ] Carol

## Agenda

1. Review last week's goals
2. Current blockers
3. This week's priorities

## Notes

## Action Items

- [ ]"
```

### During the Meeting

**Take notes:**

```bash
# Add discussion points
notion page append "$MEETING_ID" --content "## Discussion

**Alice:** Completed user authentication feature
**Bob:** Working on API integration, blocked by API rate limits
**Carol:** Design review scheduled for Friday"
```

**Track action items:**

```bash
notion page append "$MEETING_ID" --content "## Action Items

- [ ] Bob to contact API team about rate limits - Due Friday
- [ ] Alice to deploy auth feature to staging - Due Today
- [ ] Carol to share design mockups - Due Wednesday
- [ ] Schedule API architecture review - Owner: Alice"
```

### After the Meeting

**Update status:**

```bash
# Mark as complete
notion page update "$MEETING_ID" --properties "Status=Completed"
```

**Share with attendees:**

```bash
# Get the URL
notion get "$MEETING_ID" --json | jq -r '.data.url'
# Share this URL with the team
```

---

## Project Tracking Workflow

Tracking project progress in Notion.

### Setup

1. **Create project database**

```bash
PROJECTS_DB=$(notion search "Projects" --type database --json | jq -r '.data[0].id')
```

### Project Lifecycle

**Create new project:**

```bash
PROJECT_ID=$(notion db insert "$PROJECTS_DB" --title "Website Redesign" --properties "Status=Planning,Priority=High,Lead=Alice" --json | jq -r '.data.id')

# Create project page
notion page append "$PROJECT_ID" --content "# Website Redesign

## Overview
Complete redesign of company website with new branding.

## Goals
- Improve conversion rate by 20%
- Reduce page load time to <2s
- Mobile-first design

## Timeline
- Design: Week 1-2
- Development: Week 3-6
- Testing: Week 7
- Launch: Week 8

## Resources
- Designer: Carol
- Developer: Bob
- PM: Alice"
```

**Track milestones:**

```bash
notion page append "$PROJECT_ID" --content "## Milestones

- [x] Project kickoff
- [x] Requirements gathering
- [ ] Design approval - Due: 2024-03-25
- [ ] Development start - Due: 2024-04-01
- [ ] QA complete - Due: 2024-04-30
- [ ] Launch - Due: 2024-05-01"
```

**Update progress:**

```bash
# Move to in progress
notion page update "$PROJECT_ID" --properties "Status=In Progress"

# Update milestone
notion page append "$PROJECT_ID" --content "## Update $(date +%Y-%m-%d)

Design phase complete. Approved by stakeholders."
```

**Weekly status updates:**

```bash
notion page append "$PROJECT_ID" --content "## Week of $(date +%Y-%m-%d)

**Completed:**
- Homepage mockups
- Mobile responsive design

**In Progress:**
- Component library
- Style guide

**Blockers:**
- Waiting for brand assets from marketing

**Next Week:**
- Start development sprint 1"
```

---

## Content Publishing Workflow

Publishing content to Notion.

### Setup

1. **Create content calendar or database**

```bash
CONTENT_DB=$(notion search "Content" --type database --json | jq -r '.data[0].id')
```

### Content Creation

**Create content entry:**

```bash
CONTENT_ID=$(notion db insert "$CONTENT_DB" --title "Getting Started Guide" --properties "Status=Draft,Type=Blog,Author=Alice" --json | jq -r '.data.id')
```

**Write content:**

```bash
notion page append "$CONTENT_ID" --content "# Getting Started with Our Product

## Introduction

Welcome! This guide will help you get up and running in minutes.

## Quick Start

### Step 1: Sign Up

Create your account at https://example.com/signup

### Step 2: Configure Settings

Navigate to Settings and configure:
- Profile information
- Notification preferences
- Integration settings

### Step 3: Create Your First Project

Click \"New Project\" and follow the wizard.

## Next Steps

- Read the [API documentation](...)
- Join our [community forum](...)
- Contact [support](...) if you need help"
```

**Add media placeholders:**

```bash
notion page append "$CONTENT_ID" --content "## Screenshots

[Add screenshot: Sign up page]

[Add screenshot: Dashboard]

[Add screenshot: Project creation]"
```

### Review Process

**Submit for review:**

```bash
notion page update "$CONTENT_ID" --properties "Status=Review"
```

**Add review feedback:**

```bash
notion page append "$CONTENT_ID" --content "## Review Feedback

**Reviewer:** Bob
**Date:** $(date +%Y-%m-%d)

- [ ] Add more screenshots
- [ ] Clarify Step 2
- [ ] Fix broken link to API docs
- [ ] Add troubleshooting section"
```

**Publish:**

```bash
notion page update "$CONTENT_ID" --properties "Status=Published"
notion page append "$CONTENT_ID" --content "---

**Published:** $(date +%Y-%m-%d)
**URL:** https://blog.example.com/getting-started"
```

---

*See [EXAMPLES.md](EXAMPLES.md) for more command patterns.*
