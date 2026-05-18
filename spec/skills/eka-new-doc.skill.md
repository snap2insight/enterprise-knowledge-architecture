---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-new-doc
      version: 1.0
      agents: [L1, L2, L3]
      side_effects: yes
      duration_estimate: 1-3 minutes
---

# Skill: eka-new-doc

## Purpose

Create a new EKA-conformant markdown document with the right
content-type template + correctly-filled frontmatter, in the right
location.

## When to invoke

- Operator says "create a new proposal/runbook/ADR/post-mortem"
- Operator pastes a draft into chat and asks to "save this"
- Bootstrap workflows that need to seed initial content

## Inputs

Required:

| Input | Type | Example |
|-------|------|---------|
| `content_type` | enum | `proposal` \| `runbook` \| `adr` \| `post-mortem` \| `digest` \| `freeform` |
| `title` | string | "MFA + JWT upgrade" |
| `target_repo` | string | `acme-eng-docs` (defaults to operator's current repo) |
| `slug` | string | `mfa-jwt-upgrade` (auto-derived from title if omitted) |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `tier` | derived from content_type + target_repo's max_tier | |
| `domain` | derived from content_type | |
| `owner` | operator | Override if writing on someone else's behalf |
| `body` | empty stub | Optional initial body text from operator |
| `parent_folder` | derived from content_type | `proposals/`, `runbooks/`, etc. |

## Steps

### 1. Resolve target location

```bash
cd {target_repo}
test -f CLASSIFICATION.yml || { echo "Not an EKA repo"; exit 1; }
```

Read `CLASSIFICATION.yml`:
- Max tier
- Default classification
- Whether codenames required
- Whether data subjects allowed

Verify the proposed `content_type` + `tier` is compatible with the
repo's max_tier. If not, suggest a different repo.

### 2. Choose the template

| content_type | Template | Default folder |
|--------------|----------|----------------|
| `proposal` | `spec/templates/content-types/proposal.template.md` | `proposals/{slug}/00-summary.md` |
| `runbook` | `spec/templates/content-types/runbook.template.md` | `runbooks/{slug}.md` |
| `adr` | `spec/templates/content-types/adr.template.md` | `architecture/decisions/adr-{nnnn}-{slug}.md` |
| `post-mortem` | `spec/templates/content-types/post-mortem.template.md` | `post-mortems/pm-{yyyy-mm-dd}-{slug}.md` |
| `digest` | `spec/templates/content-types/digest.template.md` | `digests/weekly/{yyyy-Www}.md` |
| `freeform` | none — author-provided body | `_inbox/{yyyy-mm-dd}-{slug}.md` |

For `adr`, look at existing `architecture/decisions/` to find the
next number.

### 3. Fill frontmatter

Start from the template's frontmatter. Substitute:

- `title`: operator's input
- `owner`: operator's handle
- `last_reviewed`: today
- `next_review`: today + cadence
- `review_cadence`: per template default + per-repo override
- `domain`, `classification`, `tier`: derived per content_type and
  repo

For L2 documents creating customer- or business-specific content:
- Ask operator which codenames apply; populate `codename_refs`
- If the title contains a real entity name, rename to use codename

For L3 documents:
- Confirm `data_subjects` codes (EMP-NNN); operator provides

### 4. Apply body

If operator provided body text: paste it after the frontmatter.
If not: paste the template's stub body (with `OPERATOR_FILL` markers
where operator content goes).

### 5. Validate

Run the EKA hooks against the new file:

```bash
eka validate {file_path}
```

If validation fails, fix what the agent can autonomously (e.g.,
recompute `next_review`); for things requiring operator input
(missing domain, ambiguous classification), ASK.

### 6. Commit or stage

Default: write the file and stage (`git add`) but DO NOT commit.
Tell operator: "File created and staged. Review and commit when
ready: `git commit -m 'Add {slug} {content_type}'`."

If operator says "commit": agent commits with a sensible message
and pushes.

## Validations

- File path follows naming conventions for the tier
- Frontmatter is schema-valid
- All required fields are populated
- `eka validate {file}` returns zero

## Outputs

| Output | Location |
|--------|----------|
| New markdown file | The target path |
| Brief summary | "Created `path/to/file.md` (L1, proposal). Staged for commit." |

## Failure handling

| Failure | Recovery |
|---------|----------|
| Target repo isn't EKA-conformant | Tell operator; offer to bootstrap |
| Tier mismatch | Suggest different repo or downgrade content_type |
| File already exists | Ask: overwrite (DESTRUCTIVE), append timestamp, or stop |
| Required input ambiguous | Ask operator |
