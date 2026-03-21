# Notion CLI Roadmap

## Overview

This roadmap maps features to milestones, where each milestone represents a complete use case (success criteria). Each milestone contains 1 or more feature specifications.

---

## Milestone 1: Task & Issue Tracker ⭐ (MVP Core)

**Success Criteria:** Agent can query tasks by status/priority, create new tasks, and update task statuses.

**User Story:** "What high priority bugs are assigned to me? Mark the auth bug as fixed."

### Feature Specs

#### Spec 1.0: Authentication Setup
- `notion auth setup` — Interactive setup, saves token to config
- `notion auth status` — Show auth status and config location
- `notion auth logout` — Remove saved token
- `notion config` — Show configuration file path and contents

**Deliverable:** User can authenticate and manage credentials.

#### Spec 1.1: Core Discovery Commands
- `notion search <query>` — Search pages/databases
- `notion get <id>` — Get page/database details
- `notion skills list` — List available commands
- `notion skills show <name>` — Show command details

**Deliverable:** Agent can discover resources and understand CLI capabilities.

#### Spec 1.2: Database Query Command
- `notion db get <id>` — Get database schema
- `notion db query <id> --filter <criteria> --limit <n>` — Query with filters

**Filter Syntax (MVP):** Simple key=value pairs only
```bash
notion db query bugs-db --filter "priority=High,status=In Progress" --limit 10
```

**Deliverable:** Agent can find databases and query entries by properties.

#### Spec 1.3: Database Insert Command
- `notion db insert <db_id> --title <title> --properties <props>`

```bash
notion db insert bugs-db --title "Auth bug" --properties "priority=High,status=Open"
```

**Deliverable:** Agent can create new database entries with properties.

#### Spec 1.4: Page Update Command
- `notion page update <id> --title <title>` — Update page title
- `notion page update <id> --properties <props>` — Update properties
- `notion page archive <id> [--unarchive]` — Archive/unarchive

```bash
notion page update task-123 --properties "status=Done"
```

**Deliverable:** Agent can update task statuses and archive completed work.

---

## Milestone 2: Documentation Maintainer

**Success Criteria:** Agent can create structured documentation with rich content (code blocks, headings, lists).

**User Story:** "Create an API troubleshooting guide with common issues and code examples."

### Feature Specs

#### Spec 2.1: Page Creation Command
- `notion page create --parent <id> --title <title> [--properties <props>]`

```bash
notion page create --parent wiki-456 --title "API Troubleshooting"
```

**Deliverable:** Agent can create standalone pages (not just DB entries).

#### Spec 2.2: Page Append with Markdown
- `notion page append <id> --content <markdown>` — Support rich markdown

**Markdown Elements to Support:**
- Headings (`## Heading`)
- Lists (`- item`, `1. item`)
- Code blocks (```language ... ```)
- Todo/checkbox (`- [ ] task`)
- Bold/italic (`**bold**`, `*italic*`)
- Links (`[text](url)`)

```bash
notion page append page-123 --content "## Common Issues

### 401 Error
Check your token.

\`\`\`python
headers = {'Authorization': f'Bearer {token}'}
\`\`\`

- [ ] Verify token
- [ ] Check expiration"
```

**Deliverable:** Agent can add structured content with code blocks and todos.

---

## Milestone 3: Research & Notes Organizer

**Success Criteria:** Agent can detect duplicates, create research pages, and incrementally add findings.

**User Story:** "Research competitors for our API product and organize findings."

### Feature Specs

#### Spec 3.1: Enhanced Search with Metadata
- `notion search <query> --type <page|database>` — Filter by type
- Returns last_edited_time for duplicate detection

```bash
notion search "competitor" --type page
# Returns results with timestamps for age detection
```

**Deliverable:** Agent can find existing content and detect outdated research.

#### Spec 3.2: Content Update Workflow
- Combination of `page get` + `page append` for incremental updates
- `notion page append` supports appending to any existing page

**Deliverable:** Agent can build research incrementally over multiple sessions.

---

## Post-MVP Roadmap

### Phase 2: Advanced Filtering & Querying

**Milestone 4: Complex Task Management**

**Gap:** Current filters only support simple equality (`key=value`).

**Specs:**
- Spec 4.1: Multi-criteria filters with AND/OR
  - `--filter "priority=High AND status!=Done"`
- Spec 4.2: Date operators
  - `--filter "due_date<2026-03-30"`
  - `--filter "due_date=<TOMORROW>"` (date helpers)
- Spec 4.3: Sort and pagination
  - `--sort "due_date:asc"`
  - `--cursor <token>` for pagination

**Deliverable:** Agent can do complex queries like "High priority tasks due this week that aren't done."

---

### Phase 3: Content Management

**Milestone 5: Rich Content Operations**

**Gap:** No block-level operations or templates.

**Specs:**
- Spec 5.1: Block operations
  - `notion block get <id>` — Get block content
  - `notion block delete <id>` — Delete specific blocks
  - `notion block update <id> --content <text>` — Update block
- Spec 5.2: Template system
  - `--template <name>` flag for `page append`
  - Templates stored in `.notion-cli/templates/`
- Spec 5.3: Link resolution
  - Support `[[Page Title]]` syntax in markdown
  - Auto-convert to Notion page mentions

**Deliverable:** Agent can manage content at block level and use templates.

---

### Phase 4: Automation & Export

**Milestone 6: Advanced Workflows**

**Gap:** No batch operations or export capabilities.

**Specs:**
- Spec 6.1: Bulk operations
  - `notion bulk update --filter "status=Done" --set "archived=true"`
- Spec 6.2: Export commands
  - `notion export <id> --format markdown`
  - `notion export <id> --format html`
- Spec 6.3: File attachments (leverage existing `uno upload`)
  - Integration with the existing upload functionality
- Spec 6.4: Comments
  - `notion comment list <page_id>`
  - `notion comment add <page_id> --content <text>`

**Deliverable:** Agent can do batch operations and export content.

---

## Feature Dependency Graph

```
Milestone 1 (Task Tracker)
├── Spec 1.1: search, get, skills [FOUNDATION]
├── Spec 1.2: db query
├── Spec 1.3: db insert
└── Spec 1.4: page update, archive

Milestone 2 (Documentation)
├── Spec 2.1: page create [DEPENDS: 1.1]
└── Spec 2.2: page append with markdown [DEPENDS: 2.1]

Milestone 3 (Research)
├── Spec 3.1: enhanced search [DEPENDS: 1.1]
└── Spec 3.2: incremental append [DEPENDS: 2.2]

Post-MVP
├── Phase 2: Complex filters [DEPENDS: 1.2]
├── Phase 3: Block ops, templates [DEPENDS: 2.2]
└── Phase 4: Bulk, export [DEPENDS: Phase 2, 3]
```

---

## Implementation Priority

### Sprint 1: Foundation (Week 1)
- Spec 1.1: Core discovery (search, get, skills)
- Setup project structure, vendoring ultimate-notion
- JSON output framework
- SKILLS.md generation

### Sprint 2: Database Operations (Week 2)
- Spec 1.2: db get, db query
- Spec 1.3: db insert
- Spec 1.4: page update, archive

**Milestone 1 Complete** ✅ Task Tracker works end-to-end

### Sprint 3: Content Creation (Week 3)
- Spec 2.1: page create
- Spec 2.2: page append with markdown parser
- Rich text conversion (markdown → Notion blocks)

**Milestone 2 Complete** ✅ Documentation Maintainer works

### Sprint 4: Polish & Research (Week 4)
- Spec 3.1: enhanced search
- Spec 3.2: incremental workflow support
- Error handling improvements
- Documentation

**Milestone 3 Complete** ✅ Research Organizer works

**MVP v1.0.0 Released** 🎉

---

## Success Metrics per Milestone

| Milestone | Test Scenario | Pass Criteria |
|-----------|---------------|-----------------|
| 1 (Tasks) | "Show my open high priority bugs" | Returns filtered list from Bugs DB |
| 1 (Tasks) | "Mark bug #123 as fixed" | Updates status, returns success |
| 2 (Docs) | "Create API guide with code block" | Page created with formatted code block |
| 2 (Docs) | "Add troubleshooting section" | Appends heading + list to existing page |
| 3 (Research) | "Research competitors" | Finds old research, asks for decision, creates new page |
| 3 (Research) | "Add Competitor C findings" | Appends to existing research page |

---

## Roadmap Changes Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-03-20 | Initial roadmap | Based on use case analysis |
| TBD | Filter operators moved to Post-MVP | Simple filters sufficient for MVP use cases |
| TBD | Block commands deferred | Not needed for priority use cases |

---

## Open Questions

1. **Date helpers** (`<TODAY>`, `<TOMORROW>`): Sprint 1 or Post-MVP?
2. **Template system**: Hardcoded in agent or CLI feature?
3. **Bulk operations**: Phase 4 or agent-side loop?
4. **Export formats**: Phase 4 or use Notion's built-in export?
