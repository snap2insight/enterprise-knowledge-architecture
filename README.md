---
title: "Enterprise Knowledge Architecture (EKA)"
substitutions:
  date: "2026-05-17"
---
# Enterprise Knowledge Architecture (EKA)

> *Enterprise knowledge architecture for the AI era — classified at
> source, verifiable by audit, shareable by tier.*

## Who this is for

- **Engineering leaders** evaluating how to structure their company's
  knowledge base before agents and customer audits force the question
- **Security & compliance teams** mapping documentation to NIST / ISO /
  GDPR controls without bolting them on retroactively
- **Knowledge architects** picking conventions that scale from 20 to
  200+ engineers
- **AI / LLM agent developers** who need their agents to read and write
  organizational content safely

## What this is

EKA is a **specification, not a tool**. It defines how to organize a
company's documented knowledge so that:

1. AI agents can read and write it safely without crossing access
   boundaries
2. Classification is declared at the source and enforced by tooling
3. Compliance evidence is built in — the same metadata that informs
   agents also satisfies auditors
4. Storage choices follow access requirements (repos for tier-bounded
   content, object stores for per-file ACL)
5. The whole approach is tool-independent (markdown + YAML + git + any
   LLM runtime)

## What this is not

- A wiki or knowledge-base product
- A document-management system
- An AI / LLM agent product
- A compliance product *(EKA produces evidence; auditors interpret it)*

## Local development

Before your first `myst build`, populate the toolkit (CSS overlay +
default footer) from its upstream repo:

```bash
# Either: clone fresh into _toolkit/
TOOLKIT_URL=https://github.com/<org>/myst-docs-toolkit.git ./bin/setup-dev.sh

# Or: symlink an existing sibling clone (preferred if you have several
# docs sites checked out alongside one toolkit clone)
TOOLKIT_LOCAL=../myst-docs-toolkit ./bin/setup-dev.sh

myst build --html            # serves at http://localhost:3000
```

`_toolkit/` is gitignored — local devs and CI both fetch it. Re-run
`setup-dev.sh` whenever you want to pull a newer toolkit version.

## Deployment

This repo's GitHub Pages workflow (`.github/workflows/eka-pages-deploy.yml`)
expects two repo variables to be set:

| Variable | Value | Notes |
|---|---|---|
| `TOOLKIT_REPO` | `<org>/myst-docs-toolkit` | Required. The toolkit repo this site's build will fetch. |
| `TOOLKIT_REF` | `main` or a tag | Optional. Defaults to `main`. Pin to a tag for reproducible builds. |
| `EKA_CONFORMANCE_TARGET` | `L0` | Required. `L0` for the canonical public deploy. The `verify-visibility` job fails the build if a non-L0 site's Pages is set to public. |

Set these under **Settings → Variables → Actions** before the first
push. The workflow validates `TOOLKIT_REPO` and emits a clear error if
it isn't set.

## Where to start

| If you're… | Start with |
|------------|-----------|
| New to EKA | [`index.md`](index.md) — the project overview with framework-at-a-glance |
| Evaluating adoption | [Primer chapters 0–1](primer/00-introduction.md) + [Roadmap](primer/10-implementation-roadmap.md) |
| Implementing | [Spec](spec/README.md) — schemas, templates, hooks, skills |
| AI agent bootstrapping | [`spec/skills/eka-agent-onboarding.skill.md`](spec/skills/eka-agent-onboarding.skill.md) |
| Looking for a worked example | [Reference implementation](reference-implementation/README.md) |

## How to contribute

This is an open specification. We welcome:

- **Feedback** — open an issue describing what's unclear or wrong
- **PRs against the spec or primer** — substantive changes, missing
  details, fixes to ambiguity
- **Alternative implementations** — reference Python hooks are the
  default; Go / TypeScript / Rust ports satisfying the same contract
  are welcome (open a PR to register them in
  [`spec/hooks/README.md`](spec/hooks/README.md))

### Contribution guidelines

- Substantive PRs should reference at least one principle (P1–P8)
  the change affects
- Every spec change updates the relevant schema if the change is
  structural
- Reviewers freeze on Friday for the following Monday's release cut
- Breaking changes to the schema increment the version (`eka.v1` →
  `eka.v2`)

## Licensing

The primer and spec are intended for release under
[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) (prose) and
the [MIT License](https://opensource.org/licenses/MIT) (schemas,
templates, hooks, skills, scripts). Exact license file to be added at
v1.0 release.

## Project status

- **Version:** `eka.v1` (draft)
- **Status:** Draft for peer / leadership review
- **Last updated:** {{ date }}

Concrete feedback — especially "this won't work because…" or "we
tried this and it failed when…" — is the most useful kind.
