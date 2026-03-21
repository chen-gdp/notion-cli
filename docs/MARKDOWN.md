# Markdown Support

Complete guide to markdown syntax supported by the `notion page append` command.

## Table of Contents

- [Headings](#headings)
- [Paragraphs](#paragraphs)
- [Lists](#lists)
- [Todo Lists](#todo-lists)
- [Code Blocks](#code-blocks)
- [Formatting](#formatting)
- [Examples](#examples)

---

## Headings

Use `#` symbols to create headings. Three levels are supported.

```markdown
# Heading 1
## Heading 2
### Heading 3
```

**Notion Output:**
- `#` → Heading 1 block
- `##` → Heading 2 block
- `###` → Heading 3 block

**Example:**

```bash
notion page append <page_id> --content "# Project Overview

## Goals

### Short Term

Complete MVP by end of quarter."
```

---

## Paragraphs

Plain text is automatically converted to paragraphs.

```markdown
This is a paragraph.

This is another paragraph with multiple sentences. It will be rendered as a single paragraph block.
```

**Example:**

```bash
notion page append <page_id> --content "This is the introduction paragraph.

This is a second paragraph with more details about the topic."
```

---

## Lists

### Bullet Lists

Use `-` or `*` followed by a space.

```markdown
- Item 1
- Item 2
- Item 3

* Alternative bullet
* Another item
```

**Example:**

```bash
notion page append <page_id> --content "## Requirements

- User authentication
- Database integration
- API endpoints
- Frontend dashboard"
```

### Numbered Lists

Use numbers followed by a period.

```markdown
1. First step
2. Second step
3. Third step
```

**Example:**

```bash
notion page append <page_id> --content "## Setup Instructions

1. Install dependencies
2. Configure environment variables
3. Run database migrations
4. Start the server"
```

### Nested Lists

Indent with spaces for nested items.

```markdown
- Parent item
  - Child item 1
  - Child item 2
- Another parent
  - Child item
```

**Example:**

```bash
notion page append <page_id> --content "## Features

- Authentication
  - Email/password login
  - OAuth integration
  - Two-factor auth
- Database
  - PostgreSQL support
  - Redis caching"
```

---

## Todo Lists

Create checkboxes with `- [ ]` (unchecked) and `- [x]` (checked).

```markdown
- [ ] Unchecked task
- [x] Checked task
- [ ] Another unchecked task
```

**Example:**

```bash
notion page append <page_id> --content "## Action Items

- [ ] Review pull request #123
- [ ] Update documentation
- [x] Fix bug in authentication
- [ ] Deploy to staging
- [ ] Notify team"
```

**Mixed with other content:**

```bash
notion page append <page_id> --content "## Sprint Goals

### Must Have

- [ ] User login
- [ ] Dashboard view
- [ ] Profile editing

### Nice to Have

- [ ] Dark mode
- [ ] Export to PDF
- [ ] Mobile app"
```

---

## Code Blocks

Use triple backticks with optional language.

````markdown
```python
def hello():
    return "world"
```

```javascript
function greet() {
    console.log("Hello!");
}
```

```bash
echo "Hello World"
```
````

**Supported languages:**
- `python`
- `javascript` / `js`
- `typescript` / `ts`
- `bash` / `shell` / `sh`
- `json`
- `yaml` / `yml`
- `markdown` / `md`
- `html`
- `css`
- `sql`
- `go`
- `rust`
- `java`
- `ruby`
- `php`
- `c` / `cpp`
- `csharp` / `cs`
- `plaintext` (default)

**Example:**

```bash
notion page append <page_id> --content "## API Example

### Python

\`\`\`python
import requests

response = requests.get('https://api.example.com/users')
data = response.json()

for user in data['users']:
    print(user['name'])
\`\`\`

### cURL

\`\`\`bash
curl -H \"Authorization: Bearer TOKEN\" \\
  https://api.example.com/users
\`\`\`"
```

**Inline code:**

Use single backticks for inline code (converted to plain text with code styling).

```markdown
Use the `npm install` command to install dependencies.
```

**Example:**

```bash
notion page append <page_id> --content "Run \`npm install\` to install all dependencies.

Then use \`npm start\` to run the development server."
```

---

## Formatting

### Bold and Italic

```markdown
**bold text**
*italic text*
***bold and italic***
```

**Note:** Notion's API has limited support for inline formatting. Bold and italic may be converted to plain text in some cases.

**Example:**

```bash
notion page append <page_id> --content "This is **important** and this is *emphasized*.

Key points:
- **Security**: Use HTTPS
- **Performance**: Enable caching
- **Reliability**: Add retries"
```

### Links

```markdown
[Link text](https://example.com)
```

**Example:**

```bash
notion page append <page_id> --content "## Resources

- [Documentation](https://docs.example.com)
- [API Reference](https://api.example.com/docs)
- [Support](https://support.example.com)"
```

---

## Examples

### Meeting Notes

```bash
notion page append <page_id> --content "# Weekly Standup - $(date +%Y-%m-%d)

## Attendees

- Alice
- Bob
- Carol

## Updates

**Alice:** Completed authentication feature
**Bob:** Working on API integration
**Carol:** Finalizing designs

## Blockers

- Waiting for API keys from DevOps

## Action Items

- [ ] Bob to follow up on API keys
- [ ] Alice to deploy to staging
- [ ] Carol to share final mockups"
```

### Technical Documentation

```bash
notion page append <page_id> --content "# API Authentication

## Overview

All API requests require authentication via Bearer token.

## Getting a Token

1. Log in to your account
2. Go to Settings > API Keys
3. Generate a new key

## Using the Token

Include the token in the Authorization header:

\`\`\`bash
curl -H \"Authorization: Bearer YOUR_TOKEN\" \\
  https://api.example.com/data
\`\`\`

## Example Response

\`\`\`json
{
  \"status\": \"success\",
  \"data\": {
    \"id\": 123,
    \"name\": \"Example\"
  }
}
\`\`\`

## Error Codes

| Code | Description |
|------|-------------|
| 401 | Invalid token |
| 403 | Insufficient permissions |
| 429 | Rate limit exceeded |"
```

### Project Brief

```bash
notion page append <page_id> --content "# Project: Website Redesign

## Goals

- Improve conversion rate by 20%
- Reduce load time to <2 seconds
- Modernize visual design

## Scope

### In Scope

- Homepage redesign
- Product pages
- Checkout flow

### Out of Scope

- Mobile app
- Admin dashboard
- API changes

## Timeline

- **Week 1-2**: Research and planning
- **Week 3-4**: Design phase
- **Week 5-8**: Development
- **Week 9**: Testing
- **Week 10**: Launch

## Team

- Project Manager: Alice
- Designer: Bob
- Developer: Carol
- QA: Dave

## Success Metrics

- [ ] Conversion rate > 20%
- [ ] Page load < 2s
- [ ] Zero critical bugs
- [ ] User satisfaction > 4.5/5"
```

### Bug Report

```bash
notion page append <page_id> --content "# Bug Report: Login Failure

## Summary
Users unable to log in with valid credentials.

## Steps to Reproduce

1. Go to login page
2. Enter valid email and password
3. Click \"Sign In\"
4. Observe error

## Expected Behavior

User should be logged in and redirected to dashboard.

## Actual Behavior

Error message: \"Invalid credentials\"

## Environment

- Browser: Chrome 120
- OS: macOS 14.2
- Version: v2.1.0

## Screenshots

[Screenshot placeholder]

## Additional Context

- Issue started after v2.1.0 deployment
- Affects ~50% of users
- No errors in server logs

## Checklist

- [ ] Reproduce in staging
- [ ] Check authentication service
- [ ] Review recent changes
- [ ] Add logging
- [ ] Write test case"
```

### Release Notes

```bash
notion page append <page_id> --content "# Release Notes v2.2.0

## What's New

### Features

- Added dark mode support
- New dashboard widgets
- Improved search functionality

### Improvements

- 50% faster page loads
- Better mobile responsiveness
- Enhanced accessibility

### Bug Fixes

- Fixed login redirect issue
- Resolved data sync problems
- Corrected timezone handling

## Breaking Changes

None.

## Migration Guide

No action required.

## Known Issues

- [ ] Safari users may experience layout issues
- [ ] Export feature limited to 1000 rows

## Feedback

Report issues at https://github.com/example/issues"
```

---

## Tips

### Escaping Special Characters

Use backslash to escape special characters:

```bash
# Escape backticks
notion page append <page_id> --content "Use \`code\` inline"

# Escape newlines in bash
notion page append <page_id> --content "Line 1\nLine 2\nLine 3"
```

### Multi-line Content in Scripts

Use heredoc for complex content:

```bash
CONTENT=$(cat <<'EOF'
# Complex Document

This has multiple paragraphs.

## Section 1

- Item 1
- Item 2

## Section 2

```python
print("Hello")
```
EOF
)

notion page append <page_id> --content "$CONTENT"
```

### Reading from File

```bash
notion page append <page_id> --content "$(cat document.md)"
```

---

*See [COMMANDS.md](COMMANDS.md) for command reference.*
