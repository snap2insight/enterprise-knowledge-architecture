(chap-tooling)=
# 09 — Tooling Stack

This chapter lists the tools EKA assumes and recommends. Every
choice is **frugal-first** — free, open-source, or already-paid-for
where possible. The goal is "adopt EKA without new vendor
contracts."

Contents:

- [Required tools](#sec-required-tools)
- [Recommended tools](#sec-recommended-tools)
- [The EKA helper library](#sec-eka-helpers)
- [Source-to-artifact pipeline](#sec-artifacts)
- [What we deliberately don't recommend](#sec-non-recommended)

---

(sec-required-tools)=
## Required tools

These are non-optional. Without them, the spec is not enforceable.

| Tool | Role | Cost | Alternative if needed |
|------|------|------|----------------------|
| **Git + GitHub (or equivalent)** | Version control for L0/L1/L2 content; PR-based review | GitHub Enterprise required for `internal` visibility; otherwise free for public repos and small private repos | GitLab, Bitbucket — any with team-based ACLs and Actions equivalent |
| **An object store with per-file ACL** | L3 storage | Google Workspace (likely already paid), or paid SharePoint, or S3 with object-level ACL (technical, more setup) | Same alternatives |
| **A markdown renderer** | Generate the HTML site | MyST (free, recommended); MkDocs, Hugo, Jekyll, Docusaurus all viable | Any |
| **pre-commit framework** | Run validation hooks at commit time | Free | git hooks directly (less ergonomic) |
| **gitleaks** | Secret scanning at commit | Free | Trufflehog, Talisman |
| **An LLM-agent runtime** | Operate against EKA stores | Claude Code (subscription), or any equivalent that supports per-instance config | Any |

(sec-recommended-tools)=
## Recommended tools

These improve the experience but are substitutable.

| Tool | Role | Why this one |
|------|------|--------------|
| **MyST (`mystmd`)** | Markdown renderer + HTML site | Native cross-references, labels, mermaid in-browser, MyST directives, multi-project mounts. Open source. Used in the EKA reference implementation. |
| **Marp** | Slides from markdown | Markdown → PPTX / PDF / HTML. Slides authored as `---`-separated markdown. Open source. Sole sensible answer for "slides from the same source format as docs." |
| **Pandoc** | One-off DOCX / PDF / format conversion | Universal document converter. Use for on-demand renders, not in CI. |
| **Plane** (self-hosted) | Ticketing | Lightweight, open source, MCP integration exists. Alternative: Linear (SaaS, paid). Avoids Jira's complexity at startup scale. |
| **Google Workspace** | L3 store + email + Chat | Most likely already paid; Drive's per-file ACL is the native L3 substrate. Workspace Audit Log gives the access-trail evidence. |
| **Drive for Desktop** (Google's official sync client) | Drive ↔ local sync; the primary L3 access path | Mounts the operator's Drive as a local filesystem folder. `.md` files appear as real files (agent-readable like any local file). `.gdoc` / `.gsheet` / `.gslide` files appear as link shortcuts — for those, use the Drive MCP server or Drive API. Available on macOS and Windows. The standard sync tool for L3 markdown access. |
| **gitleaks** | Pre-commit + CI secret scanning | Industry standard. Pattern set covers AWS keys, JWTs, PEM keys, etc. |

(sec-eka-helpers)=
## The EKA helper library

EKA ships (or, when published, will ship) a small Python library
implementing the validation hooks, schema, and helper CLIs:

```
eka-helpers/
├── pyproject.toml
├── eka/
│   ├── __init__.py
│   ├── schema.py                     # Pydantic models for frontmatter, CLASSIFICATION.yml, CODENAMES.yml
│   ├── derive.py                     # tier-derivation rule
│   ├── hooks/
│   │   ├── frontmatter_required.py
│   │   ├── tier_consistency.py
│   │   ├── classification_max.py
│   │   ├── codename_filenames.py
│   │   ├── review_cadence.py
│   │   ├── data_subjects_allowed.py
│   │   ├── codename_refs_defined.py
│   │   └── related_uris_valid.py
│   ├── cli/
│   │   ├── eka_new.py                # generate a new document with template frontmatter
│   │   ├── eka_review.py             # bulk review-due report
│   │   ├── eka_audit.py              # quarterly audit report generator
│   │   ├── eka_erasure.py            # GDPR Art. 17 query + redaction helper
│   │   └── eka_validate.py           # full-repo lint
│   └── reports/
│       ├── stale_report.py
│       ├── inventory_report.py
│       └── access_review.py
└── tests/
```

CLI examples:

```bash
# Create a new document with template frontmatter
eka new --domain product --type proposal --slug new-feature
# → creates proposals/new-feature/00-summary.md with frontmatter pre-filled

# List documents due for review in the next 30 days
eka review --window 30d

# Generate the quarterly classification audit report
eka audit --quarter 2026Q2 --output audit/2026Q2.md

# Find all documents referencing a data subject
eka erasure find --subject EMP-042

# Run all hooks against a directory (for CI)
eka validate .
```

The library is implementation, not specification. EKA's *spec* is in
this document; the helper library is a reference implementation.
Other implementations (Go, TypeScript, Rust) of the same hooks
satisfy the spec equally.

(sec-artifacts)=
## Source-to-artifact pipeline

EKA prescribes one source (markdown) and on-demand rendering to
multiple artifact formats:

```
Source                       Build target                        Tool
─────────                    ────────────                        ─────

content/*.md            ─→   HTML site (per-tier)            ─→   mystmd
   ├── frontmatter
   ├── prose                                                      published to
   └── embedded diagrams                                          GitHub Pages
                                                                  on push to main

content/*.md            ─→   PDF (review-grade)              ─→   mystmd → typst
                                                                  on-demand, one-off

content/*.md            ─→   DOCX (review-grade)             ─→   mystmd → docx
                                                                  on-demand, one-off

slides/*.md             ─→   PPTX                            ─→   marp-cli
   ├── frontmatter                                                on-demand for talks
   ├── slide separators (---)
   └── slide content

slides/*.md             ─→   PDF (slides)                    ─→   marp-cli
                                                                  on-demand

content/* + diagrams    ─→   Single-PDF distribution         ─→   mystmd → typst
                                                                  manually generated,
                                                                  uploaded to Drive
                                                                  distribution/
```

### What goes in CI

Only the **HTML site build**. The CI workflow on every push to
`main`:

1. Run `eka validate .` (full lint).
2. Run `mystmd build --html`.
3. Deploy to GitHub Pages (with appropriate visibility — public for
   L0, authenticated for L1+).

CI does **not** produce PDFs, DOCX, or PPTX. Reasons:

- These formats drift from markdown over time. Auto-building them
  freezes a degraded version.
- Auto-built artifacts have no human-in-the-loop check for
  classification correctness. A misclassified PDF in
  `artifacts/` is a leak.
- The cost of a one-off `mystmd build --pdf path/to/doc.md` is
  ~30 seconds — cheap enough to do on demand.

### What gets stored in the repo as a binary

Only:

- **Diagram source files** (`.d2`, `.mmd`) and their *committed*
  rendered SVGs if MyST can't render them inline. Track the source
  in git; track the SVG as a build product (often gitignored, or
  committed as a snapshot if it's referenced from docs and rebuilds
  shouldn't be required for browsing).
- **Marp slide source** (`.md`). Generated PPTX/PDF are NOT
  committed.
- **Static images** (logos, screenshots, photos) used by docs.

Never:

- PDFs (especially board decks, RFPs, contracts) — those go to Drive
- DOCX (Word documents) — same
- PPTX (slide decks) — same
- Spreadsheets with real data (`.xlsx`) — Drive

This rule keeps the repo grep-able, diff-able, and agent-friendly.
Distribution artifacts have a different home.

(sec-non-recommended)=
## What we deliberately don't recommend

| Tool / pattern | Reason |
|----------------|--------|
| **Confluence** | Not markdown-native; LLM-hostile for round-trip; per-page ACL exists but has historically been hard to audit |
| **Notion** | Vendor lock-in; export-to-markdown is lossy; AI features keep data in Notion's tenancy |
| **SharePoint as primary docs store** | Per-file ACL works but the format (Word docs in SharePoint) is hostile to agents; only use for the specific case of Microsoft-stack-mandated environments |
| **Wiki tools (DokuWiki, MediaWiki, TWiki)** | Most don't support frontmatter-based classification; tooling ecosystem for hooks is thin |
| **PDFs as primary source** | Already covered — agent-hostile |
| **Word documents (.docx) as primary source** | Same reason |
| **Vendor "AI-powered knowledge management" SaaS** (Guru, Bloomfire, Pinecone-backed wikis, etc.) | These typically ship one-size-fits-all classification, weak per-file ACL, and vendor-locked AI integrations. EKA is the alternative: bring-your-own-LLM with your-own-classification. If the vendor solves your problem better, great — use it; but the framework still applies to the content you don't put in the vendor. |
| **Putting per-file ACL into Git via submodules or sparse-checkout** | Brittle; metadata still leaks; agents can't reason about sub-module boundaries cleanly |
| **One-mega-repo for everything** | Repo-tier ACL is then meaningless; cross-tier leak is trivial |

## A note on AI tools for authoring

EKA-using authors typically use AI tools (Claude, GPT, Copilot) to
draft and revise documents. Two safety properties:

1. **The author's AI tool reads only what the author has access to.**
   If the author is on the L2 team, their AI tool sees L2 content
   through their account. If not, it doesn't. This is the same
   property as any tool the author uses.
2. **The author's AI tool does not write to higher tiers than the
   author has access to.** A pre-commit hook in the target repo
   refuses commits that exceed the repo's max_tier, regardless of
   what the AI tool generated.

The per-tier agent topology ([chapter 7](#chap-agent-topology)) is
for *org-wide automated workflows* (digests, audits, harvests). The
per-author AI tooling is a separate concern bounded by the author's
identity.

## What's contestable

- **Python for the helper library** is the EKA reference choice
  because Python's ecosystem for YAML, JSON Schema, and pre-commit
  hooks is mature. Go or Rust implementations would be faster and
  smaller. JavaScript / TypeScript would integrate better with
  mystmd. EKA's spec is implementation-agnostic; the reference
  picks Python for accessibility.
- **MyST over MkDocs / Hugo.** MyST has the best label / cross-ref
  support and native mermaid rendering. Some orgs prefer Hugo for
  its speed and ecosystem. EKA principles work with any renderer;
  the labeling syntax may differ slightly.
- **Marp over PowerPoint / Keynote.** Marp produces less polished
  output than hand-authored slides. For board-grade decks, EKA
  recommends authoring in a presentation tool (PowerPoint /
  Keynote / Google Slides) and linking back to the markdown source
  for the substantive content. Marp is for engineering talks,
  internal presentations, etc.

[The implementation roadmap chapter](#chap-implementation-roadmap)
puts these tools into a four-week rollout plan.
