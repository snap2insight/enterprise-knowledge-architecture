# EKA Error Codes

Canonical error messages produced by EKA hooks and tools. Each
has a stable code so error-handling logic (in CI, in agents, in
operator tooling) can recognize and respond.

## Error format

```
{file}:{line_or_-}: {hook-id}: {short_message}  [{ERROR_CODE}]
  └── {longer_explanation}
  └── Fix: {suggested_action}
```

The `[ERROR_CODE]` is the suffix appended for machine parsing.

## Catalog

### EKA-001 — Frontmatter missing

```
{file}:1: eka-frontmatter-required: file does not start with YAML frontmatter  [EKA-001]
  └── Every .md file must have YAML frontmatter delimited by `---` lines.
  └── Fix: Add an appropriate template from spec/templates/content-types/
```

### EKA-002 — Frontmatter invalid YAML

```
{file}:{line}: eka-frontmatter-required: frontmatter is not valid YAML  [EKA-002]
  └── YAML parser failure: {parser_error}
  └── Fix: Correct the syntax error.
```

### EKA-003 — Frontmatter schema mismatch

```
{file}:-: eka-frontmatter-required: schema violation in frontmatter  [EKA-003]
  └── Field `{field}`: {validation_error}
  └── Fix: Refer to spec/schemas/frontmatter.schema.json
```

### EKA-101 — Tier inconsistent with classification

```
{file}:-: eka-tier-consistency: declared tier '{declared}' does not match derived tier '{expected}'  [EKA-101]
  └── derive_tier(classification, data_subjects) produces '{expected}' but file declares '{declared}'.
  └── Fix: Set `tier: {expected}` or change the classification/data_subjects.
```

### EKA-102 — Tier exceeds repo max

```
{file}:-: eka-classification-max: tier '{tier}' exceeds repo max_tier '{max}'  [EKA-102]
  └── This repo's CLASSIFICATION.yml limits content to '{max}'.
  └── Fix: Move file to a higher-tier repo, or downgrade classification.
```

### EKA-103 — data_subjects not allowed in this repo

```
{file}:-: eka-data-subjects-allowed: data_subjects declared but repo has data_subjects_allowed: false  [EKA-103]
  └── This repo's tier does not permit data-subject content. L3 (Drive) is appropriate.
  └── Fix: Move file to L3, or empty the data_subjects list (only if no individuals are mentioned).
```

### EKA-104 — Review cadence inconsistent

```
{file}:-: eka-review-cadence: next_review ({next}) != last_reviewed + review_cadence  [EKA-104]
  └── Expected next_review: {expected}
  └── Fix: Set next_review to {expected}, or change review_cadence/last_reviewed.
```

### EKA-201 — Real entity name in file path

```
{file}:-: eka-codename-filenames: file path contains real entity name '{name}'  [EKA-201]
  └── '{name}' appears in CODENAMES.yml as {code} ({disclosure}).
  └── L2+ repos require codenames in paths.
  └── Fix: Rename file path to use {code} instead of {name}.
```

### EKA-202 — Codename ref not defined

```
{file}:-: eka-codename-refs-defined: codename '{code}' not in CODENAMES.yml  [EKA-202]
  └── frontmatter codename_refs lists '{code}' but it's not registered.
  └── Fix: Register the codename via the codename-management runbook, or remove from codename_refs.
```

### EKA-301 — Invalid URI scheme

```
{file}:-: eka-related-uris-valid: related entry uses unknown URI scheme  [EKA-301]
  └── Entry: '{uri}'
  └── Known schemes: repo:, drive:, drive-folder:, plane:, link:, secret:
  └── Fix: Use one of the known schemes (see spec/reference/uri-schemes.md), or register an extension.
```

### EKA-401 — Manifest stale

```
_meta/manifest.md:-: eka-review-cadence: manifest is more than 60 days past next_review  [EKA-401]
  └── Manifests are agent-critical; stale manifests indicate the agent's discovery context is unreliable.
  └── Fix: Review manifest content; bump last_reviewed and next_review.
```

### EKA-500 — Repository not EKA-conformant

```
.: eka validate: CLASSIFICATION.yml not found  [EKA-500]
  └── This repo doesn't appear to be EKA-conformant.
  └── Fix: Bootstrap via `eka skill invoke eka-bootstrap-repo`, or add CLASSIFICATION.yml manually.
```

## Programmatic handling

Tools can match on the `[EKA-NNN]` suffix to react:

```python
def handle_eka_error(stderr_line: str) -> str | None:
    import re
    m = re.search(r"\[EKA-(\d{3})\]", stderr_line)
    return m.group(1) if m else None
```

Agent skills use these codes to decide retry vs. escalate vs. ask
the operator.
