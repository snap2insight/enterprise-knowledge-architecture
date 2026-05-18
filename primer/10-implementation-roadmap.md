(chap-implementation-roadmap)=
# 10 — Implementation Roadmap

A four-week rollout plan for adopting EKA in a startup or
mid-sized enterprise. Each week is a phase with explicit
deliverables and an exit gate.

Contents:

- [Assumptions](#sec-roadmap-assumptions)
- [Phase 1 (Week 1) — Foundations](#sec-phase-1)
- [Phase 2 (Week 2) — L1 internal store live](#sec-phase-2)
- [Phase 3 (Week 3) — L2 confidential store live](#sec-phase-3)
- [Phase 4 (Week 4) — L3 Drive store + agents](#sec-phase-4)
- [Beyond Week 4 — steady state](#sec-steady-state)
- [Cost expectations](#sec-cost)

---

(sec-roadmap-assumptions)=
## Assumptions

The roadmap assumes:

- An organization of 5–50 engineers (most likely).
- GitHub access (Enterprise preferred for `internal` visibility, but
  Team plan works for L1=private with all-members).
- Google Workspace or equivalent (for L3 store).
- One person with ~50% time across 4 weeks to lead the rollout (the
  "EKA owner").
- Existing knowledge content (wikis, scattered docs, etc.) that
  needs migration — but the roadmap covers framework adoption
  separately from content migration.

Companies migrating from a long-established docs system should plan
for **a separate content-migration project** following EKA adoption.
Don't try to migrate and adopt simultaneously.

(sec-phase-1)=
## Phase 1 (Week 1) — Foundations

### Goals

1. EKA spec read and accepted by leadership.
2. Helper tooling installed.
3. The L0 "Public" tier deferred (do not create yet unless concretely needed).

### Deliverables

| Item | Owner | Done when |
|------|-------|-----------|
| Read EKA spec; assemble objections | Engineering lead, security lead, compliance contact | A meeting where consensus is reached on six domains, five tiers, classification scheme |
| Install `eka-helpers` library in CI environment | Platform engineer | `eka validate --version` runs |
| Install pre-commit framework + base `.pre-commit-config.yaml` template | Platform | Template ready to drop into repos |
| Choose codename theme | EKA owner | Theme picked (e.g., Roman gods); first 10 customers and partners assigned codenames in a draft `CODENAMES.yml` |
| Document the org's domain baselines | EKA owner | A draft `domains.md` mapping the six domains to current content categories |

### Exit gate

- Leadership sign-off on the framework.
- `eka-helpers` operational.
- Codename theme + initial 10–20 entries.

(sec-phase-2)=
## Phase 2 (Week 2) — L1 internal store live

### Goals

1. The L1 repo exists, is set up with the right ACLs, and has the
   pre-commit + CI infrastructure.
2. Migrate or seed initial L1 content (manifest + 5–10 starter docs).

### Deliverables

| Item | Owner | Done when |
|------|-------|-----------|
| Create the L1 repo (`{org}-eng-docs` or similar) | EKA owner | Repo exists with `internal` (or `private` with all-employees team) visibility |
| Drop in `CLASSIFICATION.yml` with `max_tier: L1` | Platform | File committed |
| Drop in `_meta/manifest.md` (first version) | EKA owner | Manifest enumerates only this repo + external systems; will grow |
| Install `.pre-commit-config.yaml` + `.github/workflows/deploy.yml` | Platform | Pre-commit hooks run on commit; GitHub Pages site deploys on push to main |
| Write 5–10 starter docs (onboarding, glossary, conventions) | Engineering lead + people-ops contact | Each has valid frontmatter |
| Set up authenticated Pages (if Enterprise) | Platform | Site requires SSO to view |
| Document the L1 agent home setup | EKA owner | `~/agents/{l1}/` template documented in the manifest |

### Exit gate

- An engineer can navigate to the new L1 Pages site, see content,
  and recognize it as the org's L1 knowledge store.
- Pre-commit hooks reject a commit that attempts to violate L1
  classification limits (smoke test: try to commit a doc with
  `classification.C: HIGH`).
- The site is search-indexable (within the auth boundary).

(sec-phase-3)=
## Phase 3 (Week 3) — L2 confidential store live

### Goals

1. The L2 repo exists with restricted team access.
2. Initial L2 content (an existing customer RFP, a strategy doc, a
   threat model — anything one or two leaders need *first*).

### Deliverables

| Item | Owner | Done when |
|------|-------|-----------|
| Create the L2 repo (`{org}-company-docs`) — private | EKA owner | Repo exists |
| Create `{org}-company-docs-readers` team with leadership-only membership | EKA owner / org admin | Team has 3–8 members (CEO, CTO, COO, key leads) |
| Drop in `CLASSIFICATION.yml` with `max_tier: L2`, `codenames_required: true` | Platform | File committed |
| Drop in `CODENAMES.yml` (full version of the draft from Phase 1) | EKA owner | Customers / partners / competitors registered |
| Drop in `_meta/manifest.md` with cross-tier references | EKA owner | Manifest links to L1 manifest, names L3 Drive root |
| Migrate 2–5 existing confidential docs (e.g., latest RFP responses, current threat model, strategy memo) — applying codenames | EKA owner + content owners | Docs committed with valid frontmatter |
| Enable authenticated Pages on the L2 repo | Platform | L2 site visible only to team members |
| Update the L1 manifest to point at the L2 store | EKA owner | Cross-tier reference added |

### Exit gate

- A leadership-team member can browse the L2 Pages site after SSO.
- A non-team-member is denied (smoke test: ask an engineer not on
  the team to load the URL — should get 404).
- All committed L2 file paths pass the `eka-codename-filenames`
  hook (no real customer names in paths).

(sec-phase-4)=
## Phase 4 (Week 4) — L3 Drive store + agents

### Goals

1. The L3 Drive hierarchy is set up with appropriate folder ACLs.
2. Per-tier agent homes operational.

### Deliverables

| Item | Owner | Done when |
|------|-------|-----------|
| Create the L3 Drive root folder | HR + Eng manager | Folder exists with restricted access |
| Create sub-folders for 1on1s, feedback, perf, comp, hiring | HR + Eng manager | Per-folder ACLs configured (lead-only, lead+employee, CXO-only, etc.) |
| Install Drive for Desktop on team-lead laptops | Each team lead | `.md` files sync as local files |
| Install Drive MCP server for L3 agent | Platform | OAuth scoped per operator |
| Write per-tier `CLAUDE.md` for L1, L2, L3 agent homes | Platform + EKA owner | Each agent home has its CLAUDE.md, MCP config, audit log destination |
| Run negative-probe smoke tests | Platform | All 5 negative probes pass for each tier |
| Set up the audit-log retention policy | Platform / security | Logs collected, retention configured per tier |
| Run first agent harvest (weekly digest from Plane → L1) | Platform | Digest PR auto-opened |

### Exit gate

- All three per-tier agents pass smoke tests.
- One real workflow uses the agent (e.g., an engineer uses the L1
  agent to find docs; a team lead uses the L3 agent to draft a 1:1
  note).
- The first quarterly access review is scheduled.

(sec-steady-state)=
## Beyond Week 4 — steady state

After the four-week rollout, EKA enters steady state:

| Cadence | Activity |
|---------|----------|
| Per commit | Pre-commit hooks validate frontmatter, tier, codenames |
| Per PR | CI re-validates; cross-repo reference checks (nightly) |
| Weekly | Agent generates digests (tickets, chat summaries) → PRs to L1 |
| Monthly | Stale-doc report; review-due flagging; team owners triage |
| Quarterly | Access review per tier; CIS Control 3 self-assessment |
| Annually | Full classification audit; codename map review; spec re-evaluation |

### Content migration (separate project, T+4 weeks onwards)

Once the framework is operational, existing content migrates in
**waves of triage**:

- **Wave 1 (highest-leverage):** active runbooks, onboarding docs,
  recent design proposals. These are read frequently and migration
  pays off immediately.
- **Wave 2 (active customer content):** current RFPs, active threat
  models, strategy docs in flight. Codenames applied during
  migration.
- **Wave 3 (history):** post-mortems, archived RFPs, past strategy
  docs. Lower priority; migrate as touched.

Content that won't be touched in 12 months may stay where it is
(legacy wiki, old Drive folders) — migration cost exceeds value.
Add it to the manifest as "legacy store, not yet migrated, see
{location}."

(sec-cost)=
## Cost expectations

For a typical mid-sized startup adopting EKA:

| Cost item | Estimate | Notes |
|-----------|----------|-------|
| New SaaS spend | $0 | Use existing GitHub + Google Workspace |
| EKA owner time | ~50% × 4 weeks = ~10 person-days | Lead-engineer level |
| Other contributor time | ~5 person-days across phases | Reviewers, content writers, platform engineer |
| Optional: Plane self-hosted | ~$10/month VM | If you don't already have a ticket tracker |
| Optional: GitHub Enterprise upgrade | Per-seat increment | Only if you need `internal` visibility and aren't already on it |
| Total Phase 1-4 | $0-$50/month + ~15 person-days | Most of the work is documentation + configuration |

There is **no** required commercial-license cost. All required
software is open-source or already-paid-for in a typical startup
stack.

## Phase exit gates summary

| Phase | Exit gate (verified by) |
|-------|-------------------------|
| 1 | Spec approved; helper tooling installed; codename theme picked |
| 2 | L1 repo + Pages + pre-commit live; engineers can read L1 content |
| 3 | L2 repo + Pages + codenames live; non-team-members denied |
| 4 | L3 Drive + per-tier agents operational; smoke tests pass |
| Steady state | Quarterly access review + annual audit on calendar |

## What's contestable

- **The four-week timeline** assumes a focused EKA owner. If
  delegated 10% time, expect 12+ weeks. Don't promise four weeks
  unless someone has the bandwidth.
- **Content migration as a separate project** — some orgs prefer to
  migrate as part of adoption. EKA's recommendation against
  concurrent adoption-plus-migration reflects the reality that
  decisions about classification get made twice (once in adoption,
  again per legacy doc) and they tend to diverge under time
  pressure.
- **Skipping L0 in Phase 1** — companies with strong public-content
  needs may want L0 first. EKA's recommendation (defer L0) reflects
  that internal content benefits more from EKA's classification
  controls than public content does. Adjust per priorities.

The [reference implementation](../reference-implementation/README.md)
shows how a fictional Example Co applies EKA in detail. Use it as a
template for your own deployment.
