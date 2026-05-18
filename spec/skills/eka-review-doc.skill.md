---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-review-doc
      version: 1.0
      agents: [L1, L2, L3]
      side_effects: no
      duration_estimate: 3-7 minutes
---

# Skill: eka-review-doc

## Purpose

Review an existing EKA document for:
1. Schema/frontmatter conformance
2. Classification appropriateness (right tier, right domain)
3. Codename discipline (at L2+)
4. Content quality (clarity, references, completeness)
5. Lifecycle markers (review-due, stale, archived correctly)

## When to invoke

- PR review for an EKA repo
- Quarterly content audits
- Operator asks "is this doc OK?"
- Automated nightly review (subset)

## Inputs

Required:

| Input | Type |
|-------|------|
| `document_path` | string |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `review_mode` | `full` | `full` \| `schema-only` \| `content-only` \| `lifecycle-only` |
| `target_audience` | derived from tier | Affects content-quality checks |

## Steps

### 1. Validate schema

Run `eka validate {document_path}` — report any failures.

### 2. Check classification appropriateness

Use [`eka-classify-doc`](eka-classify-doc.skill.md) on the body:
agent's recommended classification vs. declared classification.

If they disagree:
- Declared is too high: probably fine (downgrade-allowed)
- Declared is too low: **flag for the operator** with explanation

### 3. Check codename discipline (L2+)

For each entity name found in body (cross-reference with
`CODENAMES.yml`):

- First mention should use `Mnemonic (Code)` pattern
- File path should not contain real entity name
- All `codename_refs` in frontmatter actually appear in body
- All entities mentioned in body are in `codename_refs`

### 4. Check content quality

Lightweight heuristics:

- **Has an opening summary** (first paragraph or "## Summary" or
  "## TL;DR")
- **Cross-references use semantic refs** (`[](#label)`) where the
  spec recommends them
- **No broken external links** (where the agent can probe)
- **Code blocks are syntax-valid** for declared language
- **Tables render correctly** (no obvious markdown bugs)
- **Frontmatter `related:` field resolves** (URIs parse; targets
  exist within the agent's tier)

### 5. Check lifecycle

- Is `last_reviewed` plausible? (≥ creation date; ≤ today)
- Is `next_review = last_reviewed + review_cadence`?
- Is the doc past `next_review`?
- Is `status` appropriate (`draft` vs `approved` vs
  `review-due` vs `superseded`)?
- If `superseded`, is `replaced_by` populated?

### 6. Produce the review report

```markdown
# Review: {document_path}

## Schema validation
✅ Pass — all required fields present.
(or list failures)

## Classification check
✅ Declared L2 is consistent with content.
(or: ⚠️ Recommend L2; declared L1 may underclassify due to ...)

## Codename discipline (L2+ only)
✅ All entities use codenames; file path is conformant.
(or list issues)

## Content quality
- ✅ Has opening summary
- ⚠️ External link broken: https://...
- ✅ Cross-refs resolve

## Lifecycle
✅ Review cadence consistent. Document is 12 days from next review.
(or: ⚠️ 45 days overdue; flagged review-due)

## Summary
- Severity: pass | warn | fail
- Recommended actions: ...
```

## Validations

The review report is suitable for posting as a PR comment.

## Outputs

| Output | Format |
|--------|--------|
| Review report | Markdown, suitable for PR comment |
| Severity flag | `pass` \| `warn` \| `fail` |

## Failure handling

| Failure | Recovery |
|---------|----------|
| Document doesn't exist | Report; stop |
| Document is binary | Report unsupported; stop |
| Frontmatter is malformed YAML | Quote the syntax error; suggest fix |
| Agent's tier doesn't permit reading the doc | Refuse; recommend higher-tier agent |
