# EKA Templates

Drop-in files that an implementer (or agent) clones into a new
EKA repo, then customizes by replacing `ALL_CAPS_PLACEHOLDER`
strings.

## Three template families

| Family | Folder | Purpose |
|--------|--------|---------|
| **Repo skeleton** | [`repo-skeleton/`](repo-skeleton/README.md) | Files that go at the root and conventional locations of every EKA-conformant repo: `README.md`, `CLASSIFICATION.yml`, `_meta/manifest.md`, `_agents/`, `.pre-commit-config.yaml`, `.github/workflows/deploy.yml` |
| **Content types** | [`content-types/`](content-types/README.md) | Frontmatter pre-filled for common document types: proposal, runbook, ADR, post-mortem, weekly digest |
| **CLAUDE.md (per tier)** | [`claude-md/`](claude-md/README.md) | Tier-scoped agent guardrails: L1, L2, L3. Copy the right one into your agent home |

## How an implementer uses templates

### Bootstrap a new repo

The agent skill [`eka-bootstrap-repo`](../skills/eka-bootstrap-repo.skill.md)
copies the repo-skeleton into the new repo and fills placeholders
from the operator's inputs. Manually:

```bash
SKELETON=spec/templates/repo-skeleton
cp -r $SKELETON/. /path/to/new-repo/
cd /path/to/new-repo
# Replace ALL_CAPS placeholders (see each file)
```

### Author a new document

The skill [`eka-new-doc`](../skills/eka-new-doc.skill.md) picks
the right content-type template and pre-fills frontmatter.
Manually:

```bash
cp spec/templates/content-types/proposal.template.md \
   proposals/my-new-proposal/00-summary.md
# Edit frontmatter and body
```

### Configure an agent home

```bash
mkdir -p ~/agents/my-eng-knowledge
cp spec/templates/claude-md/L1.claude.template.md \
   ~/agents/my-eng-knowledge/CLAUDE.md
# Fill placeholders
```

## Placeholder conventions

All templates use `ALL_CAPS_WITH_UNDERSCORES` for substitution
points. Common placeholders:

| Placeholder | Meaning |
|-------------|---------|
| `ORG_NAME` | Your organization (slug form) |
| `REPO_NAME` | This repo's name |
| `TIER` | L0, L1, L2, or L3 |
| `OWNER` | Email or GitHub handle |
| `YYYY-MM-DD` | A date you should set to today (or the relevant date) |
| `DOMAIN` | One of: public, customer, people, business, product, operational |
| `VISIBILITY` | public, internal, or private |

Run `eka template-fill` (from the helper library) to interactively
substitute placeholders, or do it manually with `sed` /
search-and-replace.

## Versioning

These templates target **EKA spec v1**. When the spec increments to
v2, templates increment alongside.
