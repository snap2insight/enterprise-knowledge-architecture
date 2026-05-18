# EKA Specification

> The **how** of Enterprise Knowledge Architecture. Schemas,
> templates, skills, hooks, runbooks — everything an implementer
> (human or AI) needs to produce an EKA-conformant deployment.

This section is **prescriptive and machine-readable** wherever
possible. It is not narrative. The narrative explanation of each
choice lives in [the primer](../primer/).

## Spec layout

```
spec/
├── README.md                   # this file
├── conformance.md              # what it means to be EKA-conformant
├── schemas/                    # JSON Schema — machine-readable definitions
│   ├── frontmatter.schema.json
│   ├── classification-yml.schema.json
│   ├── codenames-yml.schema.json
│   └── manifest.schema.json
├── templates/                  # drop-in files; rename and customize
│   ├── repo-skeleton/          # full repo scaffold per tier
│   │   ├── README.template.md
│   │   ├── CLASSIFICATION.template.yml
│   │   ├── CODENAMES.template.yml
│   │   ├── _meta/manifest.template.md
│   │   ├── _agents/README.md
│   │   ├── .pre-commit-config.template.yaml
│   │   └── .github/workflows/deploy.template.yml
│   ├── content-types/          # frontmatter pre-filled per content type
│   │   ├── proposal.template.md
│   │   ├── runbook.template.md
│   │   ├── adr.template.md
│   │   ├── post-mortem.template.md
│   │   └── digest.template.md
│   └── claude-md/              # tier-scoped agent guardrails
│       ├── L1.claude.template.md
│       ├── L2.claude.template.md
│       └── L3.claude.template.md
├── skills/                     # agent-actionable workflow definitions
│   ├── README.md
│   ├── eka-bootstrap-org.skill.md
│   ├── eka-bootstrap-repo.skill.md
│   ├── eka-classify-doc.skill.md
│   ├── eka-new-doc.skill.md
│   ├── eka-review-doc.skill.md
│   ├── eka-erasure.skill.md
│   ├── eka-audit-stale.skill.md
│   └── eka-classification-audit.skill.md
├── hooks/                      # pre-commit hook reference implementations
│   ├── README.md
│   ├── eka_frontmatter_required.py
│   ├── eka_tier_consistency.py
│   ├── eka_classification_max.py
│   ├── eka_codename_filenames.py
│   ├── eka_review_cadence.py
│   ├── eka_data_subjects_allowed.py
│   └── eka_codename_refs_defined.py
├── ci/                         # CI workflow definitions
│   ├── README.md
│   ├── pre-commit-config.yaml
│   └── github-actions/
│       ├── eka-validate.yml
│       ├── eka-pages-deploy.yml
│       └── eka-weekly-digest.yml
├── operations/                 # runbooks for ongoing operations
│   ├── README.md
│   ├── access-review.runbook.md
│   ├── erasure.runbook.md
│   ├── offboarding.runbook.md
│   ├── codename-management.runbook.md
│   └── annual-audit.runbook.md
└── reference/                  # supporting reference material
    ├── error-codes.md          # canonical error messages from hooks
    ├── uri-schemes.md          # the related: URI vocabulary
    └── glossary.md
```

## How to use this spec

### As a human implementer

Read top to bottom, in this order:

1. [Conformance](conformance.md) — the testable bar
2. [Schemas](schemas/) — the machine-readable definitions
3. [Templates / repo-skeleton](templates/repo-skeleton/) — copy
   these into your new EKA repo
4. [Skills](skills/) — read the bootstrap skill to understand the
   workflow; later you'll invoke skills as agent prompts
5. [Hooks](hooks/), [CI](ci/), [Operations](operations/) — install
   and operate

### As an AI agent (bootstrap mode)

The agent's entry point is one of:

- [`eka-bootstrap-org`](skills/eka-bootstrap-org.skill.md) — set up
  an entire EKA-conformant organization (multiple repos + Drive
  hierarchy + agent homes) from a blank slate
- [`eka-bootstrap-repo`](skills/eka-bootstrap-repo.skill.md) —
  set up a single new EKA-conformant repo within an existing
  organization

The skill files describe the inputs, steps, validations, and
outputs. An agent invokes the skill (i.e., reads the skill file
into context, then executes) and reports back.

### As an AI agent (operating mode)

The agent's operating context is the tier-appropriate CLAUDE.md
in the agent's home directory. The CLAUDE.md references this spec
for any operation not covered by examples.

The most-invoked operating-mode skills:

- [`eka-classify-doc`](skills/eka-classify-doc.skill.md) — classify
  an existing document
- [`eka-new-doc`](skills/eka-new-doc.skill.md) — author a new
  document with the right frontmatter for the target tier
- [`eka-review-doc`](skills/eka-review-doc.skill.md) — review an
  existing doc for tier-appropriateness

## Conformance levels

A deployment is **EKA-conformant** if it satisfies the requirements
in [conformance.md](conformance.md). Three conformance levels:

| Level | What it means | Use case |
|-------|---------------|----------|
| **L1 — Structural** | Schemas + repo layout + pre-commit hooks in place. No L3 store yet. | Minimum viable: an org that has only L1 content, hasn't yet established its L2/L3 needs |
| **L2 — Operational** | All of L1 plus L2 repo + codenames + per-tier agents | Most orgs after the 4-week rollout |
| **L3 — Fully tiered** | All of L2 plus L3 object store with per-file ACL + JIT for sensitive sub-tiers + complete audit-log retention | Orgs handling people-confidential or customer-record content |

A deployment can claim partial conformance ("EKA L2-conformant"). A
deployment cannot claim higher than its highest implemented tier.

## Versioning

This spec is **`eka.v1`**. Every machine-readable file
(`CLASSIFICATION.yml`, `CODENAMES.yml`, etc.) declares its schema
version explicitly:

```yaml
schema: eka.v1
```

Breaking changes increment to `eka.v2`. The reference Python
implementation (`eka-helpers`) is versioned independently.

## Multi-runtime agent compatibility

EKA is **runtime-agnostic**. The CLAUDE.md filename is the only
Claude-specific convention; the content is portable to any agent
runtime. Adaptation patterns:

| Runtime | How EKA materials map |
|---------|----------------------|
| Claude Code | `~/agents/{tier}/CLAUDE.md` auto-loaded; skills invoked via `Read` on `.skill.md` files |
| OpenAI Assistants API | CLAUDE.md body → `instructions` parameter; skills passed as user-message context when invoked |
| LangChain / LangGraph | CLAUDE.md body → `SystemMessage`; skills wrapped as `Tool`s that read their own definitions |
| Custom agent | Read CLAUDE.md at boot; prepend to system prompt; load skill file content on demand |

A fresh agent of any runtime onboards via the
[`eka-agent-onboarding`](skills/eka-agent-onboarding.skill.md)
skill. That skill describes the boot routine in
runtime-independent terms.

The EKA spec deliberately uses markdown (the lingua franca across
agent runtimes) for all agent-facing content. JSON Schema for
machine validation. Python is the reference language for hooks
but the contract is implementation-agnostic.

## What's deliberately not in this spec

- **The HRIS schema** — how an org tracks employee identity is
  outside EKA. EKA uses `EMP-NNN` codes that resolve via HRIS.
- **The customer-relationship-management schema** — CRM tooling
  feeds entity names into EKA's CODENAMES.yml; the CRM itself is
  out of scope.
- **Identity provider configuration** — SSO setup, MFA enforcement,
  JIT-access tooling are all platform-engineering concerns. EKA
  defines *what* access control should produce; not *how* it's
  implemented in your IDP.
- **Production runtime secrets** — anything at L4 (live API keys,
  database passwords) is outside the docs system. EKA documents
  reference L4 with pointers (`secret:vault/path`) but does not
  hold the values.

## Next

If implementing: start with [conformance](conformance.md).
If bootstrapping via an agent: invoke
[`eka-bootstrap-org`](skills/eka-bootstrap-org.skill.md).
