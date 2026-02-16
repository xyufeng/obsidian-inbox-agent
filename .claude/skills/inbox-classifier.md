# Inbox Classifier Skill

Classify and enrich markdown files in an Obsidian inbox using frontmatter tags.

## Purpose

Analyze untagged markdown notes and apply appropriate frontmatter classification for personal vs professional content.

## Analysis Process

### Step 1: Read and Parse
- Read the full markdown content
- Check for existing frontmatter (preserve it)
- Extract title, headings, and body text

### Step 2: Classify Content

Apply these classification rules:

#### Professional Signals
Classify as `professional` if ANY of these are present:

**Keywords:**
- IMD (IMD business school context)
- Copilot, Azure, AI strategy
- Faculty, participants, programs
- Business development, OKRs
- Digital transformation, enterprise software
- Meetings with professional context
- Team/colleague names (e.g., Vincent Ballini)

**Indicators:**
- Work-related deadlines and deliverables
- Project codenames or initiatives
- Organizational structures
- Strategic planning content
- Professional development topics

#### Personal Signals
Classify as `personal` if ANY of these are present:

**Keywords:**
- Health, wellness, medical appointments
- Family members, relationships
- Hobbies, leisure activities
- Travel plans (non-business)
- Journaling, self-reflection
- Personal finance, budgeting
- Social plans with friends

**Indicators:**
- Emotional or reflective writing
- Home and domestic topics
- Personal goals unrelated to work
- Entertainment and recreation

### Step 3: Handle Edge Cases

**Ambiguous Content:**
- When content has signals from both categories → default to `professional`
- When no clear signals → default to `professional`
- Travel can be both → check context (conference = professional, vacation = personal)

**Mixed Content:**
- If >70% professional signals → `professional`
- If >70% personal signals → `personal`
- Otherwise → `professional` (safe default)

### Step 4: Apply Frontmatter

Generate frontmatter in this exact format:

```yaml
---
tags:
  - inbox
  - <classification>
  - <optional-subcategory>
created: <date-from-file-or-today>
status: inbox
---
```

**Classification values:**
- `professional` or `personal`
- Subcategory examples: `meeting`, `idea`, `task`, `note`, `reference`

### Step 5: Write Changes

- Preserve all existing content
- Add or update frontmatter only
- Maintain original formatting

## Output Format

After processing, report:
```
Processed: <filename>
Classification: <personal|professional>
Signals found: <list key signals>
Frontmatter applied: <yes|no-unchanged|updated>
```

## Example

**Input:**
```markdown
# Meeting with Vincent Ballini

Discussed Q3 OKRs and AI strategy for the digital transformation initiative.
```

**Output:**
```markdown
---
tags:
  - inbox
  - professional
  - meeting
created: 2026-02-16
status: inbox
---

# Meeting with Vincent Ballini

Discussed Q3 OKRs and AI strategy for the digital transformation initiative.
```

**Classification rationale:** Professional signals: Vincent Ballini (colleague), OKRs, AI strategy, digital transformation
