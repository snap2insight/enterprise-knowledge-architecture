---
title: "Abbreviations"
options:
  eka:
    schema: eka.v1
    domain: business
    classification:
      C: LOW
      I: HIGH
      A: LOW
    tier: L0
    owner: eka-spec@example.com
    status: approved
    last_reviewed: 2026-05-17
    next_review: 2027-05-17
    review_cadence: 365d
    labels: [reference, abbreviations, eka-required]
    codename_refs: []
    data_subjects: []
---

# Abbreviations

This page is the canonical list of abbreviations used across the
EKA spec. Mystmd renders these as hover-tooltip expansions when
the abbreviation appears in body text of any project page.

## Where the data lives

The authoritative list is in
[`abbreviations.yml`](../../abbreviations.yml) at the project root,
referenced from `myst.yml` via `extends:`. mystmd reads the
project-level `project.abbreviations` map and emits hover tooltips
on every page where the term appears in body text — automatically,
on every page in the site, with zero per-page configuration.

## Adding a new abbreviation

Edit [`abbreviations.yml`](../../abbreviations.yml) at the project
root. Add the key (the acronym) and value (the full form). Re-build
the site; the expansion takes effect everywhere.

```yaml
# abbreviations.yml
version: 1
project:
  abbreviations:
    2FA: Two-Factor Authentication
    MFA: Multi-Factor Authentication
```

## Inline reference style

Where a term is used for the first time in any page, prefer the
full form with the abbreviation in parentheses:

> "Federal Information Processing Standard 199 (FIPS 199) defines
> the impact-rating vocabulary."

Subsequent uses on the same page may use the abbreviation alone;
mystmd renders the tooltip on hover.

## Categories

The list above mixes several categories:

- **EKA-specific:** EKA, L0–L4, MCP, etc.
- **Standards bodies:** NIST, ISO, CIS, etc.
- **Regulations:** GDPR, CCPA, HIPAA, etc.
- **Technical formats:** JWT, JSON, YAML, etc.
- **Security concepts:** RBAC, MFA, ZTA, STRIDE, etc.
- **Process / organizational:** RFC, RFP, SLA, etc.

Definitions for in-scope EKA terms are in the
[glossary](glossary.md); abbreviations here are the lookup table
for the acronyms themselves.
