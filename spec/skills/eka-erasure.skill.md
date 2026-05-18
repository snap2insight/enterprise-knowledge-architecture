---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-erasure
      version: 1.0
      agents: [L2, L3]                        # erasure crosses tiers
      side_effects: yes
      duration_estimate: 30-60 minutes
      human_required: yes
---

# Skill: eka-erasure

## Purpose

Process a GDPR Article 17 (right to erasure) request: find all
documents referencing a given data subject, propose redactions,
apply them upon human approval, and produce the audit trail.

## When to invoke

- Privacy admin receives a verified erasure request from a data
  subject
- Compliance team performs routine erasure-test (annual)

## Inputs

Required:

| Input | Type | Example |
|-------|------|---------|
| `subject_id` | string | `EMP-042` or `CAND-2026-W12-001` or a customer-side identifier |
| `request_reference` | string | Internal ticket ID for the request |
| `request_date` | date | When the request was received |
| `requester_role` | string | "Privacy admin: jdoe@example.com" |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `dry_run` | true | If true: produce the list only; don't redact |
| `scope` | all-stores | Limit to a specific store if needed |
| `retention_exceptions` | none | List of legal-hold reasons that block erasure |

## Steps

### 1. Identify the subject

Confirm `subject_id` is recognized:

- For EMP / CAND / BOARD codes: verify the code is registered in
  HRIS (out of scope for the agent; operator confirms)
- For customer-side individuals: confirm the customer's privacy
  policy mandates Article 17 honoring (some don't, depending on
  jurisdiction and contract)

### 2. Discover references — Git stores

For each L1+ Git repo in scope:

```bash
# Find files where data_subjects: includes the subject
git grep -l "data_subjects:" | xargs python -c "
  import yaml, sys
  for path in sys.argv[1:]:
    fm = parse_frontmatter(path)
    if subject_id in fm.get('data_subjects', []):
      print(path)
"

# Also full-text grep for safety net
git grep -l "{subject_id}" -- '*.md'
```

Both lists should overlap heavily. Discrepancies indicate:
- Doc references subject but doesn't declare in frontmatter
  (bug — fix during this erasure)
- Doc declares but doesn't actually mention (stale metadata —
  also fix)

### 3. Discover references — Drive (L3)

For Drive folders the agent has access to (via the L3 MCP):

```bash
# List all .md files; check frontmatter for data_subjects
eka erasure find --subject {subject_id} --store drive
```

This requires an L3-scoped MCP; an L2-only agent will fail this
step. If you're L2, escalate to L3 agent for the Drive scan.

### 4. Produce the redaction candidate list

For each found document:

```markdown
- repo:{org}-company-docs/customer/account-plans/c001-q3.md
  - line 47: "...mentions {subject_id} as the contract lead"
  - recommended redaction: "[REDACTED — GDPR Art. 17 erasure {request_reference}]"
  - keeps: rest of document intact
- drive:1abc... ({org}-drive/people-confidential/perf/EMP-042.md)
  - entire document
  - recommended action: move to archive with redacted body
- ...
```

### 5. HUMAN REVIEW (mandatory)

Stop. Present the candidate list to the privacy admin. The admin:

- Confirms each redaction
- Flags any retention exceptions (active litigation, legal hold,
  regulatory requirement to retain)
- Approves the redaction batch as a whole

The agent does not proceed without explicit approval.

### 6. Apply redactions (dry_run = false)

For each approved redaction:

```bash
# In Git stores: edit the file
# Replace the reference with tombstone
# Update frontmatter: remove subject from data_subjects
# Update last_reviewed = today, add review_notes: { type: erasure, reason: {request_ref} }
# Commit on branch: erasure-{request_ref}
```

For Drive files:

```bash
# Read file
# Apply redaction
# Write back to same Drive location
# Or move to archive folder if redaction is whole-document
```

### 7. Create the PR (Git stores)

Open one PR per repo with the erasure changes. PR title:

```
Erasure: {request_reference}
```

PR body:

```markdown
GDPR Article 17 erasure request {request_reference}.
Subject: {subject_id}
Request date: {request_date}
Requester: {requester_role}

Redactions applied:
- N references redacted across N files
- N files moved to archive/

Retention exceptions:
- (list any)

Audit log entry: audit-log/erasures/{request_date}-{subject_id}.md
```

Mark PR with label `erasure-art17` for visibility.

### 8. Write audit-log entry

In the L2 repo's audit-log location:

```markdown
---
title: "Erasure {request_reference} — {subject_id}"
domain: operational
classification: { C: HIGH, I: HIGH, A: LOW }
tier: L2
owner: {requester_role}
status: approved
last_reviewed: {request_date}
next_review: {request_date + 1y}
review_cadence: 1y
data_subjects: []
labels: [erasure, gdpr-art17, audit]
---

# Erasure request {request_reference}

## Request

- Subject: {subject_id}
- Date: {request_date}
- Requester: {requester_role}
- Channel: (email / portal / etc.)
- Verification: (how the request was authenticated)

## Scope

- Stores searched: {list}
- Files found: {count}
- Files redacted: {count}
- Files moved to archive: {count}

## Retention exceptions

(any, with rationale)

## Confirmation

- Erasure completed: {date}
- PRs: {list}
- Subject notified: {date}
```

### 9. Notify the subject

Out-of-scope for the agent. Operator sends confirmation per the
org's privacy-response template.

## Validations

- All references found via frontmatter == references found via
  full-text grep (within reason)
- Every redaction has a tombstone in place
- Audit-log entry is committed
- PR(s) are open with the right label

## Outputs

| Output | Location |
|--------|----------|
| Candidate redaction list | Returned to operator before step 5 |
| Audit-log entry | L2 repo's audit-log folder |
| Redaction PRs | One per affected repo |
| Summary report | Inline + audit-log entry |

## Failure handling

| Failure | Recovery |
|---------|----------|
| Subject not registered | Refuse; require operator to register or confirm out-of-scope |
| Drive access blocked | Surface limit ("can only see X of Y stores"); operator escalates to L3 agent |
| Retention exception blocks complete erasure | Document the exception; partial erasure with explicit "retained for: ..." note |
| Operator approves but git push fails | Provide manual instructions; pause; resume on `--resume` |

## What this skill does NOT do

- Verify the subject's identity (request authentication is
  operator/admin's job)
- Notify regulators (separate workflow)
- Erase production-system data (out of EKA scope; live secrets
  and DB records are L4)
- Erase backups (separate retention policy)
