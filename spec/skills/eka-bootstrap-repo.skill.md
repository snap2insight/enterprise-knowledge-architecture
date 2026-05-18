---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-bootstrap-repo
      version: 1.0
      agents: [L1, L2]
      side_effects: yes
      duration_estimate: 10-20 minutes
---

# Skill: eka-bootstrap-repo

## Purpose

Set up a single EKA-conformant repository within an existing org.
The lighter-weight sibling of `eka-bootstrap-org`.

## When to invoke

- An org already EKA-conformant needs a new repo (e.g., a new L2
  product-docs repo splitting off from a consolidated L2 store)
- An operator wants a test/sandbox repo to experiment with EKA
- A migration: an existing repo needs EKA-conformant restructuring

## Inputs

Required:

| Input | Type | Example |
|-------|------|---------|
| `org_github` | string | `acme-org` |
| `repo_name` | string | `acme-platform-docs` |
| `tier` | enum | `L1` \| `L2` |
| `default_domain` | enum | `operational` |
| `owner_handle` | string | `jdoe@acme.com` |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `visibility` | derived from tier + org plan | Override the default |
| `codenames_required` | derived from tier (true at L2+) | |
| `data_subjects_allowed` | `false` | |
| `enable_pages` | `true` | |
| `team_with_access` | `eng` (L1) / `{org}-company-docs-readers` (L2) | Existing team to grant access |

## Steps

1. Validate `gh` admin on `org_github`.
2. Verify the org has a parent EKA-conformant L1 repo (so the new
   repo can link into the org's manifest). If not, suggest
   `eka-bootstrap-org` instead.
3. Create the repo with appropriate visibility.
4. Clone locally, apply the skeleton, fill placeholders.
5. Commit and push.
6. Grant team access; configure Pages.
7. Update the org's L1 manifest to reference the new repo
   (creates a PR against the L1 repo).
8. Run `eka validate --conformance {tier}`.
9. Produce a brief report.

## Outputs

| Output | Location |
|--------|----------|
| New repo | `github.com/{org_github}/{repo_name}` |
| PR against L1 repo updating manifest | URL in report |
| Bootstrap report | `bootstrap-repo-report-{date}.md` |

## Failure handling

Same as `eka-bootstrap-org` for repo-creation steps. Additionally:

| Failure | Recovery |
|---------|----------|
| Manifest update PR fails | Provide manual instructions to update L1 manifest |
| Team grant fails | Add to checklist; operator does manually |

## What this skill does NOT do

- Cross-org operations
- Create teams (use `gh api` directly or `eka-bootstrap-org`)
- Migrate existing content into the new repo
