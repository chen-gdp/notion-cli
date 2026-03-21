# Notion CLI Specification

## Project Overview

A command-line interface for Notion, designed for AI agents (OpenClaw) to interact with Notion workspaces programmatically. Built on top of the `ultimate-notion` Python library.

## Success Criteria

1. **AI-Agent Friendly**: All commands support `--json` output for machine parsing
2. **Self-Documenting**: SKILLS.md auto-generated from CLI commands
3. **MVP Ready**: Core CRUD operations for pages, databases, and blocks
4. **Tested**: Unit tests for all commands
5. **Installable**: Single `pip install` from GitHub

---

## User Stories

### Story 1: AI Agent Queries Notion
**As an** AI agent (OpenClaw)  
**I want to** search for pages and databases  
**So that** I can find relevant content to work with

**Acceptance Criteria:**
- Search by title with partial matching
- Filter by type (page/database)
- Return results as JSON for parsing
- Show basic metadata (title, ID, URL, last edited)

### Story 2: AI Agent Creates Content
**As an** AI agent  
**I want to** create pages and append blocks  
**So that** I can add new content to Notion

**Acceptance Criteria:**
- Create page in a database or as child of another page
- Append text, headings, lists, code blocks
- Support markdown input for rich text
- Return created object ID

### Story 3: AI Agent Reads Content
**As an** AI agent  
**I want to** read page content and database rows  
**So that** I can understand existing information

**Acceptance Criteria:**
- Get page content as structured blocks
- Query database with filters
- Export to markdown for processing
- Handle pagination for large datasets

### Story 4: AI Agent Updates Content
**As an** AI agent  
**I want to** update page properties and block content  
**So that** I can modify existing information

**Acceptance Criteria:**
- Update page properties (title, custom properties)
- Update block content
- Archive/unarchive pages

### Story 5: AI Agent Discovers Capabilities
**As an** AI agent  
**I want to** discover available CLI commands  
**So that** I know what operations are possible

**Acceptance Criteria:**
- `skills list` command shows all available skills
- `skills show <skill>` shows detailed usage
- SKILLS.md file in repo root for documentation
- Each skill has description, parameters, examples

---

## Functional Requirements (EARS Format)

### Search & Discovery

**WHEN** the user runs `notion search <query>`  
**THE SYSTEM SHALL** return matching pages and databases  
**AND** support `--type page|database` filtering  
**AND** support `--json` for machine-readable output

**WHEN** the user runs `notion get <page_id>`  
**THE SYSTEM SHALL** retrieve the page with all properties  
**AND** optionally include block content with `--blocks`

**WHEN** the user runs `notion db get <database_id>`  
**THE SYSTEM SHALL** retrieve the database schema  
**AND** show all properties and their types

### Content Creation

**WHEN** the user runs `notion page create --parent <id> --title <title>`  
**THE SYSTEM SHALL** create a new page  
**AND** support `--properties` for custom property values  
**AND** return the created page ID

**WHEN** the user runs `notion page append <page_id> --content <content>`  
**THE SYSTEM SHALL** append blocks to the page  
**AND** support markdown parsing for rich text  
**AND** auto-detect block types (heading, list, code, etc.)

**WHEN** the user runs `notion db query <database_id>`  
**THE SYSTEM SHALL** query the database  
**AND** support `--filter` for property-based filtering  
**AND** support `--sort` for sorting results

### Content Updates

**WHEN** the user runs `notion page update <page_id> --title <title>`  
**THE SYSTEM SHALL** update the page title  
**AND** support updating custom properties with `--properties`

**WHEN** the user runs `notion page archive <page_id>`  
**THE SYSTEM SHALL** archive the page  
**AND** support `--unarchive` to restore

### Skills System

**WHEN** the user runs `notion skills list`  
**THE SYSTEM SHALL** display all available skills/commands  
**AND** show name, description, and category for each

**WHEN** the user runs `notion skills show <skill_name>`  
**THE SYSTEM SHALL** display detailed information  
**AND** include description, parameters, examples, and return format

**WHEN** the CLI is built/installed  
**THE SYSTEM SHALL** generate SKILLS.md  
**AND** include all commands with full documentation

---

## CLI Command Inventory

### Core Commands

| Command | Description | Priority |
|---------|-------------|----------|
| `notion search <query>` | Search pages and databases | MVP |
| `notion get <id>` | Get page/database by ID | MVP |
| `notion page create` | Create a new page | MVP |
| `notion page append <id>` | Append blocks to page | MVP |
| `notion page update <id>` | Update page properties | MVP |
| `notion page archive <id>` | Archive/unarchive page | MVP |
| `notion db get <id>` | Get database schema | MVP |
| `notion db query <id>` | Query database entries | MVP |
| `notion db insert <id>` | Insert row into database | MVP |
| `notion block get <id>` | Get block content | MVP |
| `notion block delete <id>` | Delete block | MVP |

### Skills Commands

| Command | Description | Priority |
|---------|-------------|----------|
| `notion skills list` | List all skills | MVP |
| `notion skills show <name>` | Show skill details | MVP |
| `notion skills export` | Export skills to JSON | Post-MVP |

### Utility Commands

| Command | Description | Priority |
|---------|-------------|----------|
| `notion config` | Show configuration | MVP |
| `notion auth setup` | Authenticate with Notion (saves token) | **MVP** |
| `notion auth status` | Check authentication status | **MVP** |
| `notion auth logout` | Remove saved token | **MVP** |
| `notion export <id>` | Export to markdown/HTML | Post-MVP |

---

## SKILLS.md Format

The SKILLS.md file follows the Claude Code skills format:

```markdown
# Notion CLI Skills

## Skill: search

Search for pages and databases in Notion.

### Usage

```bash
notion search <query> [options]
```

### Parameters

- `query` (required): Search query string
- `--type`: Filter by type (`page` or `database`)
- `--limit`: Maximum results (default: 100)
- `--json`: Output as JSON

### Examples

```bash
# Search for pages about "meeting"
notion search "meeting" --type page

# Get JSON output for AI processing
notion search "project" --json
```

### Returns

List of objects with:
- `id`: Page/database ID
- `title`: Object title
- `type`: `page` or `database`
- `url`: Notion URL
- `last_edited_time`: ISO timestamp

---

## Skill: page_create

Create a new page in Notion.

...
```

---

## MVP Scope

### In Scope (MVP)

1. **Search**: `notion search` with text query and type filter
2. **Get**: `notion get` for pages and databases
3. **Create**: `notion page create` with title and parent
4. **Append**: `notion page append` with markdown support
5. **Query**: `notion db query` with basic filtering
6. **Skills**: `notion skills list` and `notion skills show`
7. **Output**: `--json` flag for all commands
8. **Documentation**: Auto-generated SKILLS.md

### Out of Scope (Post-MVP)

1. File uploads (already in ultimate-notion CLI)
2. Complex database filtering (AND/OR logic)
3. Block-level updates
4. Comments and mentions
5. OAuth authentication flow
6. Export formats (HTML, PDF)
7. Batch operations

---

## Technical Design

### Architecture

```
notion-cli/
├── src/
│   └── notion_cli/
│       ├── __init__.py
│       ├── cli.py              # Main typer app
│       ├── commands/           # Command modules
│       │   ├── __init__.py
│       │   ├── search.py
│       │   ├── page.py
│       │   ├── database.py
│       │   ├── block.py
│       │   └── skills.py
│       ├── core/               # Shared utilities
│       │   ├── __init__.py
│       │   ├── output.py       # JSON/text output formatting
│       │   ├── errors.py       # Error handling
│       │   └── skills_doc.py   # SKILLS.md generator
│       └── vendor/             # Vendored ultimate-notion
│           └── ultimate_notion/
├── tests/
├── SKILLS.md                   # Auto-generated
├── pyproject.toml
└── README.md
```

### Dependencies

- `typer>=0.16` - CLI framework
- `rich>=13.0` - Terminal output formatting
- `pydantic>=2.0` - Data validation (from ultimate-notion)
- `notion-client~=2.5.0` - Low-level Notion API (from ultimate-notion)

### Output Format

All commands support `--json` flag:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Or on error:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "Page not found"
  }
}
```

---

## Testing Strategy

1. **Unit Tests**: Each command module tested in isolation
2. **Integration Tests**: Mock Notion API responses using VCR.py
3. **CLI Tests**: Test full command invocation with Click/typer test runner
4. **Skills Tests**: Verify SKILLS.md is valid and complete

---

## Open Questions

1. Should we keep the `uno` command name or use `notion`?
2. How to handle authentication (env var vs config file vs CLI flag)?
3. Should skills be discoverable via `notion --help` or only via `skills` command?
4. Pagination strategy for large databases?

---

## Approval

**Status**: Draft  
**Created**: 2026-03-20  
**Reviewed By**: [Pending]  
**Approved By**: [Pending]
