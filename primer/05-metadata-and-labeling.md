(chap-metadata-and-labeling)=
# 05 — Metadata and Labeling

This chapter specifies the frontmatter schema (the ISO 27002 5.13
labeling primitive of EKA), the validation hooks that enforce it,
and the supporting YAML files at each repo's root.

Contents:

- [Frontmatter schema](#sec-frontmatter)
- [CLASSIFICATION.yml schema](#sec-classification-yml)
- [CODENAMES.yml schema](#sec-codenames-yml)
- [manifest.md template](#sec-manifest)
- [Pre-commit hooks](#sec-pre-commit)
- [Validation in CI](#sec-ci-validation)

---

(sec-frontmatter)=
## Frontmatter schema

Every markdown file in an EKA-using repo begins with YAML frontmatter.
EKA-specific fields are **namespaced under `options.eka.*`** to avoid
"extra keys ignored" warnings from mystmd and to coexist cleanly with
mystmd-native fields (title, description, authors, date, tags, etc.):

```yaml
---
# mystmd-native (top level)
title: "Document title — descriptive, sentence case"

# EKA-specific (under options.eka)
options:
  eka:
    schema: eka.v1                       # EKA schema version this doc conforms to
    domain: business                     # public | customer | people | business | product | operational
    classification:
      C: MODERATE                        # LOW | MODERATE | HIGH
      I: MODERATE
      A: LOW
    tier: L1                             # derived from classification + data_subjects
    owner: jdoe@example.com              # email or @github-handle
    status: draft                        # draft | review | approved | review-due | superseded | archived
    last_reviewed: 2026-05-15
    next_review: 2027-05-15
    review_cadence: 365d                 # parsed: NNd / NNw / NNm / NNy

    # === Required at L2+ ===
    codename_refs: []                    # list of codes referenced in this document
    override_reason: null                # required if classification differs from domain baseline

    # === Required when applicable ===
    data_subjects: []                    # list of EMP-NNN / CAND-NNN if individuals are mentioned

    # === Optional fields ===
    labels: []                           # free-text tags for search
    related:                             # cross-references using EKA URI schemes
      - repo:other-repo/path/file
      - drive:1abc...
      - plane:proj-NNN
      - link:https://...
    replaced_by: null                    # set when status=superseded
    supersedes: null                     # the previous doc this replaces
    notes: null                          # author-only freeform notes
---
```

### Why `options.eka.*` and not top-level fields

The mystmd frontmatter parser recognizes a fixed set of fields
(title, description, authors, date, keywords, tags, …) and emits
"extra keys ignored" warnings for anything else. mystmd's
intended catch-all for tool-specific metadata is the `options:`
field. Nesting under `options.eka.*` accomplishes three things:

1. **Zero warnings** when building the site, PDF, or DOCX.
2. **Coexistence** with future tooling that uses other `options.*`
   namespaces (e.g., `options.thebe.*` for Jupyter integration).
3. **Future-proofing**: EKA v2 can add fields under `options.eka.*`
   without breaking other consumers of the same frontmatter.

mystmd-native fields (`title`, `description`, `authors`, `date`,
`keywords`, `tags`) stay at the top level. EKA-specific metadata
(everything else) goes under `options.eka.*`.

### Schema-specific variants

The `options.eka.schema` field tells validators which variant
applies:

| `schema` value | Used by | Additional required structure |
|----------------|---------|------------------------------|
| `eka.v1` | Standard documents | (none beyond base) |
| `eka.v1.manifest` | `_meta/manifest.md` files | (none; semantically distinguished by tooling) |
| `eka.v1.skill` | `*.skill.md` files in `spec/skills/` | adds `options.eka.skill.*` block |

For skill files specifically:

```yaml
---
title: "Skill: eka-bootstrap-org"
options:
  eka:
    schema: eka.v1.skill
    # ... standard doc metadata (domain, classification, tier, etc.) ...
    skill:
      skill_id: eka-bootstrap-org
      version: 1.0
      agents: [L1]
      side_effects: yes
      duration_estimate: 30-60 minutes
      audience: bootstrap operators
      human_required: no
---
```

### Field reference

| Field | Type | Required? | Description |
|-------|------|-----------|-------------|
| `title` | string | yes | Human-readable title; also used in TOC |
| `domain` | enum | yes | One of the six EKA domains |
| `classification.C` | enum | yes | Confidentiality impact: LOW / MODERATE / HIGH |
| `classification.I` | enum | yes | Integrity impact |
| `classification.A` | enum | yes | Availability impact |
| `tier` | enum | yes | L0 / L1 / L2 / L3; *derived from classification + data_subjects* |
| `owner` | string | yes | Single person owning the document's accuracy |
| `status` | enum | yes | Workflow state |
| `last_reviewed` | date | yes | ISO 8601 date when content was last validated |
| `next_review` | date | yes | When next review is due; computed from `last_reviewed + review_cadence` |
| `review_cadence` | duration | yes | How often this doc should be revalidated |
| `codename_refs` | list | yes at L2+ | Codenames the document references |
| `override_reason` | string | yes if non-baseline | Why classification differs from domain default |
| `data_subjects` | list | yes if applicable | Identifiers of individuals; triggers tier ≥ L2 |
| `labels` | list | no | Free-text tags |
| `related` | list | no | Cross-references with URI scheme |
| `replaced_by` | string | yes if status=superseded | Forward pointer |
| `supersedes` | string | no | Back pointer to predecessor |
| `notes` | string | no | Author-only notes |

### The URI scheme for `related`

| Scheme | Format | Resolves to |
|--------|--------|-------------|
| `repo:` | `repo:{repo-name}/{path/to/file}` | Another EKA repo |
| `drive:` | `drive:{drive-file-id}` | Google Drive file |
| `plane:` | `plane:{project-id}` or `plane:{issue-id}` | Plane ticket / project |
| `link:` | `link:https://...` | External URL |
| `secret:` | `secret:{vault-path}` | Pointer to live secret (L4); content not in docs |

The agent reads these and follows them according to its tier scope. A
tier-L1 agent following a `repo:{org}-company-docs/...` reference gets
"not in scope" rather than the content. The reference is preserved as
a navigation hint for humans with the right access.

### Tier derivation rule

The tier is *derived* from the classification + presence of data
subjects, not declared independently. The derivation rule:

```python
def derive_tier(classification, data_subjects):
    C, I, A = classification['C'], classification['I'], classification['A']

    # L3: any document with identifiable individuals
    if data_subjects:
        return 'L3'

    # L2: HIGH confidentiality
    if C == 'HIGH':
        return 'L2'

    # L1: MODERATE confidentiality, or HIGH integrity/availability
    if C == 'MODERATE' or I == 'HIGH' or A == 'HIGH':
        return 'L1'

    # L0: everything else
    return 'L0'
```

This is enforced by the pre-commit hook: an author cannot declare
`tier: L1` while declaring `classification.C: HIGH` — the hook will
fail the commit and tell the author what tier the classification
implies.

(sec-classification-yml)=
## CLASSIFICATION.yml schema

Lives at the root of every EKA-using repo:

```yaml
schema: eka.v1
repo:
  name: org-eng-docs
  visibility: internal                   # public | internal | private
  max_tier: L1                           # the highest tier this repo may contain
  default_domain: business
  default_classification:
    C: MODERATE
    I: MODERATE
    A: LOW
data_subjects_allowed: false             # at this tier, may any doc declare data_subjects?
codenames_required: false                # are codenames mandatory in paths and body?
codenames_file: null                     # path to CODENAMES.yml (set at L2+)
review_cadence:
  default: 365d
  by_domain:
    operational: 180d                    # runbooks reviewed more frequently
    customer: 90d
audit_log:
  enabled: true
  retention_days: 365
hooks:
  pre_commit:
    - eka.frontmatter_required
    - eka.tier_consistency
    - eka.classification_max
    - eka.codename_filenames
    - eka.review_cadence
    - gitleaks
```

The `hooks` list names the validators the pre-commit framework will
run. Each is implemented as a small Python script in the EKA helper
library (see [chapter 9](#chap-tooling)).

(sec-codenames-yml)=
## CODENAMES.yml schema

Detailed in [chapter 4](#chap-storage-and-naming) under
[Codename scheme](#sec-codenames). The schema validator confirms:

- Every code is unique within its class (no duplicate `C001`s)
- Mnemonics are unique across all classes (no Mars used for both
  customer and partner)
- Every code referenced in any document's `codename_refs:` resolves
  to a defined entry
- No codename collision with reserved words or English common words

(sec-manifest)=
## manifest.md template

The single most important document in any EKA repo. Read by every
agent at boot.

```markdown
---
title: "Manifest — what's in this repo and where else to look"
domain: business
classification: { C: LOW, I: HIGH, A: HIGH }
tier: L1
owner: platform@example.com
status: approved
last_reviewed: 2026-05-15
next_review: 2026-08-15
review_cadence: 90d
labels: [agent-context, navigation, eka-required]
---

# Manifest

## What this repo is

`org-eng-docs` is the L1 (internal) knowledge base for everyone at
{Org}. Read access: all employees via SSO. Write access: any
employee via PR. Pages site: https://docs.example.com/eng

## Tier and scope

- Maximum tier: L1
- Default domain: business
- Codenames required: no
- Data subjects allowed: no

## What lives here

| Folder | What | Owner |
|--------|------|-------|
| `onboarding/` | New-hire content, environment setup, conventions | People Ops |
| `architecture/` | Current-state architecture, ADRs | Platform |
| `runbooks/` | Operational procedures | Platform / SRE |
| `proposals/` | Forward-looking design docs (RFCs) | Engineering |
| `post-mortems/` | Incident reviews | Platform |
| `digests/` | Agent-generated weekly / monthly / quarterly summaries | Agents |

## What does NOT live here

- Customer-specific content → see L2 `org-company-docs`
- Employee performance / 1:1s → see L3 Drive folder
- Live secrets → see vault (out of scope)

## Other EKA stores in this org

| Tier | Store | URL | What |
|------|-------|-----|------|
| L0 | (not yet — deferred) | | |
| L1 | this repo | https://github.com/{org}/org-eng-docs | Eng-wide |
| L2 | `org-company-docs` | https://github.com/{org}/org-company-docs | Strategy, RFPs, threat models |
| L3 | Drive | drive://{org-drive-root} | People + customer per-record |

## External systems

| System | Purpose | Agent access |
|--------|---------|--------------|
| Plane | Tickets and project tracking | Read-only via MCP |
| Google Chat | Ephemeral conversation | On-demand summary via MCP |
| HRIS | Employee records | Out of scope for L1 agents |

## Agent boot routine

Any agent operating in this repo MUST:

1. Read this manifest first.
2. Read `_agents/{tier}.claude.md` for tier-specific guardrails.
3. Read `CLASSIFICATION.yml` for repo limits.
4. Refuse any operation that would write content above L1.
5. Refuse any operation referencing data_subjects.
6. Log every read and write to the audit log.

## Last verified

- Manifest accuracy: 2026-05-15
- Repo permissions: 2026-05-15 (quarterly access review)
- Pre-commit hooks installed: 2026-05-15
```

(sec-pre-commit)=
## Pre-commit hooks

EKA ships a `.pre-commit-config.yaml` with these hooks:

```yaml
repos:
  - repo: https://github.com/eka-spec/eka-hooks
    rev: v0.1.0                          # pinned version
    hooks:
      - id: eka-frontmatter-required
        # Every .md file (except _build/_meta exempt list) must have valid YAML frontmatter
      - id: eka-tier-consistency
        # tier field must match derive_tier(classification, data_subjects)
      - id: eka-classification-max
        # tier must not exceed CLASSIFICATION.yml's max_tier
      - id: eka-codename-filenames
        # at L2+, file paths must not contain real entity names from CODENAMES.yml's `name` field
      - id: eka-review-cadence
        # next_review must equal last_reviewed + review_cadence
      - id: eka-data-subjects-allowed
        # data_subjects: non-empty requires repo's data_subjects_allowed: true
      - id: eka-codename-refs-defined
        # every codename in codename_refs must exist in CODENAMES.yml
      - id: eka-related-uris-valid
        # related: URIs must parse and refer to known schemes
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

Each `eka-*` hook is a small Python script that reads the file's
frontmatter, applies the validation, and exits non-zero with a clear
error if it fails. The hook source is published as a reference
implementation alongside this spec.

Example hook output on failure:

```
$ git commit -m "Add Apex Retail Corp RFP response"

eka-codename-filenames......................................Failed
- hook id: eka-codename-filenames
- exit code: 1

  customer/rfps/{real-customer-name}-2026-q3.md
    └── File path contains real customer name "Apex Retail Corp" which appears in
        CODENAMES.yml as C001 with disclosure: acknowledged-public.
        L2 repos require codenames in paths.

  Rename to: customer/rfps/c001-2026-q3.md

eka-data-subjects-allowed...................................Passed
eka-tier-consistency........................................Passed
gitleaks....................................................Passed
```

(sec-ci-validation)=
## Validation in CI

Pre-commit hooks catch issues locally. CI re-runs them on every PR
to catch contributors who skipped hooks, plus a few additional
checks that need broader context:

- **Cross-repo reference validity** — `related: repo:other-repo/path`
  references actually resolve. Run as a nightly job rather than per-PR
  (the cross-repo check requires authenticated access to all EKA
  repos in the org).
- **Codename consistency across repos** — `C001` means the same thing
  in `org-company-docs` and any other L2+ repo. Centralized
  `CODENAMES.yml` (single source) avoids the divergence; the CI
  check confirms no drift.
- **Manifest freshness** — `_meta/manifest.md`'s `last_reviewed` is
  within `review_cadence` days; if not, fail (manifests stale by
  more than a quarter are a real audit finding).
- **Audit log integrity** — append-only verification on the audit
  log (no rewrites of past entries).

A reference GitHub Actions workflow for these checks is in
[chapter 9](#chap-tooling).

## What's contestable

- **YAML frontmatter** is verbose. Alternatives include TOML
  frontmatter (Hugo-style), JSON-LD blocks, or schemas embedded in
  HTML comments. YAML wins on (a) wide tool support and (b) human
  readability. The verbosity is the cost.
- **The derived-tier rule** is opinionated. Some organizations would
  invert (data subjects → L3 means *all* personnel records become
  L3, which is fine, but some prefer per-record granularity). EKA's
  rule is the safe default; granularity refinement is per-org.
- **CI validation as a nightly job vs. per-PR** for cross-repo
  checks is a trade-off between catch-speed and CI cost. Per-PR
  requires authenticated cross-repo reads in CI which is operationally
  noisy. EKA's recommendation: per-PR for in-repo checks, nightly
  for cross-repo.

[The lifecycle and review chapter](#chap-lifecycle-and-review)
covers what happens after a document is committed — review cadence,
staleness, archive, and erasure.
