---
title: "EKA — Project overview"
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
    labels: [overview, index, eka-required]
    codename_refs: []
    data_subjects: []
---

# Enterprise Knowledge Architecture (EKA)

> *Enterprise knowledge architecture for the AI era — classified at
> source, verifiable by audit, shareable by tier.*

## Three audiences, three entry points

The content is organized into three top-level sections, each
optimized for a different audience.

### 📘 [Primer](primer/) — *for new readers, leaders, reviewers*

The **why and the what**. Narrative chapters that motivate the
framework, lay out its principles, classify data, and walk through
the lifecycle. Each chapter ends with a *"What's contestable"*
section calling out trade-offs.

### 📐 [Spec](spec/) — *for staff engineers, security reviewers, and AI agent implementers*

The **how**. Schemas, templates, hooks, skills, runbooks, and
operational procedures. Dense and prescriptive. Every artifact is
either machine-readable (JSON Schema, YAML, Python) or
template-ready (drop-in markdown, CLAUDE.md, CI workflow YAML).

### 🏢 [Reference implementation](reference-implementation/) — *generic worked example*

A fictional **Example Co** showing how an organization applies EKA
end-to-end. Use it as a template for your own deployment; replace
the placeholder names with yours.

## Reading paths by role

| Your role | Path |
|-----------|------|
| Engineering leader / CXO | [Primer 0–1](primer/00-introduction.md), [Roadmap](primer/10-implementation-roadmap.md), then skim [Spec README](spec/README.md) |
| Staff engineer / security reviewer | [Spec README](spec/README.md), [Conformance](spec/conformance.md), [Schemas](spec/schemas/), then primer chapters [2–7](primer/02-classification-model.md) for context as needed |
| Compliance / audit team | [Primer 2](primer/02-classification-model.md), [Primer 8](primer/08-compliance-mapping.md), [Spec Conformance](spec/conformance.md) |
| Knowledge architect / author | [Primer 4–6](primer/04-storage-and-naming.md), [Spec templates](spec/templates/) |
| Platform / SRE implementer | [Spec README](spec/README.md), [Spec hooks](spec/hooks/), [Spec CI](spec/ci/), [Spec operations](spec/operations/) |
| AI agent (bootstrap mode) | [Spec skills/eka-bootstrap-org](spec/skills/eka-bootstrap-org.skill.md) — invoke this and follow the workflow |
| AI agent (operating mode) | [Spec templates/claude-md](spec/templates/claude-md/) — the tier-appropriate CLAUDE.md is the operating context |

## The framework at a glance

```
┌─────────────────────────────────────────────────────────────────────┐
│  CLASSIFY                                                           │
│  Every document declares {Confidentiality, Integrity, Availability} │
│  using FIPS 199 (LOW / MODERATE / HIGH). Domain folder establishes  │
│  the default; files can override down with explicit reason.         │
└──────────────────────────────────────┬──────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TIER                                                               │
│  Public → Internal → Confidential → Restricted                      │
│  Tier is *derived* from classification + presence of data subjects, │
│  not declared independently.                                         │
└──────────────────────────────────────┬──────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STORE                                                              │
│  Public / Internal / Confidential → Git repos with tier-appropriate │
│    ACL.                                                             │
│  Restricted → Object store with per-file ACL (e.g., Google Drive).  │
│  Live secrets → not in docs at all (production-system controls).    │
└──────────────────────────────────────┬──────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ENFORCE                                                            │
│  Pre-commit hooks validate frontmatter + tier + naming.             │
│  Per-tier agents have scoped read/write access via MCP.             │
│  Quarterly review: classification drift, access review, erasure.    │
└──────────────────────────────────────┬──────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ATTEST                                                             │
│  Every frontmatter field maps to a control in NIST 800-53 / ISO     │
│  27002 / CIS / GDPR. Auditors get evidence from the same metadata   │
│  the agents use.                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

:::{tip} Read the primer first
The framework's terminology (tiers, domains, classification, codenames)
is defined progressively across the primer chapters. If you encounter
an unexplained term (e.g., "L1 internal" before you've read about
tiers), the [Primer Tier architecture chapter](primer/03-tier-architecture.md)
is the canonical introduction.
:::

## Core design choices

The framework defends specific positions on contested questions. The
short version of each — full reasoning is in the primer.

1. **Classification is per-document, not per-folder.** Folders give a
   *default*; documents can override. This lets a routine status update
   sit in a confidential folder as internal content, declared
   explicitly.
2. **The CIA triad is the universal classification language.**
   `{C, I, A}` ∈ `{LOW, MODERATE, HIGH}` per
   [FIPS 199](https://csrc.nist.gov/pubs/fips/199/final). Tier
   (Public / Internal / Confidential / Restricted) is *derived*.
3. **AI agents are first-class consumers.** Every choice is evaluated
   against "can an agent parse and reason about this reliably?"
4. **Per-file ACL is the responsibility of the object store, not Git.**
   Git's container is the repo; per-file controls live where the
   storage system supports them natively (Google Drive, S3 with object
   ACLs, SharePoint).
5. **Codenames at higher tiers.** File names and paths at confidential
   tiers never contain externally-identifiable entity names. A small
   `CODENAMES.yml` (itself confidential) maps stable codes to real
   entities.
6. **Staleness is graduated, not auto-elevating.** Overdue review →
   visual flag → archive → eventual purge candidate. No surprise
   access changes.
7. **No "search everything" at the top.** Cross-tier search is a leak
   vector. Each tier searches within itself; cross-tier reasoning
   happens by deliberate linking, not by indexing.

## How to use this spec

- **Engineering leaders:** read primer 0–1 + roadmap. The middle
  chapters are operational detail you'll delegate.
- **Knowledge architects / authors:** read primer 0–7.
- **Compliance / audit teams:** read primer 2, 8, plus spec conformance.
- **Implementers / SREs:** read all of primer 4–10, plus spec.

Each chapter ends with a **"What's contestable"** section calling out
choices reasonable people will disagree with. The framework defends
specific positions but flags the trade-offs deliberately for review.

## Versioning

| Component | Version |
|-----------|---------|
| EKA spec | `v1.0-draft` |
| Schema format | `eka.v1` (referenced in all YAML files) |
| Reference Python implementation (`eka-helpers`) | `v0.1.0` (planned — see below) |

### What `eka-helpers` is (planned)

A small Python library implementing the EKA hooks and CLI tools as a
reference implementation. Components:

- **Pre-commit hooks** (the eight enumerated in
  [`spec/hooks/`](spec/hooks/)) — reads frontmatter, validates against
  the JSON Schemas, emits standardized error messages
- **CLI tools** (`eka validate`, `eka new`, `eka audit`, `eka erasure`
  etc.) — wrappers around the schemas + hooks for common operator
  workflows
- **Skill executor** — given a `*.skill.md` file, runs the workflow
  with input validation
- **Conformance checker** (`eka validate --conformance L2 .`) — the
  programmatic version of [conformance.md](spec/conformance.md)

The library is **planned**, not yet shipped. Spec implementations in
other languages (Go, TypeScript, Rust) satisfying the same contract
are equally valid. The Python reference will arrive alongside the
v1.0 release.

## Status & feedback

This spec is **Draft for peer / leadership review**. Treat its
choices as *defended defaults*, not law. See [README](README.md) for
contribution guidelines.
