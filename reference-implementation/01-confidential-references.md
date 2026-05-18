---
title: "Example Co — confidential-layer pointers"
options:
  eka:
    schema: eka.v1
    domain: public
    classification:
      C: LOW
      I: HIGH
      A: LOW
    tier: L0
    owner: eka-maintainer
    status: draft
    last_reviewed: 2026-05-17
    next_review: 2027-05-17
    review_cadence: 365d
    labels: [reference-implementation, example]
    codename_refs: []
    data_subjects: []
---

(chap-example-co-confidential-refs)=
# Example Co — confidential-layer pointers

> **This page is L0 (public).** In a real organization adopting EKA,
> the equivalent page would be L1 (internal) — but it would describe
> *only the folder paths* of L2 and L3 content, not the content itself.
> The example below shows the pointer convention.

## Why this page exists in the real-org case

When an authorized operator (or agent acting on their behalf) needs to
find content at a higher tier, they look at the pointer page for the
canonical location. **The pointer page itself contains no L2 or L3
content** — just the path. Unauthorized readers see "X exists at
location Y" — they do not gain access by reading this page.

## L2 content map (Example Co)

Located at: `example-co/company-docs` (private repo, team
`company-docs-readers`).

| Folder | Content type | Who has access |
|--------|--------------|---------------|
| `strategy/` | Strategy memos, OKRs, quarterly planning | Leadership team |
| `customer/rfps/` | RFP responses (codenamed by customer) | Leadership + account team |
| `customer/security-questionnaires/` | Customer-side security questionnaire responses | Leadership + security lead |
| `customer/account-plans/` | Per-customer engagement plans | Leadership + account team |
| `security/threat-models/` | Detailed threat models (the L2 half of split proposals) | Leadership + security lead |
| `security/vulnerabilities/` | Current-state vulnerability tracker | Leadership + security lead + platform |
| `security/incident-postmortems/` | Confidential incident details | Leadership + IR responders |
| `security/compliance/` | Audit reports, customer compliance evidence | Leadership + compliance contact |
| `financials/` | Revenue, burn, planning | CXO subset only (CODEOWNERS-gated within the repo) |
| `board/` | Board materials | CEO + named board liaisons |
| `product/designs/` | Sensitive product / IP designs | Leadership + engineering leads |

## L3 content map (Example Co)

Located at: Google Drive root folder
`Example Co Workspace/example-co-eka/`.

Pointers below are folder paths, not file paths. File names are not
enumerated in this pointer page — that would leak metadata.

| Drive folder | Content type | ACL group |
|--------------|--------------|-----------|
| `people-confidential/1on1s/{lead-handle}/` | 1:1 notes between lead and direct reports | Lead only (per folder) |
| `people-confidential/feedback/{EMP-NNN}/` | Per-employee feedback files | Lead + employee |
| `people-confidential/perf-reviews/{cycle}/draft/` | Lead-only draft reviews | Lead only |
| `people-confidential/perf-reviews/{cycle}/calibrated/` | Calibrated reviews | `perf-calibration` group |
| `people-confidential/perf-reviews/{cycle}/delivered/` | Final delivered reviews | Lead + employee |
| `people-confidential/comp/` | Compensation data | `cxo-comp` group |
| `people-confidential/hiring/active-loops/{CAND-id}/` | Active hiring loops | Hiring loop members per loop |
| `customer-confidential/per-customer/{codename}/` | Per-customer artifacts (contracts, custom configs, sensitive comms) | `account-{codename}` group |
| `distribution/per-engagement/` | Rendered artifacts shipped to customers | Per-engagement basis |
| `archive/ex-employees/` | Former-employee Drive content | HR + legal |
| `board/` | Board working files | Board + CEO |

## Cross-tier reference syntax

When a document in any tier needs to reference content in L2 or L3,
it uses an EKA URI scheme:

```yaml
related:
  - repo:example-co/company-docs/security/threat-models/auth-v2-detailed.md
  - drive:1abc...                     # Drive file ID (works only if the reader has Drive ACL)
  - drive-folder:example-co-eka/customer-confidential/per-customer/c001
```

In prose, references use markdown links pointing at folder paths,
not file paths:

```markdown
For the detailed threat model, see
[the L2 security folder](repo:example-co/company-docs/security/threat-models/).
Access requires `company-docs-readers` membership.
```

## How operators get access (Example Co's process)

**L2 access:**

- Add to `company-docs-readers` GitHub team
- Requested via: PR against the org-config repo OR email to org admins
- Approved by: existing team member (often the engineering lead)
- Audit: GitHub team-membership change is logged in the org audit log

**L3 access (per-folder):**

- Add to the appropriate Workspace group (`1on1-leads@`, etc.)
- Requested via: email to Workspace admin OR HR-managed group
  membership (preferred)
- Approved by: HR + the folder's primary owner

**L3 access (per-file via Drive's request-access):**

For files where folder-level ACL is too coarse:

- Operator clicks the Drive file, hits "Request access"
- File owner receives notification
- Owner approves with optional time-bounded JIT
- Audit: Workspace audit log records the share + the access

## What this page deliberately omits

To respect tier boundaries, this page does NOT contain:

- Specific file names in L2 or L3 (only folder paths)
- Counts of files / customers / employees per folder (small numbers
  can leak entity identity by elimination)
- Current `CODENAMES.yml` content
- Drive file IDs (which are guessable enough to merit caution)
- Names of confidential customers' codenames

Authorized readers fetch these specifics from their tier-appropriate
stores.

## What's contestable

- Listing folder structure at L1 is itself a small disclosure ("Example
  Co has a folder called `customer-confidential`" reveals they have
  confidential customer data). EKA's position: this level of disclosure
  is acceptable because folder names follow universal EKA conventions,
  not company-specific naming.
- Cross-tier references are themselves a small leak surface — the
  *existence* of an L2 document at a specific path is metadata. EKA's
  position: discoverability outweighs the metadata leak; without
  pointers, agents waste time guessing where content might live.
