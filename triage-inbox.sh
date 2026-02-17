#!/bin/bash
# Batch Triage - Process all unprocessed files in inbox
# Usage: ./triage-inbox.sh [--dry-run]

INBOX="/Users/xyufeng/The Vault/Inbox"
DRY_RUN="${1:-}"

find "$INBOX" -name "*.md" -type f | while read -r file; do
    # Skip files that already have frontmatter with 'inbox' tag
    if head -10 "$file" | grep -q "status: inbox"; then
        echo "Skipping (already processed): $file"
        continue
    fi

    echo "Processing: $file"

    if [ "$DRY_RUN" == "--dry-run" ]; then
        echo "  [DRY-RUN] Would classify: $file"
    else
        claude --print "Read '$file' and apply the inbox-classifier skill to classify it as personal or professional, then add appropriate frontmatter. Preserve all content."
        echo "  Done: $file"
    fi
done

echo "Triage complete."
