(chap-storage-and-naming)=
# 04 — Storage and Naming

This chapter operationalizes [P3](#chap-principles): how files are
named, organized, and how codenames work.

Contents:

- [Repo structure per tier](#sec-repo-structure)
- [Folder organization within a repo](#sec-folder-structure)
- [File naming conventions](#sec-file-naming)
- [Codename scheme](#sec-codenames)
- [The CODENAMES.yml file](#sec-codenames-file)
- [Anti-patterns](#sec-naming-antipatterns)

---

(sec-repo-structure)=
## Repo structure per tier

A typical EKA-using organization has the following repos:

| Repo | Tier | Visibility | Pages enabled? | Notes |
|------|------|-----------|---------------|-------|
| `org-public` *(optional)* | L0 | Public | Public Pages | Only if you need a public docs site |
| `org-eng-docs` | L1 | Internal (or private with all-employees team access) | Authenticated Pages | Eng-wide content, proposals, runbooks |
| `org-company-docs` | L2 | Private, leadership-team access | Authenticated Pages (recommended) | Strategy, RFPs, financials, threat models |
| `org-product-docs` *(optional)* | L2 | Private, engineering-leadership access | Authenticated Pages | If product/IP content needs different access than business content |
| `org-platform-docs` *(optional)* | L2 | Private, platform / SRE access | Authenticated Pages | If operational content (infra plans, secrets inventories) needs different access |
| Drive folder hierarchy | L3 | Per-folder / per-file ACL | n/a (object store) | People data, customer per-record content |

For most startups, three Git repos + a Drive hierarchy suffices:
`org-eng-docs` (L1), `org-company-docs` (L2 with all confidential
content combined), Drive (L3). The split into separate L2 repos
(company / product / platform) is a scaling refinement, not
day-one need.

Each repo's root contains:

```
{repo-name}/
├── README.md                      # what this repo is, who reads it, link to EKA spec
├── CLASSIFICATION.yml             # max_tier + repo metadata, enforced by hooks
├── CODENAMES.yml                  # only at L2+ — entity codename mapping
├── .github/
│   └── workflows/
│       └── deploy.yml             # Pages build (if applicable)
├── .pre-commit-config.yaml        # frontmatter + tier validation
├── _meta/
│   ├── manifest.md                # the discovery index — see below
│   ├── glossary.md
│   └── ownership.yml
├── _agents/
│   ├── README.md
│   └── {tier-name}.claude.md      # agent guardrails for this tier
└── {content-folders}/             # see folder organization below
```

### CLASSIFICATION.yml

Every EKA-using repo declares its maximum allowed tier:

```yaml
# CLASSIFICATION.yml at the root of org-eng-docs
schema: eka.v1
repo:
  name: org-eng-docs
  max_tier: L1                     # pre-commit refuses content above this
  default_domain: business         # most content here is business-domain
  default_baseline:                # default classification for new files
    C: MODERATE
    I: MODERATE
    A: LOW
data_subjects_allowed: false       # this repo must not contain data subjects
codenames_required: false          # L0/L1 repos don't require codenames
review_cadence:
  default: 365d                    # annual review for L1 content
  override_allowed: true
audit_log:
  enabled: true
  retention_days: 365
```

The schema is parsed by pre-commit hooks and validation scripts. The
`schema: eka.v1` field declares conformance to this version of the
EKA spec.

### The manifest.md file

`_meta/manifest.md` is the **single most important file** in any
EKA-using repo. It's the index an agent reads first. It enumerates:

- Every other EKA repo in the org and what's in it
- Every external system (Drive folders, Plane projects, chat
  workspaces) and what they contain
- Cross-tier references ("for the L2 version of this content, see X")
- The agent boot-up routine for this tier

Without a manifest, an agent answering "where do I find the customer
RFP for our largest customer?" has to guess. With a manifest, the
agent looks up "RFP" → finds "L2 → company-docs → customer/rfps/"
→ knows it can't read that but can tell the human where it is.

A manifest template is in
[chapter 5 (metadata)](#chap-metadata-and-labeling).

(sec-folder-structure)=
## Folder organization within a repo

Folders organize content by **domain** (per [chapter 2](#chap-classification-model)).
Within a domain, sub-folders organize by **artifact type** or
**topic area**:

### L1 internal-docs example

```
org-eng-docs/
├── onboarding/                    # domain: business
│   ├── new-hire/
│   ├── conventions/
│   └── tooling/
├── architecture/                  # domain: product (de-sensitized)
│   ├── overview.md
│   ├── data-platform/
│   ├── ml-pipeline/
│   └── decisions/                 # ADRs
├── runbooks/                      # domain: operational (de-sensitized)
│   ├── incident-response/
│   └── per-service/
├── proposals/                     # domain: product
│   ├── index.md                   # active + past proposals
│   ├── _template/
│   └── {proposal-slug}/
├── post-mortems/                  # domain: operational
├── digests/                       # agent-generated
│   ├── weekly/
│   ├── monthly/
│   └── quarterly/
├── slides/                        # Marp presentation sources
└── _meta/                         # manifest, glossary, ownership
```

### L2 company-docs example

```
org-company-docs/
├── strategy/                      # domain: business
├── customer/                      # domain: customer (codenamed)
│   ├── rfps/
│   ├── security-questionnaires/
│   └── account-plans/
├── security/                      # domain: operational
│   ├── threat-models/
│   ├── vulnerabilities/           # current-state
│   ├── incident-postmortems/      # confidential parts
│   └── compliance/
├── financials/                    # domain: business
│   └── README.md                  # Drive index
├── board/                         # domain: business
├── product/                       # domain: product
│   └── designs/                   # IP-sensitive designs
├── artifacts/                     # rendered PDFs/DOCX for distribution
└── _meta/
```

### L3 Drive structure example

```
{org}-drive/
├── people-confidential/
│   ├── 1on1s/
│   │   ├── {lead-name}/           # lead-only folder ACL
│   │   │   └── {employee-codename}.md
│   ├── feedback/                  # per-employee folder, lead + employee ACL
│   ├── perf-reviews/
│   │   ├── draft/                 # lead-only
│   │   ├── calibrated/            # lead + calibration committee
│   │   └── delivered/             # lead + employee + manager
│   ├── comp/                      # CXO + HR only
│   └── hiring/
│       ├── active-loops/
│       └── archive/
├── customer-confidential/
│   ├── per-customer/              # one folder per customer, named with codename
│   │   ├── c001/                  # all C001-related per-record content
│   │   ├── c002/
│   │   └── ...
│   └── audit-log/
├── distribution/                  # rendered artifacts shipped externally
│   └── per-engagement/
└── archive/                       # ex-employees, closed projects, demoted content
```

(sec-file-naming)=
## File naming conventions

File names live in many interfaces — file tree, commit log, PR title,
CI output, URL. They leak by default.

### Universal rules

1. **Lowercase, hyphens.** `customer-rfp-2026-q3.md`, not
   `CustomerRFP_2026Q3.md`. Easier to type, easier to grep, no
   case-sensitivity bugs.
2. **No spaces.** `cust-status-update.md`, not
   `cust status update.md`.
3. **Date prefix where order matters** — for time-series content
   (digests, post-mortems, decisions): `2026-05-15-{slug}.md`. Date
   sorts chronologically; slug is descriptive.
4. **No internal abbreviations that obscure meaning** to the reader
   tier. `arch-doc.md` is fine in L1 (everyone there knows what arch
   means); `q3-strat-rev.md` is unhelpful even at L2.
5. **No leading underscores or dots** except for meta/build folders
   (`_meta`, `_build`). Files starting with `_` or `.` get filtered
   out by many tools.

### Tier-specific rules

**L0 (public)** — descriptive, optimized for SEO and human
discoverability. Examples: `getting-started.md`,
`api-reference.md`, `architecture-overview.md`.

**L1 (internal)** — descriptive; may include team or service names.
Examples: `pipeline-design.md`,
`onboarding-new-hire-checklist.md`,
`adr-0042-jwt-migration.md`.

**L2 (confidential)** — descriptive *for the type of artifact*, but
**externally-identifiable entity names are replaced by codenames**.
Examples (correct):

- `customer/rfps/c001-2026-q3.md` *(C001 is the codename)*
- `security/threat-models/payment-flow-2026.md` *(no entity name needed)*
- `customer/account-plans/c003-renewal.md`

Examples (incorrect):

- `customer/rfps/{real-customer-name}-2026-q3.md` ← real name in path
- `security/threat-models/examplecorp-checkout-mfa.md` ← real name + customer-specific feature
- `customer/c-examplecorp/...` ← real name in folder

**L3 (restricted, in object store)** — file names may be more
descriptive because Drive's per-file ACL gates visibility *and*
listing. But because Drive sharing links can be wide and link-sharing
defaults are surprising, **the L2 convention extends to L3**:
codenames for entities, descriptive for artifact type.

(sec-codenames)=
## Codename scheme

EKA's recommended scheme is **stable numeric IDs for paths,
mnemonic display names for body**:

| Use | Format | Example | Where |
|-----|--------|---------|-------|
| In paths, file names, frontmatter | Domain prefix + 3-digit sequence | `C001`, `P001`, `X001`, `EMP-042` | Wherever the entity is referenced structurally |
| In body text (first occurrence) | Mnemonic + parenthetical code | "Vesta (C001) has signaled interest" | Body paragraphs at L2+ |
| In body text (subsequent occurrences) | Mnemonic alone | "Vesta requested..." | Same document |

### Prefix conventions

| Prefix | Entity class | Example |
|--------|--------------|---------|
| `C` | Customer | `C001` (with mnemonic "Vesta") |
| `P` | Partner / vendor | `P001` (with mnemonic "Hermes") |
| `X` | Competitor | `X001` (with mnemonic "Sirius") |
| `EMP` | Employee (data subject) | `EMP-042` (no mnemonic — too small a pool to be useful) |
| `CAND` | Candidate (hiring) | `CAND-2026-W12-001` (year-week-sequence) |
| `BOARD` | Board member | `BOARD-001` |
| `INV` | Investor | `INV-001` |

The mnemonic for customers / partners / competitors uses themed
naming (Roman gods, constellations, gemstones — pick a scheme and
stick to it). The mnemonic exists for body-text readability;
insiders learn the top mappings within their first week.

### Why this scheme (and not a transformation cipher)

We considered transformation-based schemes — rot13, reverse-consonant,
short-hash — that let insiders mentally decode without a lookup. All
were rejected:

- Any transformation easy enough to mental-decode is also
  susceptible to frequency analysis when an outsider sees patterns
  ("which 4-letter code is paired with `*-rfp.md`? Probably their
  most active customer").
- Maintenance compounds: new entities need the rule applied
  consistently; rule changes require re-encoding history.
- A simple numeric ID + mnemonic gets you both: zero info in paths,
  pleasant readability in body.

### Disclosure status

`CODENAMES.yml` tracks each entity's disclosure status:

- `confidential` — the relationship's existence is not public; only
  codename in any internal doc
- `acknowledged-public` — the entity is publicly known to be a
  customer/partner/etc., so the *name* may appear in L0/L1, but
  relationship *details* are still confidential
- `historical` — relationship has ended; codename may be dropped but
  the mapping is retained for ~3 years for retroactive reference

(sec-codenames-file)=
## The CODENAMES.yml file

Lives at the root of every L2+ repo. The file is itself L2-classified
(`{C: HIGH}` because it cross-references real entities to internal
codes).

```yaml
schema: eka.v1.codenames
customers:
  C001:
    name: "Apex Retail Corp"
    mnemonic: "Vesta"
    disclosure: acknowledged-public
    since: 2024-Q3
    primary_owner: jdoe@example.com
    notes: "Public statement issued 2025-01 about partnership."
  C002:
    name: "Beacon Convenience"
    mnemonic: "Mars"
    disclosure: acknowledged-public
    since: 2025-Q1
    primary_owner: jdoe@example.com
  C003:
    name: "Citadel Distributors"
    mnemonic: "Juno"
    disclosure: acknowledged-public
    since: 2024-Q1
    primary_owner: jdoe@example.com
  C004:
    name: "{Confidential Customer 4}"
    mnemonic: "Apollo"
    disclosure: confidential
    since: 2025-Q4
    primary_owner: jdoe@example.com
    notes: "Active sales engagement. Public reveal target Q3 2026."

partners:
  P001:
    name: "Provider X"
    mnemonic: "Hermes"
    disclosure: confidential

competitors:
  X001:
    name: "Competitor Y"
    mnemonic: "Sirius"
    disclosure: confidential

employees:
  EMP-001:
    # employee names are not stored here; use the HRIS for the mapping.
    # The CODENAMES.yml *registers* the existence of the code, not the identity.
    code_only: true
    department: engineering
```

Two design notes:

1. **Employee mappings are NOT in CODENAMES.yml.** Employee
   identifiers (`EMP-042`) reference the HRIS as the source of
   truth. CODENAMES.yml only registers that the code exists; the
   actual mapping to "Sarah Chen" lives in the HRIS with proper
   access controls. This keeps people-data out of the L2 repo
   even at the metadata level.
2. **Confidential customers** are named with placeholder strings
   (`"{Confidential Customer 4}"`) rather than real names. Even
   inside CODENAMES.yml, an active confidential engagement gets
   placeholder-only until it's publicly disclosed. This protects
   against the "CODENAMES.yml itself leaks" failure mode.

(sec-naming-antipatterns)=
## Anti-patterns to avoid

| Anti-pattern | Why bad | Better |
|--------------|---------|--------|
| `customer/examplecorp/Q3-RFP.md` in an L2 repo | Real customer name in path | `customer/rfps/c001-2026-q3.md` |
| `1on1-sarah-2026-05.md` in any repo | Employee name in path | `1on1/emp-042/2026-05.md` (in Drive with proper ACL) |
| `urgent-vuln-do-not-share.md` | Filename signals sensitivity, ironically inviting curiosity | Descriptive name; classification carried by frontmatter |
| `tmp-notes-2.md` | Non-descriptive; will outlive its author's memory of what it is | `incident-2026-05-12-pipeline-stall-notes.md` |
| `john_smith_perf_2026.docx` | Person name + perf in filename | `emp-042-perf-2026-q2.md` in Drive with delivered/lead ACL |
| `final-final-v3.md` | Versioning by filename is a Git anti-pattern | One filename, history in Git |
| `customer1.md` | Generic non-codename that drift-aligns with real-customer order | `c001-{descriptive-artifact-type}.md` — codenames are stable across docs |

## What's contestable

- **The numeric-code + mnemonic split** adds one indirection (look up
  the mnemonic). Some teams find this annoying. The alternative is
  "numeric codes only," which is fine but harder to read in long
  documents. EKA recommends the split; teams may simplify.
- **The mnemonic theme is your choice.** Roman gods, constellations,
  gemstones, plants, fictional characters — any closed set without
  obvious mapping to real entities works. Avoid themes that are
  themselves sensitive (no political figures, no current
  celebrities).
- **L3 file-name conventions inheriting from L2** is a precaution
  some teams find unnecessary. Drive's per-file ACL does gate
  visibility tightly. EKA's position: link-sharing defaults change,
  ACL configurations drift, the precaution is cheap.

[The metadata and labeling chapter](#chap-metadata-and-labeling)
specifies the full frontmatter schema and the validation hooks that
enforce these rules.
