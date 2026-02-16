# Obsidian Inbox Agent

A Claude Code skill for triaging and classifying markdown notes in an Obsidian inbox.

## Features

- **Automatic classification** of notes as `personal` or `professional`
- **Frontmatter enrichment** with appropriate tags
- **Dry-run mode** to preview changes without modifying files

## Installation

Copy the `.claude` folder and `CLAUDE.md` to your project root.

## Usage

### Triage Inbox

```
/triage-inbox
```

Processes all markdown files in your inbox directory, classifies them, and applies frontmatter tags.

### Dry-Run (Preview)

```
/triage-inbox-dry-run
```

Shows what classifications would be applied without modifying any files.

## Classification Rules

### Professional Signals
- IMD, Copilot, Azure, AI strategy
- Faculty, participants, programs
- Business development, OKRs
- Digital transformation, enterprise software
- Meetings, team/colleague names

### Personal Signals
- Health, wellness, medical
- Family, relationships
- Hobbies, leisure
- Travel (non-business)
- Journaling, self-reflection
- Personal finance

### Edge Cases
- Ambiguous content defaults to `professional`
- Mixed content uses majority rule (>70%)

## Output Format

Each processed file receives frontmatter:

```yaml
---
tags:
  - inbox
  - professional  # or personal
  - meeting       # subcategory
created: 2026-02-16
status: inbox
---
```

## License

MIT
