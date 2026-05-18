# EKA CI / Build Workflows

Ready-to-drop CI workflows and configuration files.

## What's here

| File | Purpose |
|------|---------|
| [`pre-commit-config.yaml`](pre-commit-config.yaml) | Same as `spec/templates/repo-skeleton/.pre-commit-config.template.yaml`; pinned reference version |
| [`github-actions/eka-validate.yml`](github-actions/eka-validate.yml) | Re-run pre-commit hooks + conformance check on every PR |
| [`github-actions/eka-pages-deploy.yml`](github-actions/eka-pages-deploy.yml) | MyST build + deploy to GitHub Pages (auth-gated for L1/L2) |
| [`github-actions/eka-weekly-digest.yml`](github-actions/eka-weekly-digest.yml) | Weekly cron: invoke `eka-weekly-digest` agent; open PR with the report |

## Installation

```bash
# From your EKA repo root:
EKA_SPEC=path/to/enterprise-knowledge-architecture

cp $EKA_SPEC/spec/ci/pre-commit-config.yaml .pre-commit-config.yaml
mkdir -p .github/workflows
cp $EKA_SPEC/spec/ci/github-actions/*.yml .github/workflows/

pre-commit install
git add .pre-commit-config.yaml .github/workflows/
git commit -m "Install EKA CI workflows"
```

## Tuning per tier

L1 vs. L2 differences in CI:

- **L1** uses `eka validate --conformance L1`
- **L2** uses `eka validate --conformance L2`
- **L2** Pages workflow includes a step to verify
  `pages.visibility == private`

Set the conformance target via repo variable:

```bash
gh variable set EKA_CONFORMANCE_TARGET --body "L1"
```
