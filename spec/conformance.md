# EKA Conformance

This document defines the **testable bar** for claiming EKA
conformance. Every requirement here can be verified by a script or
a checklist.

## Conformance levels

| Level | Required for | What you have |
|-------|--------------|---------------|
| **L1 — Structural** | Minimum claim | L1 repo + schemas + hooks + validation passing |
| **L2 — Operational** | "We use EKA" claim | L1 + L2 repo + codenames + per-tier agents |
| **L3 — Fully tiered** | Compliance-evidence claim | L2 + L3 store + audit logs + erasure workflow |

Claim only what you've actually implemented. Per-level requirements
follow.

---

## L1 — Structural conformance

To claim L1 conformance, an organization MUST have ALL of the
following.

### L1-R1: Repo declares classification

The organization has at least one repository with a
`CLASSIFICATION.yml` at its root that conforms to
[`schemas/classification-yml.schema.json`](schemas/classification-yml.schema.json).

**Verify:**
```bash
test -f CLASSIFICATION.yml && \
python -c "import json, yaml, jsonschema; \
  jsonschema.validate(yaml.safe_load(open('CLASSIFICATION.yml')), \
  json.load(open('spec/schemas/classification-yml.schema.json')))" && \
  echo "L1-R1: PASS"
```

### L1-R2: Every markdown file has valid frontmatter

Every `.md` file in the repo (except those in build-output or
explicitly-excluded directories listed in `CLASSIFICATION.yml`)
has YAML frontmatter conforming to
[`schemas/frontmatter.schema.json`](schemas/frontmatter.schema.json).

**Verify:** Run `eka validate .` (from
[hooks/](hooks/)); it must exit zero.

### L1-R3: Tier derivation is consistent

For every document, `tier = derive_tier(classification, data_subjects)`
per the rule in [`hooks/eka_tier_consistency.py`](hooks/eka_tier_consistency.py).

**Verify:** The `eka-tier-consistency` hook passes on all files.

### L1-R4: Classification does not exceed repo max

For every document, `tier ≤ CLASSIFICATION.yml::repo.max_tier`.

**Verify:** The `eka-classification-max` hook passes on all files.

### L1-R5: Pre-commit hooks are installed and enforced

The repository's `.pre-commit-config.yaml` includes the seven core
EKA hooks. The hooks run on `pre-commit run --all-files` without
errors. The repository's CI configuration runs the same hooks on
every PR.

**Verify:**
```bash
test -f .pre-commit-config.yaml && \
grep -q "eka-" .pre-commit-config.yaml && \
pre-commit run --all-files && \
echo "L1-R5: PASS"
```

### L1-R6: Manifest exists and is current

`_meta/manifest.md` exists, has valid frontmatter, and its
`last_reviewed` is within the cadence declared in its own
frontmatter.

**Verify:** Manual inspection of `_meta/manifest.md`; cadence
adherence checked by `eka-review-cadence` hook.

### L1-R7: Ownership is declared

Every document declares an `owner` in its frontmatter. The owner
either exists in `_meta/ownership.yml` (preferred) or is a
recognizable identifier (email, GitHub handle).

**Verify:** `eka-frontmatter-required` hook validates `owner` is
non-empty.

### L1-R8: Authentication required for repo access

The L1 repository is `internal` visibility (Enterprise) or
`private` with org-wide team access. Anonymous internet readers
cannot access content.

**Verify:** Attempt to read repo URL from an unauthenticated browser.
Must redirect to login or 404.

### L1 conformance summary

A repo passing L1-R1 through L1-R8 may be declared **EKA L1
conformant**. The conformance is verified by running:

```bash
eka validate --conformance L1 .
```

(Reference implementation; alternative implementations producing
equivalent verification also satisfy the requirement.)

---

## L2 — Operational conformance

To claim L2 conformance, an organization MUST have L1 conformance
plus:

### L2-R1: L2 repo exists with codenames

A separate `{org}-company-docs` (or equivalent) repo exists with
its own `CLASSIFICATION.yml` declaring `max_tier: L2` and
`codenames_required: true`. The repo contains a `CODENAMES.yml`
conforming to
[`schemas/codenames-yml.schema.json`](schemas/codenames-yml.schema.json).

### L2-R2: No real entity names in L2 file paths

For every file in the L2 repo, the file path does NOT contain any
string from the `name` field of any entry in `CODENAMES.yml`
(case-insensitive). Only codenames (e.g., `c001`, `p001`) appear
in paths.

**Verify:** The `eka-codename-filenames` hook passes.

### L2-R3: Codename references are defined

Every codename in any document's `codename_refs` frontmatter field
exists in `CODENAMES.yml`.

**Verify:** The `eka-codename-refs-defined` hook passes.

### L2-R4: Per-tier agent homes exist

The organization has at least one configured agent home for each
tier in use, with a tier-appropriate `CLAUDE.md` template
(matching the structure in
[`templates/claude-md/`](templates/claude-md/)).

**Verify:** Manual inspection. A future automated check
(`eka-agent-homes-validate`) is planned.

### L2-R5: Tier-isolation smoke tests pass

Each per-tier agent passes the negative-probe smoke test in its
tier (see [Primer §7](../primer/07-agent-topology.md#sec-negative-probes)).

**Verify:** Run the agent-test suite; results recorded in
`_meta/agent-onboarding-record.md`.

### L2-R6: Access control is RBAC

L2 repo read access is gated by team membership (e.g., a GitHub
team like `{org}-company-docs-readers`). The team is reviewed at
least quarterly; the most recent review is documented.

**Verify:** Manual: locate the most recent access-review record;
confirm it's within 90 days.

### L2-R7: Cross-tier references use URI scheme

Cross-tier references in `related:` frontmatter use the URI scheme
defined in [`reference/uri-schemes.md`](reference/uri-schemes.md)
(`repo:`, `drive:`, `plane:`, `link:`, `secret:`). No raw
filesystem paths or unprefixed URLs.

**Verify:** The `eka-related-uris-valid` hook passes.

---

## L3 — Fully tiered conformance

To claim L3 conformance, an organization MUST have L2 conformance
plus:

### L3-R1: L3 object store with per-file ACL

A configured object store (Google Drive, SharePoint, S3 with
object ACLs, or equivalent) holds the org's L3 content. The store
supports per-file or per-folder ACL natively. The store's root and
sub-structure match the layout in [Primer §4](../primer/04-storage-and-naming.md).

### L3-R2: Data-subject tracking is consistent

Every L3 document containing references to identifiable individuals
declares `data_subjects:` in its frontmatter using the `EMP-NNN`
or `CAND-NNN` code form. The codes resolve via the org's HRIS;
EKA itself does not store name-to-code mapping for L3 individuals.

**Verify:** Sample 20 random L3 documents. Each must declare
`data_subjects` if any individual is mentioned.

### L3-R3: GDPR Article 17 erasure workflow exists

The org has documented and tested an erasure workflow per
[`operations/erasure.runbook.md`](operations/erasure.runbook.md).
Test: produce an erasure report for a sample subject within 60
minutes.

**Verify:** Documented test record in
`_meta/erasure-test-record.md` from within the last 12 months.

### L3-R4: Audit logs are retained per tier

Audit logs are collected for every agent action and meet retention
requirements:

| Tier | Retention |
|------|-----------|
| L1 audit logs | ≥12 months |
| L2 audit logs | ≥24 months |
| L3 audit logs | ≥36 months |

**Verify:** Inspect log-retention configuration; spot-check log
contents for completeness.

### L3-R5: JIT access for sensitive sub-tiers

Sensitive L3 sub-tiers (e.g., performance-review-in-calibration,
compensation-data, candidate-evaluation-mid-loop) use just-in-time
access elevation rather than persistent ACL membership.

**Verify:** Documented JIT process for at least one sub-tier;
evidence of recent JIT events in audit log.

### L3-R6: Annual classification audit run

The organization has executed at least one annual classification
audit per
[`operations/annual-audit.runbook.md`](operations/annual-audit.runbook.md)
in the past 14 months, and the audit report is filed in the L2 repo.

---

## Non-conformance examples

A deployment **does NOT** conform to L1 if:

- Frontmatter is missing from any markdown file in the repo (excluding declared exclusions)
- Pre-commit hooks are not installed
- The L1 repo is publicly visible without auth
- Classification fields use non-FIPS-199 values
- `tier` field is missing or inconsistent with classification

A deployment **does NOT** conform to L2 if:

- Real customer names appear in L2 file paths
- CODENAMES.yml is missing
- L2 repo is readable by all employees (rather than by a defined team)
- Cross-tier references use ad-hoc syntax instead of URI scheme

A deployment **does NOT** conform to L3 if:

- L3 content lives in a Git repo (no per-file ACL)
- `data_subjects` is omitted on documents mentioning individuals
- Audit logs are not retained
- No documented erasure workflow exists

## Auditing conformance

The EKA reference implementation provides:

```bash
eka validate --conformance L2 .
```

This runs all applicable hooks plus the manual-inspection checklist
in a CI-friendly format. Output is a per-requirement pass/fail
report suitable for evidence packages.

For human review, [`operations/annual-audit.runbook.md`](operations/annual-audit.runbook.md)
walks through the conformance check end-to-end.

## Public claim language

When an organization publicly claims EKA conformance, it should
use the form:

> "Documentation classification follows the Enterprise Knowledge
> Architecture (EKA) framework. Our deployment is **EKA L2
> conformant** as of `{date}`, verified against `{spec version}`."

The version reference makes the claim falsifiable. Claims without
a version are not meaningful — EKA evolves, and conformance to v1
is not conformance to v2.
