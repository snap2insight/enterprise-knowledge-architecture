---
title: "Runbook — ACL as a first-class L3 artifact + automation"
options:
  eka:
    schema: eka.v1
    domain: operational
    classification:
      C: HIGH
      I: HIGH
      A: HIGH
    tier: L2
    owner: platform@example.com
    status: approved
    last_reviewed: 2026-05-17
    next_review: 2026-11-17
    review_cadence: 180d
    labels: [runbook, operational, acl, automation, eka-required]
    codename_refs: []
    data_subjects: []
    related:
      - link:https://github.com/GAM-team/GAM
      - repo:enterprise-knowledge-architecture/spec/operations/access-review.runbook.md
---

# Runbook — ACL as a first-class L3 artifact + automation

**When to read:** Setting up EKA L3 storage; designing the access-management lifecycle.
**Who runs the automation:** Platform engineering + HR/IT integration owner.
**Companion:** [`access-review.runbook.md`](access-review.runbook.md) — what to do when automation is partial or missing.

## The principle

The original EKA model used **quarterly access reviews** as the
control: every 90 days, an operator manually reconciles team
membership against current org reality. This is a backstop, not a
control — between reviews, drift accumulates and risk grows.

**A better model: ACL state is itself a first-class L3 artifact,**
versioned, queried, and updated by the same authoritative signals
that drive org reality (HRIS events, customer-engagement
lifecycle, hiring-loop opens/closes).

Specifically:

- The **canonical ACL state** lives as YAML files in the L3 store
  (Drive `{org}-eka/people-confidential/_acls/` and equivalent).
- **Automation** propagates HRIS state → ACL files → Workspace
  groups → Drive ACLs (and GitHub team memberships).
- **Periodic review** becomes a verification activity (does the
  automation match reality?) rather than the primary control.

This runbook describes the pattern. It is **aspirational** for most
startups — implement progressively.

## The ACL artifact

Every Workspace group (or GitHub team) has a YAML descriptor in
the L3 store. Schema:

```yaml
# Example: {org}-eka/people-confidential/_acls/1on1-leads.yml
---
group:
  email: 1on1-leads@example-co.com
  display_name: "1on1 Leads (eng managers)"
  description: "Engineering managers who hold 1:1s with direct reports."
  visibility: secret                       # secret | closed | open
  tier_scope: L3                           # the EKA tier this group operates within

members:
  # Populated either manually (Excel/CSV import) or by automation
  # from HRIS. Each member entry should resolve via HRIS to an active
  # employee in the named role.
  - email: alice@example-co.com
    role: manager                          # role within the group (manager | member)
    source: hris                           # how the membership was added
    added_at: 2026-04-01
    last_verified: 2026-05-17
  - email: bob@example-co.com
    role: member
    source: manual
    added_at: 2026-05-15
    last_verified: 2026-05-17

policy:
  # Joining conditions: an employee should be added when these are met.
  join_conditions:
    - "department == 'engineering'"
    - "role.includes('manager')"
  # Leaving conditions: an employee should be removed when these are true.
  leave_conditions:
    - "employment_status != 'active'"
    - "department != 'engineering' OR role does not include 'manager'"

drive_acls:
  # Folders this group has access to, with permission level.
  - path: "people-confidential/1on1s/{lead-handle}/"
    permission: editor
    note: "Per-lead folder; the group itself doesn't grant access — individual lead grants do. This is documentation."

audit:
  last_reconciled_at: 2026-05-17T14:32:00Z
  reconciliation_source: workspace-admin-api
  drift_detected: false
```

Properties:

- The **`policy.join_conditions` / `leave_conditions`**: the
  authoritative rules. An automation engine evaluates these
  against HRIS state to determine who should be in the group.
- **`members.source`**: distinguishes automation-added from
  manual additions. Auditors can see at a glance which entries
  the automation owns.
- **`last_verified`**: each entry has a timestamp showing when
  the member was last confirmed as still meeting the join
  conditions.
- **`audit.last_reconciled_at`**: when the automation last
  ran end-to-end and confirmed Workspace state matches this file.

## Automation patterns (pick one or layer them)

### Pattern A — HRIS webhook (real-time)

**Trigger:** HRIS fires a webhook on employee join, leave, role
change, or department change.

**Flow:**
```
HRIS webhook → Lambda/CloudFunction → reconciler →
  for each ACL file: re-evaluate policy → update Workspace groups →
  commit updated ACL files to L3 Drive → audit-log entry
```

**Latency:** seconds to minutes from HRIS event to Workspace
update.

**Strengths:** real-time; tightest control.
**Weaknesses:** requires HRIS that supports webhooks (Rippling,
Workday, BambooHR all do; smaller HRIS may not); needs
reconciler infrastructure.

### Pattern B — SCIM provisioning (push from HRIS)

**Trigger:** HRIS pushes employee state changes via SCIM to
Workspace and/or GitHub Enterprise.

**Flow:**
```
HRIS → SCIM client → Workspace SCIM endpoint → group membership updated
                  → GitHub Enterprise SCIM → team membership updated
```

**Latency:** typically <1 hour; depends on SCIM cadence.

**Strengths:** standards-based; no custom code.
**Weaknesses:** SCIM mappings can be fragile; not all policy
expressions translate into SCIM rules.

### Pattern C — Scheduled reconciliation (cron)

**Trigger:** Hourly / daily cron job.

**Flow:**
```
cron → reconciler reads HRIS API + all ACL files →
  diff Workspace state ↔ expected state →
  apply additions/removals → commit changes → audit-log
```

**Latency:** up to one cron interval (typically 1 hour).

**Strengths:** simplest; works with any HRIS that has an API.
**Weaknesses:** drift window equal to the interval; departures
can leak access for up to that long.

### Pattern D — Excel import (semi-manual)

**Trigger:** Operator updates an Excel/CSV with the desired
membership; runs an import script.

**Flow:**
```
Operator edits CSV → gam update group --members file users.csv →
  ACL file regenerated from gam state → committed to L3
```

**Latency:** whenever the operator remembers to run it.

**Strengths:** zero infrastructure; appropriate for very small orgs.
**Weaknesses:** no real-time guarantee; drift between updates.

### Recommended progression

| Org size | Recommended pattern | Add-on |
|----------|---------------------|--------|
| 5–25 employees | D (Excel) + monthly verification | none yet |
| 25–100 | C (cron, hourly) | + alerts on unexpected drift |
| 100–500 | A (webhook) | + C as backstop |
| 500+ | A + B | + drift dashboards |

## Customer engagement stage → ACL breadth

For per-customer groups, ACL breadth is determined by the
customer's `engagement_stage` field in `CODENAMES.yml`. The
principle: collaboration with customer-relevant internal teams
should be enabled when the customer is **live**; restricted to
the account lead during earlier stages.

| Engagement stage | Who has access | Rationale |
|------------------|----------------|-----------|
| `pre-rfp` | Account lead only | Even the existence of the conversation is sensitive |
| `rfp` | Account lead only | Active proposal-writing; broader access creates contamination risk between competing engagements |
| `negotiation` | Account lead only | Contract terms not yet signed; broad access creates contractual disclosure risk |
| `live` | Account lead + `internal_team_groups` from CODENAMES.yml (typically: eng, data, product, etc.) | Collaboration with implementing teams is required for delivery |
| `historical` | HR + Legal + Compliance only | Archived; access only for retention / regulatory purposes |

Even at `live` stage, EKA tier discipline still applies to
specific content types about that customer:

| Content type | Tier | Access |
|--------------|------|--------|
| General per-customer engagement notes | L2 | All members of `account-{name}@` group (which includes internal teams when live) |
| Contract terms, commercial details | L2 (more restricted) or L3 | Subset of account-team group OR per-file ACL on Drive |
| Customer-identifiable records / raw data | L3 (Drive) | Per-file ACL — even within the broader account team |
| Public statements / case studies | L0/L1 | Anyone (post-customer-approval) |

The `engagement_stage` field in `CODENAMES.yml` is the
**authoritative driver** for the customer-group ACL breadth. The
reconciler (any of patterns A-D below) reads this field and
adjusts membership accordingly. A stage transition (e.g.,
`negotiation` → `live`) triggers a re-evaluation of the customer
group's `internal_team_groups`.

## Required immediate updates (when does ACL change synchronously?)

Regardless of automation pattern, certain events MUST trigger
**synchronous** ACL updates (not deferred to the next cron):

| Event | Action | Why synchronous |
|-------|--------|----------------|
| Employee termination (voluntary or involuntary) | Revoke ALL group memberships within minutes; revoke MCP / SSO tokens | Departure-day access creates the worst-case insider exfiltration risk |
| Role change with reduced access | Remove from no-longer-applicable groups; keep new-role grants | Drift here creates over-privileged windows |
| Customer engagement stage transitions (e.g., `negotiation` → `live` or `live` → `historical`) | Re-evaluate customer-group `internal_team_groups`; add/remove team membership accordingly | Drift between intended stage and actual access creates either over- or under-privileged windows |
| Customer relationship ends | Move customer-specific Drive folders to archive; set `engagement_stage: historical`; revoke account-team group memberships | Customer-data contractual obligations may require timely revocation |
| Hiring loop closes | Retire the hiring-loop group; archive candidate files | Per-loop access is time-bounded by design |
| Security incident (suspected compromise) | Suspend affected accounts; revoke their tokens; force re-auth | Standard IR practice |

These should fire from HR/IT runbooks (NOT from EKA's reconciler
alone), with EKA's reconciler as a secondary check.

## How periodic review changes

If automation is in place (any of patterns A–C), the quarterly
access review described in
[`access-review.runbook.md`](access-review.runbook.md) becomes a
**verification** rather than a primary control:

1. Confirm `audit.last_reconciled_at` is recent across all ACL
   files (no automation outages).
2. Spot-check 5% of memberships against HRIS state directly
   (catches reconciler bugs).
3. Spot-check 5% of Workspace state against ACL files (catches
   manual changes that bypassed the automation).
4. Review the `audit-log/access-changes.md` for the past quarter
   for unusual patterns.

This is a half-hour exercise rather than a half-day one.

Without automation, the quarterly review remains the full,
detailed reconciliation in `access-review.runbook.md`.

## EKA conformance interaction

[Conformance L2-R6](../conformance.md) requires "Access control
is RBAC … reviewed at least quarterly." Both automation-based
and manual-review-based deployments satisfy this — but they
generate different evidence:

| Deployment | Evidence for L2-R6 |
|------------|--------------------|
| Manual quarterly review | Quarterly review reports filed in audit/access-reviews/ |
| Automated + verification | Verification reports + `last_reconciled_at` timestamps + automation-run audit logs |

Either works; pick what matches your scale.

## Open questions for evolution

1. **Should EKA spec mandate automation at a given org size?**
   Current view: no — recommend, don't mandate. Some orgs have
   regulatory reasons to keep humans in the loop.
2. **Should the ACL artifact format be standardized as part of
   the EKA spec (so multiple implementations are interoperable)?**
   Worth considering for EKA v2; not yet in scope.
3. **How does this interact with JIT access for sensitive
   sub-tiers?** JIT grants are short-lived by definition;
   automation should suppress them from "drift" detection. ACL
   files should track only the persistent baseline.
