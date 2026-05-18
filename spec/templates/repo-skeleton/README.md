# Repo skeleton

Files that go into the root and conventional locations of every
EKA-conformant repository. Copy this entire folder into a new
repo, then fill ALL_CAPS placeholders.

## What's here

| File | Purpose | See also |
|------|---------|----------|
| [`README.template.md`](README.template.md) | The new repo's own README | — |
| [`CLASSIFICATION.template.yml`](CLASSIFICATION.template.yml) | Repo metadata: tier, defaults, hook list | [classification-yml.schema.json](../../schemas/classification-yml.schema.json) |
| [`CODENAMES.template.yml`](CODENAMES.template.yml) | L2+ codename registry (omit at L1) | [codenames-yml.schema.json](../../schemas/codenames-yml.schema.json) |
| [`_meta/manifest.template.md`](_meta/manifest.template.md) | The agent boot file + human discovery index | [agent topology primer](../../../primer/07-agent-topology.md) |
| [`_agents/README.md`](_agents/README.md) | Instructions for agent setup | — |
| [`.pre-commit-config.template.yaml`](.pre-commit-config.template.yaml) | Pre-commit hooks to install | [hooks/](../../hooks/) |
| [`.github/workflows/deploy.template.yml`](.github/workflows/deploy.template.yml) | GitHub Actions: build & deploy Pages | [ci/](../../ci/) |

## How an agent uses this skeleton

The [`eka-bootstrap-repo`](../../skills/eka-bootstrap-repo.skill.md)
skill copies every file here, then runs `eka template-fill` to
substitute placeholders. Manual equivalent:

```bash
SKEL=spec/templates/repo-skeleton
TARGET=/path/to/new-repo

# Copy structure
cp $SKEL/README.template.md       $TARGET/README.md
cp $SKEL/CLASSIFICATION.template.yml $TARGET/CLASSIFICATION.yml
cp $SKEL/CODENAMES.template.yml   $TARGET/CODENAMES.yml      # L2+ only
mkdir -p $TARGET/_meta $TARGET/_agents $TARGET/.github/workflows
cp $SKEL/_meta/manifest.template.md $TARGET/_meta/manifest.md
cp $SKEL/_agents/README.md $TARGET/_agents/README.md
cp $SKEL/.pre-commit-config.template.yaml $TARGET/.pre-commit-config.yaml
cp $SKEL/.github/workflows/deploy.template.yml \
   $TARGET/.github/workflows/deploy.yml

# Then sed-replace all ALL_CAPS placeholders, or use eka template-fill.
```

## Placeholders by file

| File | Common placeholders |
|------|---------------------|
| `README.template.md` | `REPO_TITLE`, `ONE_LINE_DESCRIPTION`, `TIER`, `VISIBILITY`, `REPO_PURPOSE_PARAGRAPH`, `OWNER_HANDLE` |
| `CLASSIFICATION.template.yml` | `REPO_NAME`, `VISIBILITY`, `TIER`, `DOMAIN` |
| `_meta/manifest.template.md` | `REPO_NAME`, `ORGANIZATION`, `TIER`, `DOMAIN`, `OWNER_HANDLE`, `PAGES_URL` |

See each template's comments for the full list.
