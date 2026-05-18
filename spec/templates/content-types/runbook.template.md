---
title: "RUNBOOK_TITLE — When/why to run, what it does"
options:
  eka:
    schema: eka.v1
    domain: operational
    classification:
      C: MODERATE                          # raise to HIGH if runbook contains production specifics
      I: HIGH                              # runbooks must be trustworthy
      A: HIGH                              # runbooks must be available during incidents
    tier: L1
    owner: PLATFORM_OR_SRE_LEAD
    status: approved
    last_reviewed: YYYY-MM-DD
    next_review: YYYY-MM-DD
    review_cadence: 180d
    codename_refs: []
    data_subjects: []
    labels: [runbook, operational]
    related: []
---

# RUNBOOK_TITLE

> **When to run:** SHORT_DESCRIPTION
> **Who runs it:** ROLE
> **Estimated duration:** N minutes / hours
> **Last validated against production:** YYYY-MM-DD

## Pre-conditions

What must be true before running this runbook.

- [ ] Pre-condition 1
- [ ] Pre-condition 2

## Procedure

### Step 1 — DESCRIPTION

```bash
COMMAND_OR_ACTION
```

Expected result: WHAT_SHOULD_HAPPEN

If FAILURE_CONDITION: see [Recovery: SCENARIO](#recovery-scenario)

### Step 2 — DESCRIPTION

...

## Verification

How to confirm the runbook succeeded.

```bash
VERIFICATION_COMMAND
```

Expected output: ...

## Rollback

If the runbook needs to be reversed, here's how.

## Recovery scenarios

### Recovery: SCENARIO

What to do if Step N goes wrong.

## Related

- Incident postmortem PM-YYYY-MM-DD (if this runbook was created from an incident)
- ADR-NNN (if this runbook implements an architectural decision)
- Plane ticket: plane:proj/issue-NNN (if there's an active improvement)

## Change log

| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | NAME | Initial version |
