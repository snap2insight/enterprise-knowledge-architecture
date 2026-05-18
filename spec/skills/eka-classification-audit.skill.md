---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-classification-audit
      version: 1.0
      agents: [L2]                            # auditor needs L1+L2 read access
      side_effects: yes
      duration_estimate: 1-2 hours
      human_required: yes
---

# Skill: eka-classification-audit

## Purpose

Run the annual classification audit per
[`spec/conformance.md`](../conformance.md): inventory, domain
distribution, staleness, override-reason sampling, codename
discipline, access review summary, erasure-log review.

## When to invoke

- Annual cadence (recommended Q1 of each year)
- After a major reorganization or compliance event
- Pre-audit (customer / SOC 2 / ISO certification)

## Inputs

Required:

| Input | Type | Default |
|-------|------|---------|
| `target_year` | int | current year |
| `orgs_to_audit` | list of repos + drive roots | inferred from manifest |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `sample_rate` | 10% | For override-reason sampling |
| `output_repo` | L2 repo | Where to commit the audit report |

## Steps

### 1. Build inventory

For every repo in scope:

```python
inventory = {
  'total_docs': N,
  'by_tier': {'L0': N, 'L1': N, 'L2': N, 'L3': N},
  'by_domain': {'public': N, 'customer': N, 'people': N, 'business': N, 'product': N, 'operational': N},
  'by_status': {'draft': N, 'review': N, 'approved': N, 'review-due': N, 'superseded': N, 'archived': N},
}
```

Compare with prior year's inventory. Surface deltas.

### 2. Domain-distribution drift check

If a domain's share grew or shrank by >25% YoY, flag for
investigation. Possible causes:
- Real shift in work focus (legitimate)
- Misclassification drift (concerning — investigate sample)

### 3. Stale-doc summary

Run `eka-audit-stale` for each repo. Summarize:

- Yellow flags: N
- Red flags: N
- Purge candidates: N

Trend vs. prior year.

### 4. Override-reason sampling

For each repo, sample 10% of documents with non-null
`override_reason`. For each sampled doc:

- Is the reason still valid given current content?
- Should the classification be re-baselined upward / downward?

Output: list of suspect overrides with recommended actions.

### 5. Codename discipline (L2+ repos)

Run the file-name scan: `grep` each entity's `name` field from
CODENAMES.yml against every file path. Any match is a finding.

Run the body-text scan: for each document mentioning an entity
without the entity's code in `codename_refs`, flag for fix.

### 6. Access review summary

For each L2+ repo:

- List current team members of `{org}-{repo}-readers` team
- Compare with prior quarterly review record
- Flag any net additions / removals
- Confirm departures align with HR offboarding records

### 7. Erasure-log review

For each erasure event in the past year:

- Was the request fulfilled?
- Was the audit-log entry filed?
- Were retention exceptions documented?

Spot-check: pick one random erasure, attempt to find tombstones
in the relevant docs. Audit log integrity confirmed.

### 8. CIS Control 3 self-assessment

Reapply the CIS Control 3.1–3.7 status from
[`primer/08-compliance-mapping.md`](../../primer/08-compliance-mapping.md):

| Sub-control | Status |
|-------------|--------|
| 3.1 Data management process | green / yellow / red |
| 3.2 Data inventory | green / yellow / red |
| ... | ... |

### 9. Produce the audit report

Commit to `output_repo` at `audit/annual-{year}.md`:

```markdown
---
title: "Annual classification audit — {year}"
domain: operational
classification: { C: HIGH, I: HIGH, A: MODERATE }
tier: L2
owner: COMPLIANCE_CONTACT
status: approved
last_reviewed: {audit_date}
next_review: {audit_date + 1y}
review_cadence: 1y
labels: [audit, classification, annual, eka-conformance]
---

# Annual classification audit — {year}

## Executive summary

- N total documents across {N} stores
- Tier distribution: ...
- Stale-doc backlog: N (was N last year, ±N)
- Codename discipline: PASS / FAIL with N findings
- Access reviews: ALL CURRENT / N PAST DUE
- CIS Control 3 self-assessment: ...

## Detailed findings

(per section above)

## Recommended actions

| Priority | Action | Owner | Due |
|----------|--------|-------|-----|
| P0 | ... | ... | ... |
| P1 | ... | ... | ... |
| P2 | ... | ... | ... |

## Sign-off

| Role | Name | Date |
|------|------|------|
| Compliance lead | ... | ... |
| Engineering lead | ... | ... |
| Privacy admin | ... | ... |
```

### 10. Open the followup PRs

For each recommended action that's mechanical:
- Codename-discipline fix: PR per repo
- Stale-doc bulk renew: PR per repo
- Frontmatter corrections: PR per repo

For non-mechanical actions: surface to operator as a checklist.

## Validations

- Audit report is committed and signed off
- Followup PRs exist for mechanical findings
- CIS sub-control statuses are consistent with the actual repo state

## Outputs

| Output | Location |
|--------|----------|
| Audit report | `{output_repo}/audit/annual-{year}.md` |
| Followup PRs | One per mechanical recommendation |
| Compliance-evidence package | Optional: `{output_repo}/audit/evidence-{year}.md` aggregating links |

## Failure handling

| Failure | Recovery |
|---------|----------|
| Some repos inaccessible to agent | Report scope limit; partial audit; require operator to escalate to higher-tier agent |
| Inventory query times out | Chunk by directory; resume |
| Findings exceed action-list reasonable size (>50) | Group by category; escalate to operator for prioritization |
