---
title: "Manifest — what's in this repo and where else to look"
options:
  eka:
    schema: eka.v1
    domain: business
    classification: {C: LOW, I: HIGH, A: HIGH}
    tier: L1
    owner: OWNER_HANDLE
    status: approved
    last_reviewed: 2026-05-17
    next_review: 2026-08-17
    review_cadence: 90d
    labels: [eka-required, navigation, agent-context]
---

# Manifest

This document is the **agent boot file** and the **human discovery
index** for this repo. Read it first.

## What this repo is

REPO_NAME is the TIER (e.g., "L1 Internal") knowledge store for
ORGANIZATION. Read access: GROUP_DESCRIPTION via SSO. Write access:
GROUP_DESCRIPTION via PR. Pages site: PAGES_URL.

## Tier and scope

- **Maximum tier:** TIER (per `CLASSIFICATION.yml`)
- **Default domain:** DOMAIN
- **Codenames required:** YES/NO
- **Data subjects allowed:** YES/NO

## What lives here

| Folder | What | Owner |
|--------|------|-------|
| `onboarding/` | New-hire content, environment setup, conventions | OWNER |
| `architecture/` | Current-state architecture, ADRs | OWNER |
| `runbooks/` | Operational procedures | OWNER |
| `proposals/` | Forward-looking design docs (RFCs) | OWNER |
| `post-mortems/` | Incident reviews | OWNER |
| `digests/` | Agent-generated weekly / monthly summaries | (agents) |

ADJUST_FOLDER_LIST_TO_MATCH_REPO

## What does NOT live here

- Higher-tier content of type X → see REPO_OR_LOCATION
- Lower-tier content of type Y → see REPO_OR_LOCATION

## Other EKA stores in this org

| Tier | Store | URL | What |
|------|-------|-----|------|
| L0 | (status) | URL | What's there |
| L1 | this repo | URL | this repo's content |
| L2 | OTHER_REPO | URL | OTHER_REPO_CONTENT |
| L3 | Drive | drive://ROOT | DRIVE_CONTENT |

## External systems

| System | Purpose | Agent access |
|--------|---------|--------------|
| EXAMPLE: Plane | Tickets and project tracking | Read-only via MCP |
| EXAMPLE: Google Chat | Ephemeral conversation | On-demand summary via MCP |
| EXAMPLE: HRIS | Employee records | Out of scope for this repo's agents |

## Agent boot routine

Any agent operating in this repo MUST:

1. Read this manifest first.
2. Read `_agents/CLAUDE.md` for tier-specific guardrails.
3. Read `CLASSIFICATION.yml` for repo limits.
4. (If L2+) Read `CODENAMES.yml`.
5. Refuse any operation that would write content above the repo's
   `max_tier`.
6. Refuse any operation that violates `data_subjects_allowed` or
   `codenames_required`.
7. Log every read and write to the audit log.

## Last verified

- Manifest accuracy: 2026-05-17
- Repo permissions: 2026-05-17 (quarterly access review due
  NEXT_DATE)
- Pre-commit hooks installed: 2026-05-17
- Pages deployment last successful: SEE_GITHUB_ACTIONS

## Change log

| Date | Change |
|------|--------|
| 2026-05-17 | Initial manifest |
