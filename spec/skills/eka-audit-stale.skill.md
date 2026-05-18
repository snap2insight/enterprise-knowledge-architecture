---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-audit-stale
      version: 1.0
      agents: [L1, L2, L3]
      side_effects: yes
      duration_estimate: 5-15 minutes
---

# Skill: eka-audit-stale

## Purpose

Find documents past their `next_review` date and apply the
graduated-staleness response: yellow flag, red flag + archive,
purge-candidate surfacing.

## When to invoke

- Monthly cadence (recommended; automated via CI cron)
- After a quarterly audit identifies stale-doc backlog
- Operator asks "what's stale?"

## Inputs

Required:

| Input | Type | Default |
|-------|------|---------|
| `repo` | string | current repo |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `window` | `30d` | Surface docs N+ days past `next_review` |
| `apply_actions` | `false` | If true, apply yellow/red flagging; if false, report only |
| `dry_run` | `true` | If true, doesn't write |

## Steps

### 1. Enumerate documents

```bash
find {repo} -name "*.md" -not -path "*/_build/*" -not -path "*/.git/*"
```

For each, parse frontmatter and compute days-past-review:

```python
days_past = (today - next_review).days
```

### 2. Classify each doc

| Days past | Bucket | Action |
|-----------|--------|--------|
| < 0 | On time | No action |
| 0–29 | Grace | No action |
| 30–89 | Yellow flag | Set `status: review-due` if not already |
| 90–364 | Red flag + archive | Move to `archive/{year}/{path}`, leave forwarding stub |
| 365+ | Purge candidate | Surface to operator for human decision |

### 3. Build the report

```markdown
# Stale-doc audit — {repo} — {date}

## Summary

| Bucket | Count | Action available |
|--------|-------|------------------|
| Yellow flag (30-89d) | N | Auto-flag |
| Red flag (90-364d) | N | Auto-archive |
| Purge candidate (365+d) | N | Manual review |

## Yellow flags

- `path/to/doc.md` (45d past, owner: ALICE)
- ...

## Red flags

- `path/to/doc.md` (120d past, owner: BOB)
- ...

## Purge candidates

- `path/to/doc.md` (520d past, owner: CAROL)
  - Last commit: SHA on YYYY-MM-DD
  - Last meaningful change: HHA
  - Recommended action: review with owner; restore-with-renewal,
    delete (if no historical value), or extend with override_reason
```

### 4. Apply actions (if `apply_actions = true`)

For yellow flags: open a single PR per repo:
- Add `status: review-due` to frontmatter of affected docs
- Update HTML banner config (if MyST site has staleness rendering)
- PR title: `eka-bot: flag {N} review-due docs`

For red flags: open a single PR per repo:
- Move file to `archive/{year}/{path}`
- Leave forwarding stub in original location
- PR title: `eka-bot: archive {N} stale docs`

For purge candidates: do NOT modify files. Add to a
`PURGE-CANDIDATES.md` in the audit folder; tag the owners.

### 5. Notify owners

For each owner with at least one flagged doc, surface in the next
weekly digest:

> "`@OWNER`: {N} documents you own are flagged review-due or stale.
> Top 3: {paths}. See the stale-doc audit report for details."

## Validations

- Report matches the on-disk state
- Yellow-flag PR doesn't change content, only frontmatter
- Red-flag PR moves files atomically (no partial state)

## Outputs

| Output | Location |
|--------|----------|
| Audit report | `audit/stale-{yyyy-mm-dd}.md` |
| Yellow-flag PR | One per repo |
| Red-flag PR | One per repo |
| Purge candidate list | Surfaced to operator inline |

## Failure handling

| Failure | Recovery |
|---------|----------|
| Repo has no frontmatter (not EKA-conformant) | Refuse; suggest bootstrap |
| Many docs would be archived (>20% of repo) | Pause; require operator confirmation |
| Author of affected docs has left the org | Reassign owner via `_meta/ownership.yml` before flagging |
