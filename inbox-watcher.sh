#!/bin/bash
# Inbox Watcher - Auto-triage new files using Claude Code
# Usage: ./inbox-watcher.sh

INBOX="/Users/xyufeng/The Vault/Inbox"
SKILL_PATH="/Users/xyufeng/The Vault/.claude/skills/inbox-classifier.md"
LOG_FILE="/Users/xyufeng/The Vault/.inbox-watcher.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Starting inbox watcher..."
log "Watching: $INBOX"
log "Press Ctrl+C to stop"

# Process existing unprocessed files first
find "$INBOX" -name "*.md" -type f | while read -r file; do
    if ! head -5 "$file" | grep -q "^---"; then
        log "Processing existing file: $file"
        claude --print "Read the markdown file at '$file'. Apply the inbox-classifier skill rules: classify as 'personal' or 'professional' based on content signals, then add YAML frontmatter with tags (inbox, classification, subcategory), created date, and status: inbox. Preserve all original content. Output the complete updated file." > "${file}.tmp" && mv "${file}.tmp" "$file"
        log "Done: $file"
    fi
done

# Watch for new files
fswatch -r --event Created --event Modified --latency 2 "$INBOX" 2>/dev/null | while read -r file; do
    # Only process .md files
    if [[ "$file" == *.md ]]; then
        # Skip if already has frontmatter
        sleep 1  # Wait for file to be fully written
        if ! head -5 "$file" | grep -q "^tags:"; then
            log "New file detected: $file"
            claude --print "Read the markdown file at '$file'. Apply the inbox-classifier skill rules: classify as 'personal' or 'professional' based on content signals, then add YAML frontmatter with tags (inbox, classification, subcategory), created date, and status: inbox. Preserve all original content. Output the complete updated file." > "${file}.tmp" && mv "${file}.tmp" "$file"
            log "Processed: $file"
        fi
    fi
done
