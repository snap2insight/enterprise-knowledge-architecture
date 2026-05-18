---
title: "Example Co — applying EKA"
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

(chap-example-co-overview)=
# Example Co — applying EKA

> A fictional company applying EKA end-to-end. Replace `Example Co`
> with your organization's name throughout. The structure and
> conventions transfer; the specific names and numbers won't.

## Example Co at a glance

- **Industry:** B2B SaaS (analytics / data platform — substitute yours)
- **Size:** ~25 engineers; ~50 total employees
- **Customer base:** Mix of mid-market and a few enterprise customers;
  three publicly acknowledged, several confidential
- **Stack:** Polyglot back-end, ML pipeline, web + mobile clients,
  major cloud provider
- **Compliance posture:** SOC 2 Type II in progress; customers run
  vendor security questionnaires
- **GitHub org:** `example-co`
- **Workspace:** Google Workspace

Example Co sells into customers with significant compliance overhead.
EKA adoption is driven by both internal need (knowledge fragmentation,
agent workflows) and a sales need (have evidence to show vendor
security reviews).

## Repo inventory

| Tier | Repo | Purpose | Pages site |
|------|------|---------|------------|
| L0 | (deferred) | If/when Example Co needs a public CMS, blog, or recruiting site, an `example-co-public` repo would land here | n/a |
| L1 | `example-co/eng-docs` | Eng-wide internal portal — onboarding, architecture, runbooks, proposals (L1 summary half) | Authenticated (internal-visibility) Pages |
| L2 | `example-co/company-docs` | Strategy, customer RFPs, threat models, financials index, proposals (L2 detail half) | Authenticated Pages, leadership-team-only |
| L3 | Google Drive (`Example Co Workspace`) | People-confidential + customer-per-record content | n/a (object store with native per-file ACL) |

For most startups, two Git repos plus a Drive hierarchy is enough.
Splitting L2 into multiple sub-repos (`product-docs`, `platform-docs`,
etc.) is a scaling refinement, not day-one need.

## Team structure & ACLs

GitHub teams in the `example-co` org:

| Team | Members | Repos read | Repos write |
|------|---------|-----------|-------------|
| `eng` | All engineers (~25) | eng-docs (internal visibility makes this implicit) | eng-docs |
| `company-docs-readers` | CEO, CTO, COO, VPE, lead engineers (~8) | eng-docs + company-docs | eng-docs (via `eng` membership) + company-docs |
| `leadership-only` | CEO, CTO, COO, founding team (~4) | Above plus financial / board content within company-docs (sub-folder ACL via CODEOWNERS reviewer-required gating) | Same |
| `platform` | Platform engineers (~3) | All of above | eng-docs + future platform-docs |

Drive ACL groups (Google Workspace groups):

| Group | Members | Drive folders |
|-------|---------|---------------|
| `1on1-leads@example-co.com` | Engineering managers (~4) | `people-confidential/1on1s/{their-name}/` per-lead |
| `perf-calibration@example-co.com` | Eng managers + VPE | `people-confidential/perf-reviews/calibrated/` |
| `cxo-comp@example-co.com` | CEO, CTO, COO | `people-confidential/comp/` |
| `account-{customer}@example-co.com` | Per-customer account team (one group per active customer) | `customer-confidential/per-customer/{codename}/` |

## Domain mapping for Example Co

| EKA domain | Example Co content categories |
|------------|--------------------------------|
| Public *(deferred)* | Future blog, OSS components, recruiting content |
| Customer Data | Customer-supplied records, customer-specific configurations, per-customer analytics outputs |
| People Data | Employee identifying information, performance reviews, 1:1 notes, hiring, compensation |
| Business Data | RFPs, customer contracts (commercial terms), revenue forecasts, board materials, OKRs |
| Product Data | Service architecture, ML model designs, pipeline algorithms, API designs, the "Auth v2" proposal |
| Operational Data | Infrastructure plans, runbooks, incident response, secrets inventory (pointers only), SRE on-call |

:::{note} Domain breakdown is *recommended*, not mandatory
Example Co uses six domains because that decomposition matches its
internal organization. Smaller companies may collapse Product +
Operational into a single "Engineering" domain. Larger or more
regulated organizations may split further (e.g., separate
"Customer-PHI" out of "Customer Data" for healthcare). See
[primer 2 — classification model](../primer/02-classification-model.md)
for the extensibility rules.
:::

## Codename theme & initial mapping

**Theme:** Roman gods for customers, Greek for partners, Norse for
competitors. Numeric codes for individuals (`EMP-NNN` / `CAND-NNN`).

Example `CODENAMES.yml` (in `company-docs` repo, L2-classified):

```yaml
schema: eka.v1.codenames

customers:
  C001:
    name: "Apex Retail Corp"      # acknowledged-public — real name OK in body
    mnemonic: "Vesta"
    disclosure: acknowledged-public
    engagement_stage: live
    since: 2024-Q3
    primary_owner: alice@example-co.com
    internal_team_groups:
      - eng@example-co.com
      - data@example-co.com
      - product@example-co.com

  C002:
    name: "Beacon Convenience"
    mnemonic: "Mars"
    disclosure: acknowledged-public
    engagement_stage: live
    since: 2025-Q1
    primary_owner: bob@example-co.com
    internal_team_groups:
      - eng@example-co.com
      - data@example-co.com

  C003:
    name: "{Confidential — disclosure pending}"
    mnemonic: "Apollo"
    disclosure: confidential
    engagement_stage: rfp
    since: 2025-Q4
    primary_owner: alice@example-co.com
    internal_team_groups: []   # rfp stage → account lead only

partners: {}
competitors: {}
employees: {}    # codes registered; mapping in HRIS
```

## Drive structure for L3

```
Example Co Workspace/example-co-eka/
├── people-confidential/
│   ├── 1on1s/{lead-handle}/
│   ├── feedback/{EMP-NNN}/
│   ├── perf-reviews/{cycle}/{draft|calibrated|delivered}/
│   ├── comp/
│   └── hiring/{active-loops,archive}/
├── customer-confidential/
│   ├── per-customer/{codename}/
│   └── audit-log/
├── distribution/per-engagement/
├── archive/
└── board/{cycle}/
```

ACLs per folder: per the EKA operations runbooks.

## The "Auth v2" proposal — example of L1/L2 split

Example Co's first major spec landed under EKA is "Auth v2" (modernize
the auth stack, add MFA, support offline mobile, etc.). It illustrates
the L1/L2 split pattern.

**L1 — executive summary** (in `eng-docs/proposals/auth-v2/`):

| File | Purpose |
|------|---------|
| `README.md` | Status, owners, summary |
| `00-executive-summary.md` | Goals, non-goals, decision log |
| `02-target-architecture.md` | High-level component view (de-sensitized) |
| `05-backward-compatibility-migration.md` | Phase plan |
| `08-test-scenarios.md` | Test matrix |
| `09-rollout-plan.md` | Phase plan + observability |

The L1 chapters do NOT contain:

- Production hostnames
- Threat-model details
- Specific attacker capabilities
- Detailed risk register
- Customer-specific security context

**L2 — detailed companion** (in `company-docs/product/designs/auth-v2/`):

| File | Purpose |
|------|---------|
| `README.md` | Why this content is L2 |
| `01-current-state.md` | As-is auth analysis with production specifics |
| `03-detailed-flows.md` | Detailed sequence diagrams (attack-surface) |
| `04-token-and-2fa-design.md` | Crypto + customer impact |
| `06-security-hardening.md` | Threat model |
| `07-data-model-and-api-spec.md` | Production schema + API surface |
| `10-security-posture.md` | Residual risks per customer |

The two halves cross-reference each other. An engineer reads the L1
summary and follows the `related:` link to the L2 detail when their
access permits. Reviewers from the broader eng team comment on L1;
leadership-team reviewers comment on L2.

## External system integrations

| System | Tier | Purpose | Agent access |
|--------|------|---------|--------------|
| Plane (self-hosted) | L1 metadata | Project tracking, sprint planning | L1 agent: read-only via MCP |
| Google Chat | L1 ephemeral | Team conversation | L1 agent: on-demand summary, operator-consent only |
| HRIS | L3 source-of-truth | Employee identity, comp data | No agent access |
| CRM (HubSpot / Salesforce / Linear depending) | L2 customer source | Sales pipeline, contact info | L2 agent: future MCP integration |
| Cloud key vault | L4 production | Live runtime secrets | No EKA agent access |

## Adoption notes for Example Co

This worked example assumes EKA is being adopted from a relatively
clean slate. If the organization has existing docs that need
migrating:

- **Wave 1** (most-touched, highest value): active runbooks,
  onboarding, recent design proposals
- **Wave 2** (active customer content): in-flight RFPs, threat models
- **Wave 3** (history): post-mortems, archived RFPs, past strategy

Content not touched in 12 months may stay where it is (legacy wiki,
old Drive folders) — migration cost exceeds value. Add a manifest
entry naming the legacy store.

## Substituting this for your organization

1. Replace `Example Co` and `example-co` throughout
2. Substitute your real customer names + theme for the codenames
3. Update the team list to match yours
4. Replace "Auth v2" with your real flagship proposal
5. Adjust the domain breakdown if needed (collapse or extend)
6. Confirm the L3 Drive structure matches your Workspace conventions
