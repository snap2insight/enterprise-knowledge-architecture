# EKA Pre-Commit Hooks

> Reference Python implementations of the hooks that enforce EKA
> conformance at commit time. Repository-level alternative
> implementations (Go, TypeScript, etc.) satisfying the same
> contract are equally compliant.

## Hook catalog

| Hook ID | Validates | Required for tier |
|---------|-----------|-------------------|
| `eka-frontmatter-required` | Every `.md` has valid frontmatter conforming to [`frontmatter.schema.json`](../schemas/frontmatter.schema.json) | L1+ |
| `eka-tier-consistency` | `tier == derive_tier(classification, data_subjects)` | L1+ |
| `eka-classification-max` | `tier <= CLASSIFICATION.yml::repo.max_tier` | L1+ |
| `eka-review-cadence` | `next_review == last_reviewed + review_cadence` | L1+ |
| `eka-data-subjects-allowed` | `data_subjects:` non-empty requires `data_subjects_allowed: true` | L1+ |
| `eka-related-uris-valid` | `related:` entries match known URI schemes | L1+ |
| `eka-codename-filenames` | File paths contain no real entity names from `CODENAMES.yml::*.name` | L2+ |
| `eka-codename-refs-defined` | Every `codename_refs:` entry exists in `CODENAMES.yml` | L2+ |

## Frontmatter namespace

As of EKA v1, all EKA-specific frontmatter fields are namespaced under
`options.eka.*` to coexist with mystmd's native frontmatter keys
without triggering "extra keys ignored" warnings:

```yaml
---
title: "..."
options:
  eka:
    schema: eka.v1
    domain: business
    classification: { C: MODERATE, I: MODERATE, A: LOW }
    tier: L1
    owner: ...
    status: approved
    last_reviewed: 2026-05-17
    next_review: 2027-05-17
    review_cadence: 365d
    codename_refs: []
    data_subjects: []
    labels: []
    related: []
---
```

Hook implementations read from `options.eka.*`. The reference
implementation in `eka_tier_consistency.py` includes a transitional
fallback to top-level keys for pre-migration files.

## Universal hook contract

Every hook implementation MUST:

1. **Read its inputs from `argv` or stdin** as pre-commit-framework
   specifies.
2. **Exit 0 on success, non-zero on failure.**
3. **Print a human-readable error on failure**, naming the file,
   the line (where applicable), the rule violated, and a
   suggested fix.
4. **Be idempotent** — running the hook twice in a row produces the
   same result.
5. **Be fast** — process ~1000 files in under 10 seconds. Slower hooks
   block contributor flow.

## Error message format

Hooks produce errors in this format:

```
{file_path}:{line_or_-}: {hook-id}: {short message}
  └── {longer explanation if needed}
  └── Fix: {suggested action}
```

Example:

```
customer/rfps/{real-customer-name}-q3-2026.md:-: eka-codename-filenames: File path contains real customer name "Apex Retail Corp"
  └── "Apex Retail Corp" appears in CODENAMES.yml as C001 (disclosure: acknowledged-public).
  └── At L2+, file paths must not contain real entity names.
  └── Fix: Rename file to customer/rfps/c001-q3-2026.md
```

## Reference Python implementation

The `eka_*.py` files in this folder are reference implementations.
They share:

- **A common library** for parsing YAML frontmatter, loading
  `CLASSIFICATION.yml` / `CODENAMES.yml`, and deriving tier
- **A common error-reporting function** (see
  [`eka_tier_consistency.py`](eka_tier_consistency.py))
- **JSON Schema validation** via `jsonschema` library

Run a single hook:

```bash
python eka_frontmatter_required.py path/to/file.md
```

Run all hooks via pre-commit:

```bash
pre-commit run --all-files
```

## Installing hooks in a new repo

```bash
# 1. Copy the pre-commit config template
cp spec/templates/repo-skeleton/.pre-commit-config.template.yaml \
   .pre-commit-config.yaml

# 2. Install pre-commit framework
pip install pre-commit

# 3. Install the git hooks
pre-commit install

# Now every commit runs the hooks automatically.
# Run manually anytime:
pre-commit run --all-files
```

## Alternative implementations

EKA's spec is implementation-agnostic. Alternative implementations
satisfying the universal contract above are equally valid. Likely
candidates:

- **Go**: faster, single-binary distribution
- **TypeScript / Node**: integrates with mystmd toolchain
- **Rust**: fastest, can run on giant monorepos

If you ship an alternative implementation, please open a PR
against this README to register it under a "Community
implementations" section.
