# Runbook: Annual Classification Audit

**When to run:** Once per year, typically Q1.
**Who runs it:** Compliance lead + EKA program owner.
**Duration:** 1 week of part-time effort.
**Companion skill:** [`eka-classification-audit`](../skills/eka-classification-audit.skill.md) — automates inventory and discovery.

## Pre-conditions

- [ ] Previous year's audit report is filed and was acted upon
- [ ] All quarterly access reviews for the past year are filed
- [ ] CODENAMES.yml is current

## Procedure

### 1. Run the audit skill (Day 1)

```bash
eka skill invoke eka-classification-audit \
  --target-year {YEAR}
```

Produces a draft audit report in `{L2-repo}/audit/annual-{YEAR}.md`.

### 2. Review skill output (Day 2-3)

Walk through each section:

- Inventory delta — explain large changes (new repos, mass
  archival, etc.)
- Domain distribution drift — investigate any > 25% YoY shift
- Stale-doc trend — concerning if growing
- Override-reason sample — flag suspect overrides
- Codename discipline findings — fix mechanically
- Access review summary — confirm no gaps
- Erasure log — confirm all requests fulfilled
- CIS Control 3 self-assessment — update statuses honestly

### 3. Land mechanical fixes (Day 3-4)

The skill opens PRs for mechanical findings. Review and merge:
- Frontmatter fixes
- Codename-in-filename fixes (rename via PR)
- Stale-doc bulk renewal or archive

### 4. Resolve non-mechanical findings (Day 4-5)

For each finding requiring human judgment:
- Assign owner + due date
- Track in Plane (or equivalent) for follow-through

### 5. Sign off (Day 5)

The audit report's sign-off section:

```markdown
## Sign-off

| Role | Name | Date |
|------|------|------|
| Compliance lead | ... | YYYY-MM-DD |
| Engineering lead | ... | YYYY-MM-DD |
| Privacy admin | ... | YYYY-MM-DD |
```

Land via PR. Status → `approved`.

### 6. Publish summary for leadership (Day 5+)

A condensed executive-summary version of the audit (the dashboard
deltas and top recommendations) goes to leadership in the next
ops meeting.

## Verification

- The audit report is committed and signed off in the L2 repo
- All mechanical-fix PRs are merged
- Non-mechanical findings have assigned owners
- The report's `next_review` is set to ~365 days out

## Recovery scenarios

### Recovery: audit reveals systemic miscalassification

If > 10% of sampled overrides are wrong, the domain baselines may
be miscalibrated. Schedule a baseline-review project (not part
of the audit; separate effort).

### Recovery: audit reveals access drift

If quarterly access reviews aren't being run on cadence, fix
the cadence reminder + assign a process owner before closing
the audit.
