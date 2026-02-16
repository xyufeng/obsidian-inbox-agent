Preview inbox triage without making changes.

## Instructions

1. Find all `.md` files in the inbox directory (ask user for path if not known)
2. For each file:
   - Apply the inbox-classifier skill to analyze the content
   - Determine classification (personal/professional)
   - Show what frontmatter would be applied
3. Do NOT modify any files
4. Report summary of proposed classifications

Use the classification rules defined in `.claude/skills/inbox-classifier.md`.

This is a dry-run: analyze and report only, no file modifications.
