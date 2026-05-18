# REPO_TITLE

> ONE_LINE_DESCRIPTION

**Tier:** TIER (e.g., L1 Internal)
**Visibility:** VISIBILITY
**EKA conformance:** Targeting EKA TIER conformant per
[EKA spec](https://github.com/ORG/enterprise-knowledge-architecture)
**Last updated:** YYYY-MM-DD

## What this repo is

REPO_PURPOSE_PARAGRAPH

Examples of content that belongs here:
- EXAMPLE_1
- EXAMPLE_2
- EXAMPLE_3

## What does NOT belong here

- LIST_OF_OUT_OF_TIER_CONTENT_TYPES — link to where they live instead

## Navigation

- [`_meta/manifest.md`](_meta/manifest.md) — **read this first** if
  you're new to this repo or you're an AI agent operating against it.
  It enumerates every content area and cross-references other tier
  stores.
- See [the EKA primer](LINK_TO_PRIMER) if you're new to the
  framework.

## Working with this repo

### Authoring conventions

- Every markdown file requires EKA frontmatter; see
  [`spec/schemas/frontmatter.schema.json`](LINK_TO_SCHEMA) or use
  templates in [`spec/templates/content-types/`](LINK_TO_TEMPLATES).
- File names follow [EKA naming conventions](LINK):
  lowercase-kebab; date prefix for time-series; **codenames at L2+**.
- Pre-commit hooks are mandatory. Install: `pre-commit install`.

### Review and contribution

- All changes via PR; reviewers per `CODEOWNERS` where applicable.
- Documents marked `status: review-due` should be triaged within
  30 days. Renewal PRs require a `review_notes:` block.

### Agent operations

- Agents operating against this repo MUST follow the boot routine
  in [`_agents/CLAUDE.md`](_agents/CLAUDE.md).
- The repo's `max_tier` is **TIER**. Content above this tier is
  rejected by the pre-commit hooks; agents must not attempt to
  introduce it.

## Owners

| Role | Owner |
|------|-------|
| Repo administrator | OWNER_HANDLE |
| Content area: ONBOARDING | OWNER_HANDLE |
| Content area: ARCHITECTURE | OWNER_HANDLE |
| Security & compliance | OWNER_HANDLE |

## Build & deploy

- HTML site is built and deployed by GitHub Actions on push to `main`
  (see `.github/workflows/deploy.yml`).
- Pages visibility: PAGES_VISIBILITY (typically: matches repo
  visibility).
- Build locally: `myst start` (requires `mystmd` installed).

## License

LICENSE_NOTE (e.g., "All rights reserved; internal use only.")
