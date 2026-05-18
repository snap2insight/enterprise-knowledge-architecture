---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-bootstrap-org
      version: 1.0
      agents: [L1]                            # bootstrap is L1-scoped; it doesn't yet exist at higher tiers
      side_effects: yes
      duration_estimate: 30-60 minutes
---

# Skill: eka-bootstrap-org

## Purpose

Set up an entire EKA-conformant organization from a blank slate.
Creates the L1 + L2 Git repositories, populates them with the
spec's repo-skeleton templates, configures pre-commit hooks +
CI workflows, and produces a checklist for the manual steps
(Drive folder structure, agent-home configuration, team
membership).

## When to invoke

- A new organization is adopting EKA.
- An existing organization is restarting its docs program and
  wants a clean EKA-conformant baseline.
- A reference implementation is being created for a customer.

## Preconditions

Before invoking this skill, the operator must have:

- A GitHub organization with admin access
- `gh` CLI authenticated with admin scope
- The EKA spec checked out locally (`git clone .../enterprise-knowledge-architecture`)
- `eka-helpers` installed (`pip install eka-helpers`)
- A Google Workspace org (or chosen L3 store equivalent) — manual
  setup happens at the end
- One person designated as the "EKA owner" who'll drive this

## Inputs

Required:

| Input | Type | Example |
|-------|------|---------|
| `org_name` | string | `acme` (becomes `acme-eng-docs` etc.) |
| `org_github` | string | `acme-org` (the GitHub org slug) |
| `eka_owner_handle` | string | `jdoe@acme.com` |
| `tiers_to_create` | list | `[L1, L2]` (L3 is Drive-side, not Git) |
| `codename_theme` | string | `roman-gods` (one of: `roman-gods`, `greek-gods`, `constellations`, `gemstones`, `colors`) |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `enable_pages` | true | Enable Pages for L1/L2 (auth-gated) |
| `enterprise_plan` | autodetect | Detect via `gh api orgs/{org_github}` |
| `pages_visibility` | `private` | `private` (L1/L2) or `public` (L0 only) |

## Steps

### 1. Validate environment

```bash
# Verify gh CLI authentication and scopes
gh auth status
gh api user --jq '.login'

# Verify org admin access
gh api orgs/{org_github}/memberships/{operator} --jq '.role'  # must be "admin"

# Verify EKA spec is accessible
test -f spec/conformance.md || exit 1

# Verify eka-helpers
eka --version
```

**Validation:** all four commands must succeed. If any fails, stop
and report what's missing.

### 2. Determine org's GitHub plan (for visibility decisions)

```bash
PLAN=$(gh api orgs/{org_github} --jq '.plan.name')
```

- If `PLAN == "enterprise"`: use `internal` visibility for L1; private for L2; private Pages enabled
- If `PLAN == "team"` or `"free"`: use `private` for L1 and L2; Pages requires Pro/Team minimum

Record this decision; report to operator before proceeding.

### 3. Create the L1 repo

```bash
gh repo create {org_github}/{org_name}-eng-docs \
  --private \                           # or --internal if Enterprise
  --description "EKA L1 — Internal engineering knowledge for {org_name}" \
  --homepage "" \
  --add-readme=false

# Clone it locally
mkdir -p /tmp/eka-bootstrap && cd /tmp/eka-bootstrap
gh repo clone {org_github}/{org_name}-eng-docs
cd {org_name}-eng-docs
```

### 4. Apply the repo-skeleton template to L1

For each file in `spec/templates/repo-skeleton/`, copy into the new
repo, then substitute placeholders:

```bash
SKELETON=$(eka spec-path)/templates/repo-skeleton

# Copy structure
cp $SKELETON/CLASSIFICATION.template.yml CLASSIFICATION.yml
cp $SKELETON/.pre-commit-config.template.yaml .pre-commit-config.yaml
cp $SKELETON/README.template.md README.md
mkdir -p _meta _agents .github/workflows
cp $SKELETON/_meta/manifest.template.md _meta/manifest.md
cp $SKELETON/_agents/README.md _agents/README.md
cp $SKELETON/.github/workflows/deploy.template.yml .github/workflows/deploy.yml

# Substitute placeholders for L1
eka template-fill CLASSIFICATION.yml \
  --repo-name "{org_name}-eng-docs" \
  --visibility "$VISIBILITY" \
  --max-tier "L1" \
  --default-domain "business"

eka template-fill README.md _meta/manifest.md _agents/README.md .github/workflows/deploy.yml \
  --org-name "{org_name}" \
  --tier "L1" \
  --owner "{eka_owner_handle}"
```

**Validation:** No `ALL_CAPS_PLACEHOLDER` strings remain in any
file. Run `eka validate .` on the L1 repo; it must pass.

### 5. Copy the L1 CLAUDE.md template

```bash
mkdir -p _agents
cp $SKELETON/../claude-md/L1.claude.template.md _agents/CLAUDE.md

eka template-fill _agents/CLAUDE.md \
  --org-name "{org_name}" \
  --repo-name "{org_name}-eng-docs"
```

### 6. Commit and push L1

```bash
git add .
git commit -m "Initial EKA L1 scaffolding via eka-bootstrap-org v1.0"
git push origin main
```

### 7. Repeat for L2

If `L2` in `tiers_to_create`:

```bash
gh repo create {org_github}/{org_name}-company-docs \
  --private \
  --description "EKA L2 — Confidential business and product content for {org_name}" \
  --add-readme=false

cd ..
gh repo clone {org_github}/{org_name}-company-docs
cd {org_name}-company-docs
```

Apply the skeleton, but for L2:

```bash
eka template-fill CLASSIFICATION.yml \
  --repo-name "{org_name}-company-docs" \
  --visibility "private" \
  --max-tier "L2" \
  --default-domain "business" \
  --codenames-required true \
  --data-subjects-allowed false           # default; users can override per repo

# Enable the codename hooks in .pre-commit-config.yaml
# (uncomment the L2+ hooks block)

# Add CODENAMES.yml with the chosen theme seed (empty registry)
cp $SKELETON/CODENAMES.template.yml CODENAMES.yml

# Copy L2 CLAUDE.md
cp $SKELETON/../claude-md/L2.claude.template.md _agents/CLAUDE.md
```

Commit and push.

### 8. Create the access-control GitHub team for L2

```bash
gh api -X POST orgs/{org_github}/teams \
  -f name="{org_name}-company-docs-readers" \
  -f privacy="closed" \
  -f description="L2 readership for {org_name}-company-docs per EKA"

# Add owner to team
gh api -X PUT orgs/{org_github}/teams/{org_name}-company-docs-readers/memberships/{eka_owner_handle} \
  -f role="maintainer"

# Grant team read+write on the L2 repo
gh api -X PUT orgs/{org_github}/teams/{org_name}-company-docs-readers/repos/{org_github}/{org_name}-company-docs \
  -f permission="push"
```

### 9. Configure Pages for both repos

```bash
# L1 Pages
gh api -X POST repos/{org_github}/{org_name}-eng-docs/pages \
  -f source[branch]="gh-pages" \
  -f source[path]="/"

# Set Pages visibility (Enterprise only)
if [ "$PLAN" = "enterprise" ]; then
  gh api -X PUT repos/{org_github}/{org_name}-eng-docs/pages -f visibility="private"
  gh api -X PUT repos/{org_github}/{org_name}-company-docs/pages -f visibility="private"
fi
```

### 10. Produce the manual-steps checklist

Write to operator:

```markdown
EKA bootstrap complete for the Git portion. Manual steps remaining:

## Drive setup (L3)
- [ ] Create Workspace folder `{org_name}-drive/people-confidential/`
- [ ] Create sub-folders per EKA Drive structure (see Primer §4)
- [ ] Create Workspace ACL groups: `1on1-leads@`, `perf-calibration@`, `cxo-comp@`
- [ ] Install Drive for Desktop on team-lead laptops

## Agent homes (per operator)
- [ ] Create `~/agents/{org_name}-eng-knowledge/` (L1 agent home)
- [ ] Copy `_agents/CLAUDE.md` from L1 repo
- [ ] Configure MCP tokens scoped to L1
- [ ] Run `eka agent-smoke-test --tier L1`

- [ ] Create `~/agents/{org_name}-company-knowledge/` (L2 agent home)
- [ ] Same for L2 token and smoke test

- [ ] Create `~/agents/{org_name}-people-knowledge/` (L3 agent home)
- [ ] Configure Drive MCP with OAuth scope to relevant folders
- [ ] Run smoke test

## Team management
- [ ] Add the right people to `{org_name}-company-docs-readers`
- [ ] Set quarterly access-review calendar reminder
- [ ] Document the access-review owner in `_meta/manifest.md` of L2 repo

## Codename seeding
- [ ] Populate `CODENAMES.yml` in `{org_name}-company-docs` with
      the org's known customers, partners, competitors
- [ ] Commit on the `codenames-seed` branch and merge via PR with
      leadership review

## Validate
- [ ] Run `eka validate --conformance L1 {org_name}-eng-docs/`
- [ ] Run `eka validate --conformance L2 {org_name}-company-docs/`
- [ ] Confirm Pages sites build and deploy
- [ ] Confirm SSO gating works (try from a logged-out browser)
```

## Validations

- L1 repo passes `eka validate --conformance L1`
- L2 repo passes `eka validate --conformance L2`
- Pages deploy succeeds for both
- The L2 readership team exists and has at least one member
- Pre-commit hooks reject a deliberate violation (smoke test)

## Outputs

| Output | Location |
|--------|----------|
| L1 repo | `github.com/{org_github}/{org_name}-eng-docs` |
| L2 repo | `github.com/{org_github}/{org_name}-company-docs` |
| Team | `{org_name}-company-docs-readers` |
| Bootstrap report | `bootstrap-report-{date}.md` (the manual-steps checklist + what was automated) |

## Failure handling

| Failure | Recovery |
|---------|----------|
| `gh auth status` fails | Tell operator to run `gh auth login`; exit |
| Repo already exists | Ask operator: continue with existing repo (verify it's EKA-conformant first), recreate (DESTRUCTIVE), or pick a different name |
| Pre-commit hook installation fails | Report which hook; provide fix (usually missing Python deps); allow operator to retry |
| Pages enablement fails | Continue without Pages; add to manual-steps checklist |
| Plan detection ambiguous | Default to `private` for both repos; let operator override |

If any step fails non-recoverably, the skill writes a partial-state
file (`bootstrap-state-{date}.json`) and exits. Re-invoking with
`--resume` reads this file and continues from the last successful
step.

## What this skill does NOT do

- Migrate existing content from a legacy docs system (that's a
  separate manual project after bootstrap)
- Create Drive folders (the agent typically lacks Workspace admin
  scope; manual)
- Add humans to teams beyond the operator (manual; intentional)
- Configure agent MCP tokens (operator-specific; manual)
- Configure JIT-access tooling for L3 sub-tiers
