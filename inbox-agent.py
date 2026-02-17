#!/usr/bin/env python3
"""
Inbox Triage Agent - Automatically classifies and tags markdown files
Usage: python3 inbox-agent.py [--watch] [--dry-run]
"""

import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package required. Run: pip install anthropic")
    sys.exit(1)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog package required. Run: pip install watchdog")
    sys.exit(1)

INBOX_PATH = Path("/Users/xyufeng/The Vault/Inbox")
SKILL_PATH = Path("/Users/xyufeng/The Vault/.claude/skills/inbox-classifier.md")

def load_skill():
    """Load the inbox-classifier skill"""
    with open(SKILL_PATH, 'r') as f:
        return f.read()

def has_frontmatter(content: str) -> bool:
    """Check if file already has frontmatter"""
    return content.strip().startswith('---')

def classify_file(filepath: Path, skill_content: str, client: Anthropic, dry_run: bool = False) -> dict:
    """Classify a markdown file using the skill rules"""

    with open(filepath, 'r') as f:
        content = f.read()

    if has_frontmatter(content):
        return {"status": "skipped", "reason": "already has frontmatter"}

    prompt = f"""You are an inbox classifier. Apply these classification rules:

{skill_content}

Now classify this markdown file and add appropriate frontmatter.

File: {filepath.name}
Content:
{content}

Output ONLY the complete updated file content with frontmatter added. No explanations."""

    if dry_run:
        # Simulate classification without API call
        return {"status": "dry-run", "file": str(filepath)}

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        new_content = message.content[0].text

        # Strip markdown code fences if present
        if new_content.strip().startswith('```'):
            lines = new_content.strip().split('\n')
            # Remove first line (```markdown or ```) and last line (```)
            new_content = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])

        # Write updated content
        with open(filepath, 'w') as f:
            f.write(new_content)

        return {"status": "processed", "file": str(filepath)}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def process_existing_files(dry_run: bool = False):
    """Process all existing files in inbox"""
    client = Anthropic() if not dry_run else None
    skill = load_skill()

    print(f"Processing existing files in {INBOX_PATH}...")

    for filepath in INBOX_PATH.glob("*.md"):
        result = classify_file(filepath, skill, client, dry_run)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - {result}")

class InboxHandler(FileSystemEventHandler):
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.client = Anthropic() if not dry_run else None
        self.skill = load_skill()

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return

        # Wait for file to be fully written
        time.sleep(1)

        filepath = Path(event.src_path)
        result = classify_file(filepath, self.skill, self.client, self.dry_run)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} - {result}")

def watch_mode(dry_run: bool = False):
    """Watch inbox for new files"""
    process_existing_files(dry_run)

    print(f"\nWatching {INBOX_PATH} for new files...")
    print("Press Ctrl+C to stop\n")

    event_handler = InboxHandler(dry_run)
    observer = Observer()
    observer.schedule(event_handler, str(INBOX_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    parser = argparse.ArgumentParser(description="Inbox Triage Agent")
    parser.add_argument("--watch", action="store_true", help="Watch for new files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without changes")
    args = parser.parse_args()

    if not INBOX_PATH.exists():
        print(f"Error: Inbox path does not exist: {INBOX_PATH}")
        sys.exit(1)

    if args.watch:
        watch_mode(args.dry_run)
    else:
        process_existing_files(args.dry_run)

if __name__ == "__main__":
    main()
