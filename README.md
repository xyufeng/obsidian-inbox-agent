# Obsidian Inbox Agent

A Claude Code skill for triaging and classifying markdown notes in an Obsidian inbox.

## Features

- **Automatic classification** of notes as `personal` or `professional`
- **Frontmatter enrichment** with appropriate tags
- **Dry-run mode** to preview changes without modifying files

## Installation

Copy the `.claude` folder and `CLAUDE.md` to your Obsidian vault root.

For automated processing, also copy the Python agent files.

### Dependencies

```bash
pip install anthropic watchdog
```

Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY=your-key-here
```

## Usage

### Option 1: Automated Agent (Recommended)

**Watch mode** - Auto-process new files:
```bash
python3 inbox-agent.py --watch
```

**One-time processing:**
```bash
python3 inbox-agent.py
```

**Dry-run (preview):**
```bash
python3 inbox-agent.py --dry-run
```

### Option 2: Claude Code Slash Commands

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

## Files

| File | Description |
|------|-------------|
| `.claude/skills/inbox-classifier.md` | Classification rules and logic |
| `.claude/commands/triage-inbox.md` | Slash command for processing |
| `.claude/commands/triage-inbox-dry-run.md` | Preview slash command |
| `inbox-agent.py` | Automated Python agent with file watching |
| `inbox-watcher.sh` | Shell-based file watcher (requires fswatch) |
| `triage-inbox.sh` | Batch processing shell script |

## License

MIT
