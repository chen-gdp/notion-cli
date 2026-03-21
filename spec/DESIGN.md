# Notion CLI Design Document

## Architecture Overview

```
notion-cli/
├── src/notion_cli/                    # Main package
│   ├── __init__.py                    # Package init, version
│   ├── cli.py                         # Main typer app, entry point
│   ├── commands/                      # Command implementations
│   │   ├── __init__.py
│   │   ├── search.py                  # Spec 1.1: search command
│   │   ├── get.py                     # Spec 1.1: get command
│   │   ├── skills.py                  # Spec 1.1: skills list/show
│   │   ├── database.py                # Spec 1.2, 1.3: db get, query, insert
│   │   ├── page.py                    # Spec 1.4, 2.1, 2.2: page CRUD
│   │   └── __init__.py
│   ├── core/                          # Shared utilities
│   │   ├── __init__.py
│   │   ├── output.py                  # JSON/text formatting
│   │   ├── errors.py                  # Error handling, custom exceptions
│   │   ├── session.py                 # Notion session management
│   │   ├── markdown.py                # Markdown → Notion blocks parser
│   │   └── skills_registry.py         # Skills metadata, SKILLS.md generator
│   └── vendor/                        # Vendored ultimate-notion
│       └── ultimate_notion/           # Copied from ultimate-notion/src/
├── tests/
│   ├── unit/                          # Unit tests per command
│   ├── integration/                   # Integration tests with mocks
│   └── fixtures/                      # Test data, VCR cassettes
├── SKILLS.md                          # Auto-generated (do not edit)
├── pyproject.toml                     # Package config
└── README.md                          # User documentation
```

---

## Component Design

### 1. CLI Layer (`cli.py`)

**Responsibility:** Entry point, command routing, global options

```python
import typer
from notion_cli.commands import search, get, skills, database, page

app = typer.Typer(name="notion", help="Notion CLI for AI agents")

# Global callback for --json flag
@app.callback()
def main(json: bool = typer.Option(False, "--json", help="Output as JSON")):
    ctx = typer.get_current_context()
    ctx.ensure_object(dict)
    ctx.obj["json"] = json

# Register commands
app.add_typer(search.app, name="search")
app.add_typer(get.app, name="get")
app.add_typer(skills.app, name="skills")
app.add_typer(database.app, name="db")
app.add_typer(page.app, name="page")
```

**Key Design:**
- Single typer app with subcommands
- Global `--json` flag stored in context
- Commands organized by resource type (page, db, skills)

---

### 2. Command Layer (`commands/*.py`)

**Pattern:** Each command module exports a typer app

```python
# commands/search.py
import typer
from notion_cli.core.output import output_json, output_table
from notion_cli.core.session import get_session

app = typer.Typer()

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    type: str = typer.Option(None, "--type", help="Filter by type: page|database"),
    limit: int = typer.Option(100, "--limit", help="Max results"),
):
    """Search for pages and databases."""
    session = get_session()
    results = session.search(query, type=type, limit=limit)
    
    if ctx.obj.get("json"):
        output_json({"success": True, "data": results})
    else:
        output_table(results, columns=["title", "type", "id"])
```

**Command Structure:**
- Each command validates inputs
- Calls core session for Notion API operations
- Formats output via `core/output.py`
- Handles errors consistently

---

### 3. Core Layer (`core/*.py`)

#### 3.1 Configuration Management (`config.py`)

**Responsibility:** Manage CLI configuration, auth tokens, settings

**Config Locations (in order of priority):**
1. Environment variable: `NOTION_TOKEN`
2. Config file: `~/.config/notion-cli/config.json`
3. Project config: `./.notion-cli.json`

```python
import json
import os
from pathlib import Path
from typing import Optional

class Config:
    """Configuration manager for notion-cli."""
    
    def __init__(self):
        self._config_dir = Path.home() / ".config" / "notion-cli"
        self._config_file = self._config_dir / "config.json"
        self._data = {}
        self._load()
    
    def _load(self):
        """Load config from file if exists."""
        if self._config_file.exists():
            with open(self._config_file) as f:
                self._data = json.load(f)
    
    def _save(self):
        """Save config to file."""
        self._config_dir.mkdir(parents=True, exist_ok=True)
        with open(self._config_file, 'w') as f:
            json.dump(self._data, f, indent=2)
    
    def get_token(self) -> Optional[str]:
        """Get Notion token from env var or config."""
        # Priority 1: Environment variable
        token = os.environ.get("NOTION_TOKEN")
        if token:
            return token
        
        # Priority 2: Config file
        return self._data.get("token")
    
    def set_token(self, token: str):
        """Save token to config file."""
        self._data["token"] = token
        self._save()
    
    def clear_token(self):
        """Remove token from config."""
        if "token" in self._data:
            del self._data["token"]
            self._save()
    
    def get_config_path(self) -> Path:
        """Return path to config file."""
        return self._config_file
    
    def to_dict(self) -> dict:
        """Return config as dict (hiding sensitive data)."""
        return {
            "config_file": str(self._config_file),
            "has_token": bool(self.get_token()),
            "data": {k: v for k, v in self._data.items() if k != "token"}
        }

# Global config instance
_config: Optional[Config] = None

def get_config() -> Config:
    """Get or create global config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
```

**Config File Structure:**
```json
{
  "token": "secret_xxxxxxxxxxxxxxxx",
  "default_workspace": "Personal",
  "templates_dir": "~/.config/notion-cli/templates"
}
```

---

#### 3.2 Session Management (`session.py`)

**Responsibility:** Manage Notion API connection, caching, auth

```python
from ultimate_notion import Session
from notion_cli.core.config import get_config
from notion_cli.core.errors import AuthError

class NotionSession:
    """Wrapper around ultimate_notion Session with error handling."""
    
    _instance = None
    
    @classmethod
    def get(cls) -> Session:
        if cls._instance is None:
            config = get_config()
            token = config.get_token()
            if not token:
                raise AuthError(
                    "No Notion token found. Run 'notion auth setup' or set NOTION_TOKEN environment variable."
                )
            cls._instance = Session(token=token)
        return cls._instance
    
    @classmethod
    def close(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance = None
    
    @classmethod
    def is_authenticated(cls) -> bool:
        """Check if we have a token available."""
        config = get_config()
        return bool(config.get_token())

def get_session() -> Session:
    """Get or create Notion session."""
    return NotionSession.get()

def check_auth() -> bool:
    """Check if authenticated without creating session."""
    return NotionSession.is_authenticated()
```

**Design Decisions:**
- Config file in `~/.config/notion-cli/` (XDG standard)
- Env var takes priority over config file
- Singleton pattern for session reuse
- Lazy initialization
- Auto-cleanup on exit

---

#### 3.2 Output Formatting (`output.py`)

**Responsibility:** Format results as JSON or human-readable tables

```python
import json
import sys
from typing import Any
from rich.console import Console
from rich.table import Table

console = Console()

def output_json(data: dict, success: bool = True):
    """Output structured JSON for AI parsing."""
    response = {
        "success": success,
        "data": data if success else None,
        "error": data if not success else None
    }
    console.print(json.dumps(response, indent=2, default=str))
    sys.exit(0 if success else 1)

def output_table(data: list[dict], columns: list[str]):
    """Output human-readable table."""
    if not data:
        console.print("No results found.")
        return
    
    table = Table(show_header=True, header_style="bold")
    for col in columns:
        table.add_column(col)
    
    for item in data:
        row = [str(item.get(col, "")) for col in columns]
        table.add_row(*row)
    
    console.print(table)

def output_error(code: str, message: str, details: dict = None):
    """Output error in consistent format."""
    error_data = {"code": code, "message": message}
    if details:
        error_data["details"] = details
    output_json(error_data, success=False)
```

**Output Format:**
```json
{
  "success": true,
  "data": [...],
  "error": null
}
```

---

#### 3.3 Markdown Parser (`markdown.py`)

**Responsibility:** Convert markdown to Notion block objects

```python
from ultimate_notion.blocks import Paragraph, Heading, Code, BulletedListItem, ToDo
import re

def parse_markdown(text: str) -> list:
    """Parse markdown text into Notion block objects."""
    blocks = []
    lines = text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Code blocks
        if line.startswith('```'):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append(Code('\n'.join(code_lines), language=lang or 'plain text'))
            i += 1
            continue
        
        # Headings
        if line.startswith('## '):
            blocks.append(Heading(line[3:], level=2))
            i += 1
            continue
        if line.startswith('### '):
            blocks.append(Heading(line[4:], level=3))
            i += 1
            continue
        
        # Todo items
        todo_match = re.match(r'- \[([ x])\] (.+)', line)
        if todo_match:
            checked = todo_match.group(1) == 'x'
            blocks.append(ToDo(todo_match.group(2), checked=checked))
            i += 1
            continue
        
        # Bulleted lists
        if line.startswith('- '):
            blocks.append(BulletedListItem(line[2:]))
            i += 1
            continue
        
        # Paragraphs (default)
        if line.strip():
            blocks.append(Paragraph(line))
        i += 1
    
    return blocks
```

**Supported Markdown:**
- `## Heading` → Heading 2
- `### Heading` → Heading 3
- `- item` → Bulleted list
- `- [ ] task` → To-do unchecked
- `- [x] task` → To-do checked
- ````python ... ```` → Code block
- Plain text → Paragraph

---

#### 3.4 Error Handling (`errors.py`)

```python
class NotionCLIError(Exception):
    """Base CLI error with code and message."""
    def __init__(self, code: str, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)

class AuthError(NotionCLIError):
    """Authentication failed."""
    def __init__(self, message: str):
        super().__init__("AUTH_ERROR", message)

class NotFoundError(NotionCLIError):
    """Resource not found."""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__("NOT_FOUND", f"{resource_type} '{resource_id}' not found",
                        {"type": resource_type, "id": resource_id})

class ValidationError(NotionCLIError):
    """Invalid input."""
    def __init__(self, field: str, message: str):
        super().__init__("VALIDATION_ERROR", message, {"field": field})
```

---

#### 3.5 Skills Registry (`skills_registry.py`)

**Responsibility:** Auto-generate SKILLS.md from command metadata

```python
from typing import List, Dict
import typer
from pathlib import Path

class Skill:
    def __init__(self, name: str, description: str, category: str, 
                 usage: str, args: list, options: list, examples: list):
        self.name = name
        self.description = description
        self.category = category
        self.usage = usage
        self.args = args
        self.options = options
        self.examples = examples

class SkillsRegistry:
    """Registry of all CLI skills/commands."""
    
    _skills: Dict[str, Skill] = {}
    
    @classmethod
    def register(cls, skill: Skill):
        cls._skills[skill.name] = skill
    
    @classmethod
    def list(cls) -> List[Skill]:
        return list(cls._skills.values())
    
    @classmethod
    def get(cls, name: str) -> Skill:
        return cls._skills.get(name)
    
    @classmethod
    def generate_skills_md(cls, output_path: Path):
        """Generate SKILLS.md file."""
        lines = ["# Notion CLI Skills\n"]
        
        for skill in sorted(cls._skills.values(), key=lambda s: s.name):
            lines.extend([
                f"## Skill: {skill.name}\n",
                f"{skill.description}\n",
                "### Usage\n",
                f"```bash\n{skill.usage}\n```\n",
                "### Parameters\n",
            ])
            
            for arg in skill.args:
                req = "(required)" if arg.get("required") else "(optional)"
                lines.append(f"- `{arg['name']}` {req}: {arg['description']}\n")
            
            for opt in skill.options:
                lines.append(f"- `--{opt['name']}`: {opt['description']}\n")
            
            lines.extend([
                "### Examples\n",
            ])
            for ex in skill.examples:
                lines.append(f"```bash\n{ex}\n```\n")
            
            lines.append(f"Category: {skill.category}\n")
            lines.append("---\n")
        
        output_path.write_text(''.join(lines))
```

**SKILLS.md Generation:**
- Commands self-register with `@register_skill` decorator
- Build process calls `generate_skills_md()`
- File committed to repo for OpenClaw discovery

---

### 4. Vendor Layer (`vendor/ultimate_notion/`)

**Approach:** Copy ultimate-notion source, don't submodule

**Rationale:**
- No external dependency to break
- Pinned version
- Can patch if needed
- Simpler install for OpenClaw

**Process:**
```bash
# One-time vendoring
cp -r ultimate-notion/src/ultimate_notion notion-cli/src/notion_cli/vendor/

# Update as needed
cd ultimate-notion && git pull
cp -r src/ultimate_notion ../notion-cli/src/notion_cli/vendor/
```

---

## Data Flow

### Search Flow
```
User: notion search "meeting" --json
    ↓
cli.py: search command
    ↓
commands/search.py: validate args
    ↓
core/session.py: get_session()
    ↓
vendor/ultimate_notion/Session.search()
    ↓
Notion API
    ↓
commands/search.py: format results
    ↓
core/output.py: output_json()
    ↓
stdout: {"success": true, "data": [...]}
```

### Page Append Flow
```
User: notion page append <id> --content "## Goals"
    ↓
cli.py: page append command
    ↓
commands/page.py: append handler
    ↓
core/markdown.py: parse_markdown()
    → Returns: [Heading("Goals", level=2)]
    ↓
vendor/ultimate_notion/Page.append()
    ↓
Notion API (batch block creation)
    ↓
commands/page.py: format result
    ↓
core/output.py: output_json() or output_table()
```

---

## Testing Strategy

### Unit Tests
```python
# tests/unit/test_markdown.py
def test_parse_heading():
    blocks = parse_markdown("## Test")
    assert len(blocks) == 1
    assert blocks[0].type == "heading_2"
    assert blocks[0].text == "Test"

def test_parse_code_block():
    md = "```python\nprint('hello')\n```"
    blocks = parse_markdown(md)
    assert blocks[0].type == "code"
    assert blocks[0].language == "python"
```

### Integration Tests (VCR.py)
```python
# tests/integration/test_search.py
@pytest.mark.vcr
def test_search_returns_results():
    result = runner.invoke(app, ["search", "test", "--json"])
    data = json.loads(result.output)
    assert data["success"] is True
    assert "data" in data
```

---

## Build & Distribution

### pyproject.toml
```toml
[project]
name = "notion-cli"
version = "0.1.0"
description = "Notion CLI for AI agents"
dependencies = [
    "typer>=0.16",
    "rich>=13.0",
    "pydantic>=2.0",
    # ultimate-notion deps vendored
]

[project.scripts]
notion = "notion_cli.cli:app"

[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "vcrpy"]
```

### Installation
```bash
# For OpenClaw
pip install git+https://github.com/chen-gdp/notion-cli.git

# Set auth
export NOTION_TOKEN=secret_xxx

# Use
notion search "project" --json
```

---

## Implementation Phases

### Phase 1: Foundation (Sprint 1)
- [ ] Project structure
- [ ] Vendor ultimate-notion
- [ ] Session management
- [ ] Output formatting
- [ ] Error handling
- [ ] `search`, `get`, `skills list/show`

### Phase 2: Database Operations (Sprint 2)
- [ ] `db get` - schema inspection
- [ ] `db query` - with simple filters
- [ ] `db insert` - create entries
- [ ] `page update` - property updates
- [ ] `page archive` - soft delete

### Phase 3: Content Creation (Sprint 3)
- [ ] `page create` - standalone pages
- [ ] Markdown parser
- [ ] `page append` - rich content
- [ ] SKILLS.md generation

### Phase 4: Polish (Sprint 4)
- [ ] Enhanced search
- [ ] Incremental updates
- [ ] Documentation
- [ ] Integration tests

---

## Design Decisions Log

| Decision | Alternative | Rationale |
|----------|-------------|-----------|
| Vendor ultimate-notion | Git submodule | Simpler install, pinned version |
| `NOTION_TOKEN` env var | Config file, OAuth | Simplest for MVP, agent-friendly |
| Simple filters only | Complex AND/OR | Sufficient for MVP use cases |
| Markdown → blocks | Direct block API | More natural for agent content |
| Typer | Click, argparse | Modern, type hints, rich support |
| Rich tables | Plain text | Better UX for human debugging |
| Singleton session | Per-command session | Reuse connection, caching |

---

## Open Questions

1. **Caching:** Should we cache search results? (Probably not for MVP)
2. **Rate limiting:** Handle 429 errors with retry? (Yes, exponential backoff)
3. **Pagination:** Cursor support in `db query`? (Post-MVP)
4. **Templates:** Hardcoded or user-defined? (Hardcoded in agent for MVP)
5. **Block operations:** Needed for priority use cases? (No, defer to Phase 3)
