---
title: "PM-YYYY-MM-DD — INCIDENT_TITLE"
options:
  eka:
    schema: eka.v1
    domain: operational
    classification:
      C: MODERATE                          # raise to HIGH if customer-specific
      I: HIGH                              # post-mortems must be accurate
      A: MODERATE
    tier: L1
    owner: INCIDENT_COMMANDER
    status: approved
    last_reviewed: YYYY-MM-DD
    next_review: YYYY-MM-DD
    review_cadence: 1y
    codename_refs: []                      # codenames for affected customers (at L2)
    data_subjects: []
    labels: [post-mortem, incident]
    related: []
---

# PM-YYYY-MM-DD — INCIDENT_TITLE

> **Incident date:** YYYY-MM-DD HH:MM PT
> **Duration:** Nh Nm of impact; Nh Nm of mitigation
> **Severity:** SEV-N
> **Customer impact:** PERCENTAGE_OR_LIST (codenamed at L2)
> **Incident commander:** NAME
> **Reviewers:** NAME, NAME

## TL;DR

What happened, in one paragraph.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| HH:MM | First signal |
| HH:MM | Page fires |
| HH:MM | IC declared |
| HH:MM | Mitigation begins |
| HH:MM | Customer impact ends |
| HH:MM | All-clear |

## Impact

- Customer-side: PER_SEGMENT_DESCRIPTION
- Internal: PER_TEAM_DESCRIPTION
- Financial: DOLLARS or "n/a"
- Regulatory: NOTIFICATION_FILED or "n/a"

## Root cause analysis

What actually happened, technically. Don't blame people; describe
the system conditions that made the failure possible.

### Contributing factors

- Factor 1
- Factor 2

### Trigger

What event tipped the system from "vulnerable" into "incident."

## What went well

- ...

## What went poorly

- ...

## Action items

| # | Action | Owner | Due | Plane |
|---|--------|-------|-----|-------|
| 1 | DESCRIBE | OWNER | YYYY-MM-DD | plane:proj/NNN |
| 2 | DESCRIBE | OWNER | YYYY-MM-DD | plane:proj/NNN |

## Glossary of internal terms

(if any)

## Sign-off

| Role | Name | Sign-off date |
|------|------|---------------|
| Incident commander | NAME | YYYY-MM-DD |
| Service owner | NAME | YYYY-MM-DD |
| Engineering lead | NAME | YYYY-MM-DD |
