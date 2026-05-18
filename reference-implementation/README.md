---
title: "Reference Implementation — generic startup example"
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
    labels: [reference-implementation, example, eka-required]
    codename_refs: []
    data_subjects: []
---

# Reference implementation — a generic startup

> A fictional **Example Co** showing how EKA is applied end-to-end at
> a small / mid-size startup. Use this as a template: replace
> `Example Co` and the placeholder team / customer names with yours.

## Why this exists

The spec describes *what* and *how* in the abstract. A worked example
shows what choices look like when made concretely. Reading the
[reference implementation overview](00-overview.md) alongside
[primer 10 — implementation roadmap](../primer/10-implementation-roadmap.md)
gives you the full picture: the four-week rollout maps onto specific
artifacts that look like the ones here.

## About Example Co (the fictional company)

| Attribute | Value |
|-----------|-------|
| Industry | B2B SaaS (analytics / fintech / dev-tools — pick one that resembles yours) |
| Size | ~25 engineers, ~50 total employees |
| Stack | Polyglot (back-end + ML + frontend) on a major cloud (AWS / Azure / GCP) |
| Customer base | Mid-market + a handful of enterprise customers; some publicly acknowledged, some confidential |
| Stage | Series A / B; not yet public-company |
| Compliance posture | Driving toward SOC 2 Type II; selling into customers who run vendor security questionnaires |

Example Co's profile is deliberately middle-of-the-road. If your
organization is bigger, smaller, more regulated, or pre-PMF, the same
EKA principles apply — your concrete choices just shift.

## What's in this section

- [`00-overview.md`](00-overview.md) — Example Co's repo inventory,
  team structure, domain mapping, codename theme, and the L1/L2
  proposal-split pattern illustrated with a fictional "Auth v2"
  proposal
- [`01-confidential-references.md`](01-confidential-references.md) —
  Example Co's pointer page showing what lives at L2 and L3 (folder
  paths, not file names)

## What to substitute when adapting

| Placeholder in this section | Replace with your |
|-----------------------------|-------------------|
| `Example Co` | Real company name |
| `example-co` (slug) | Your org slug |
| `example-co.com` | Your domain |
| `acme-eng-docs`, `acme-company-docs` | Your repo names |
| `C001` (Vesta) / `C002` (Mars) / `C003` (Juno) | Real customer codenames per your `CODENAMES.yml` |
| Roman / Greek / Norse god mnemonics | Your chosen theme |
| "Auth v2 proposal" | Your equivalent flagship proposal |

## When your reference implementation diverges

Common divergences and how to handle them:

- **Smaller team (fewer than 15 engineers):** collapse L2 into L1 with
  team-protected sub-folders OR keep L2 but with read-write access to
  a single team
- **B2C company:** customer-data tier defaults to L3 with stricter
  per-record ACLs; expand the `customer` domain
- **Regulated industry** (healthcare, finance, fed contractor): add
  domain-specific compliance mapping (HIPAA, SOX, FedRAMP) on top of
  the base NIST mapping; revise tier boundaries per regulator
  expectations
- **Larger team (50+ engineers):** split L1 into per-team sub-repos
  with the meta-manifest tying them together; add per-team agent homes

The framework scales by adjusting domain / tier counts, not by
abandoning the principles.

## Adopting this for your organization

1. Fork or copy this reference implementation
2. Run a global find/replace for `Example Co` → your org name + slug
3. Recreate `CODENAMES.yml` with your customers (use a different
   mnemonic theme to avoid confusion)
4. Update the team / role names in `00-overview.md` to match yours
5. Replace the "Auth v2 proposal" example with one of your real
   proposals
6. Confirm the domain breakdown matches your organization's structure;
   add a 7th or collapse a domain as needed (see
   [primer 2 — classification model](../primer/02-classification-model.md))

The resulting implementation should serve as your team's onboarding
material when explaining the framework internally.
