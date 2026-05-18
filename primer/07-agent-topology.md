(chap-agent-topology)=
# 07 — Agent Topology

This chapter operationalizes [P6](#chap-principles): how AI agents
interact with an EKA knowledge base safely, with tier-scoped access
and verifiable audit.

Contents:

- [The per-tier agent model](#sec-per-tier-agents)
- [Agent boot routine](#sec-boot-routine)
- [MCP scoping](#sec-mcp-scoping)
- [Working-directory boundaries](#sec-working-dirs)
- [CLAUDE.md skeletons](#sec-claude-md)
- [Negative-probe smoke tests](#sec-negative-probes)
- [Audit logging](#sec-audit)
- [What this prevents and what it doesn't](#sec-threat-coverage)

---

(sec-per-tier-agents)=
## The per-tier agent model

EKA does not deploy a single agent with access to everything. Each
access tier has its own agent runtime with its own:

- Working directory (the agent home)
- `CLAUDE.md` (or equivalent system prompt) declaring tier scope
- MCP servers configured for that tier only
- Audit-log destination

```mermaid
flowchart TB
    subgraph Tier_L1[L1 Internal — eng-knowledge agent]
        Home1[~/agents/eng-knowledge/<br/>CLAUDE.md, manifest pointers]
        MCP1[MCPs:<br/>• Plane read-only<br/>• Chat read-only<br/>• org-eng-docs repo access]
        Logs1[Audit log:<br/>eng-agent-audit-2026.jsonl]
    end

    subgraph Tier_L2[L2 Confidential — company-knowledge agent]
        Home2[~/agents/company-knowledge/<br/>CLAUDE.md, expanded manifest]
        MCP2[MCPs:<br/>• L1 reads ABOVE PLUS<br/>• org-company-docs repo<br/>• Read-only L3 metadata]
        Logs2[Audit log:<br/>company-agent-audit-2026.jsonl<br/>retained 24 months]
    end

    subgraph Tier_L3[L3 Restricted — people-knowledge agent]
        Home3[~/agents/people-knowledge/<br/>CLAUDE.md, Drive-scoped]
        MCP3[MCPs:<br/>• Google Drive MCP<br/>  scoped to operator's<br/>  Drive folders]
        Logs3[Audit log:<br/>people-agent-audit-2026.jsonl<br/>retained 36 months]
    end

    Tier_L1 -.cannot read.-> Tier_L2
    Tier_L2 -.cannot read.-> Tier_L3
    Tier_L3 -.cannot read.-> Tier_L1
```

The agents are different *instances of the same runtime* (e.g.,
Claude Code). What makes them different is the working directory and
MCP configuration. A user might run all three on the same laptop,
in separate terminal sessions, each with its own `cwd` and
`.claude/` directory.

### Why separate runtimes per tier

The natural temptation is a "super-agent" with conditional access
("if reading L3, require MFA"). Two reasons EKA rejects this:

1. **Composability of context.** A super-agent that reads L2 + L3
   in the same session will produce output that mixes both, even
   if the human asks only L1-tier questions. Tier-scoping at the
   *runtime* level prevents this mix from being possible.
2. **Trust in the agent runtime.** LLMs are not yet reliably
   instruction-following for "don't reveal X." Removing the
   capability is safer than restricting the behavior. Tier-scoped
   MCPs make the capability genuinely absent.

(sec-boot-routine)=
## Agent boot routine

Every agent operating against EKA stores follows this routine on
every conversation:

```
1. Read CLAUDE.md (tier scope, conventions, guardrails)
2. Read _meta/manifest.md (what's where, cross-tier references)
3. Read CLASSIFICATION.yml (repo limits, max_tier)
4. (If applicable) Read CODENAMES.yml (entity codes)
5. For every file read:
   - Verify file's tier ≤ agent's max_tier
   - Log read with timestamp + path + frontmatter snapshot
6. For every file written:
   - Validate generated frontmatter
   - Verify written tier ≤ repo's max_tier
   - Log write with diff
7. For every cross-tier reference encountered:
   - If pointing higher: report as out-of-scope, don't follow
   - If pointing lower: may follow if relevant
```

Steps 1–4 are typically ~30 seconds of context. Steps 5–7 happen
continuously during the session. The boot-routine is enforced by
the `CLAUDE.md` template (each tier's CLAUDE.md says "before
anything else, do these steps").

(sec-mcp-scoping)=
## MCP scoping

The Model Context Protocol servers connect agents to external
systems. EKA's MCP scoping rules:

| Agent tier | Allowed MCP scopes |
|------------|--------------------|
| L1 (eng-knowledge) | Read/write `org-eng-docs`; read-only Plane (all projects, no edits); read-only Chat (with operator consent); no Drive access |
| L2 (company-knowledge) | All of L1 plus: read/write `org-company-docs`; read-only L3 metadata (filenames only, not content) |
| L3 (people-knowledge) | Google Drive MCP scoped to operator's accessible folders only; no L1/L2 repo access (to prevent inadvertent cross-tier mixing) |

### Filename-only L3 metadata access from L2

An L2 agent can know that **a doc exists at L3** (so it can include
a pointer in its output) but cannot read the doc's content. The
filename-only access is implemented via a thin MCP shim that exposes
`list_files` but not `read_file` for the L3 store.

This enables L2 agents to write things like:

> "The MFA threat model has a sensitive companion document at L3
> Drive: customer-confidential/c001/security-review.md. Access via
> the account team."

Without the filename-only access, the L2 agent would have to *guess*
that such a doc exists, leading to either invented references or
omissions. The thin shim is the right trade-off.

### MCP auth realms

For per-tier scoping to work, MCP servers must enforce **separate
authentication realms**:

- L1 MCPs authenticate with a token that only grants L1 access
- L2 MCPs use a different token granting L2
- L3 MCPs (Drive) use OAuth scoped to the operator's specific Drive
  folders

Sharing a single token across tiers defeats the model.
Implementation-wise: each tier's `.claude/` directory has its own
secrets file (gitignored, of course); the secrets contain
tier-appropriate tokens.

(sec-working-dirs)=
## Working-directory boundaries

The simplest enforcement layer is the agent's working directory.
Claude Code (and similar runtimes) respect `cwd` as a hard boundary
for file operations — the agent cannot accidentally `cat`
`/etc/passwd` or read files outside `cwd`.

EKA structures agent homes accordingly:

```
~/agents/
├── eng-knowledge/
│   ├── CLAUDE.md               # tier-L1 guardrails
│   ├── .claude/
│   │   ├── settings.json       # MCP config, L1 token
│   │   └── secrets.json        # gitignored; L1 token
│   ├── manifest-pointer.md     # symlinks to org-eng-docs/_meta/manifest.md
│   └── work/                   # scratch space; agent's cwd
├── company-knowledge/
│   ├── CLAUDE.md               # tier-L2 guardrails
│   ├── .claude/
│   │   └── settings.json       # L2 token, expanded MCPs
│   ├── manifest-pointer.md
│   └── work/
└── people-knowledge/
    ├── CLAUDE.md               # tier-L3 guardrails
    ├── .claude/
    │   └── settings.json       # Drive OAuth
    └── work/
```

An operator running an L1 query opens a terminal at
`~/agents/eng-knowledge/work/`, launches Claude Code, and the agent
reads `CLAUDE.md` (tier scope) plus the L1 manifest pointer. Any
attempt to access content above L1 either fails (MCP returns
not-found) or is refused by the agent per its CLAUDE.md.

To answer an L2 question, the operator opens a new terminal at
`~/agents/company-knowledge/work/` — a separate session, separate
context, separate agent identity.

(sec-claude-md)=
## CLAUDE.md skeletons

A reference CLAUDE.md for each tier. These live in the agent home,
not in the EKA repos (they're agent-runtime configuration, not
documentation).

### L1 eng-knowledge CLAUDE.md

```markdown
# Eng-knowledge agent — Tier L1

## Your tier
- You operate at L1 (Internal). You may read and write content in
  org-eng-docs and equivalent L1 stores only.
- You may read but not write Plane tickets via MCP.
- You may summarize Chat conversations on demand (with operator
  consent).

## Hard rules
1. You must NOT attempt to read content classified L2 or higher.
2. You must NOT write content with classification.C: HIGH.
3. You must NOT write content with non-empty data_subjects.
4. Every write must include valid frontmatter per EKA spec v1.

## Boot routine (every session)
1. Read manifest-pointer.md.
2. Read CLASSIFICATION.yml of any repo you write to.
3. Verify your MCP scopes match this tier.

## When you see a cross-tier reference
- Pointing to L2/L3: report it as out-of-scope. Tell the operator
  what they'd need to do to access it.
- Pointing to L0: follow if relevant.

## Writing conventions
- Use the eka-frontmatter-template skill to generate frontmatter.
- Default classification: { C: MODERATE, I: MODERATE, A: LOW }.
- Default domain: business unless context implies otherwise.
- Cite sources using [](#label) semantic refs, not URLs.

## On uncertainty
- If you cannot determine classification for a draft, ASK the
  operator. Do not guess upward (overclassify) or downward
  (underclassify).
- If your reasoning involves L2/L3 content, STOP and report.
```

### L2 company-knowledge CLAUDE.md

```markdown
# Company-knowledge agent — Tier L2

## Your tier
- You operate at L2 (Confidential). You may read content at L1 and
  L2; you may write content at L2 only (or L1 if explicitly
  requested with confirmation).
- You may list (but not read) L3 file metadata via the filename-only
  shim.

## Hard rules
1. You must NEVER read L3 file content.
2. You must use codenames for all entities in any file path,
   filename, or first body-text occurrence. Refer to CODENAMES.yml.
3. You must include data_subjects: in frontmatter whenever an
   identifiable individual is mentioned in the body.
4. You must redact any sensitive content when writing summaries that
   will be shared at L1.

## Boot routine
1. Read manifest-pointer.md (extended L2 manifest).
2. Read CODENAMES.yml of org-company-docs.
3. Read CLASSIFICATION.yml.
4. Confirm MCP scopes.

## When asked to share content cross-tier
- Down to L1: explicit summarization required. Identify what must
  be removed. Ask the operator to confirm before writing.
- Up to L0: refuse. L0 publication is a deliberate process, not an
  agent operation.

## Audit
- Every read of L2 content logged with intent (operator's
  question that triggered the read).
- Every write logged with diff.
```

### L3 people-knowledge CLAUDE.md

```markdown
# People-knowledge agent — Tier L3

## Your tier
- You operate at L3 (Restricted). You read and write content in the
  operator's Drive folders only.
- You have no access to L1 or L2 stores from this agent home.

## Hard rules
1. Every output must respect the per-file ACL of the source. If
   you read a doc owned by lead-A and lead-B, your output must NOT
   reveal lead-B's content to lead-A.
2. When summarizing across multiple individuals, name only those
   the operator has explicit access to. If unsure, ASK.
3. Never write frontmatter that creates data_subjects entries for
   individuals other than those mentioned in your source.

## Boot routine
1. Verify Drive MCP scope matches the operator's Drive ACLs.
2. Confirm operator identity (this should match a known team-lead
   or HR-role identity).

## Conventions
- Employee codes (EMP-NNN) only in writing; the agent does not
  resolve codes to names without operator confirmation.
- Outputs are written to the same Drive folder structure as sources;
  do not bring content into the local working directory beyond the
  immediate session.
```

(sec-negative-probes)=
## Negative-probe smoke tests

Every agent passes a tier-isolation smoke-test suite before it's
considered onboarded:

| Probe | L1 agent | L2 agent | L3 agent |
|-------|----------|----------|----------|
| Read `org-eng-docs/runbooks/foo.md` | ✅ succeeds | ✅ succeeds | ❌ refuses (out of scope) |
| Read `org-company-docs/strategy/q3.md` | ❌ refuses + logs | ✅ succeeds | ❌ refuses |
| Read `drive://people-confidential/perf/EMP-042.md` | ❌ refuses + logs | ❌ refuses (filename visible, content blocked) + logs | ✅ if operator has folder ACL |
| Write `org-eng-docs/new-doc.md` with frontmatter `data_subjects: [EMP-042]` | ❌ refuses (data_subjects not allowed at L1) | n/a | n/a |
| Read `org-company-docs/customer/rfps/c001-2026-q3.md` | ❌ refuses | ✅ succeeds | ❌ refuses |
| Resolve "C001" to real customer name in output | ❌ no access to CODENAMES.yml | ✅ but defaults to codename | ❌ no access to CODENAMES.yml |
| Write a summary of stale docs across all tiers | partial — only L1 | partial — L1+L2 | partial — L3 in Drive scope |

The suite is run by a smoke-test script in `~/agents/{tier}/work/`
that issues each probe via the agent and verifies the expected
outcome. Pass = ready for production use.

(sec-audit)=
## Audit logging

Every agent invocation logs to a per-tier audit file:

```json
{"ts":"2026-05-15T10:32:14Z","agent":"eng-knowledge","operator":"jdoe@example.com","action":"read","target":"org-eng-docs/runbooks/foo.md","tier":"L1","classification":{"C":"MODERATE","I":"MODERATE","A":"LOW"},"prompt_intent":"checking incident response procedure","ok":true}
{"ts":"2026-05-15T10:32:18Z","agent":"eng-knowledge","operator":"jdoe@example.com","action":"refuse","target":"org-company-docs/strategy/q3.md","tier":"L2","reason":"out_of_scope","ok":false}
{"ts":"2026-05-15T10:35:02Z","agent":"eng-knowledge","operator":"jdoe@example.com","action":"write","target":"org-eng-docs/proposals/foo-bar/00-summary.md","tier":"L1","classification":{"C":"MODERATE","I":"MODERATE","A":"LOW"},"diff_sha":"abc123","ok":true}
```

Audit logs are append-only files. Each tier keeps its own;
retention per tier:

- L1: 12 months
- L2: 24 months
- L3: 36 months (longer per most employment-data retention regs)

Logs are themselves L2-classified (they reveal access patterns).
Periodic review (quarterly) flags anomalies: cross-tier refuse rate
above threshold, unusual operator/time-of-day reads, repeated reads
of the same file by different operators within a short window.

(sec-threat-coverage)=
## What this prevents and what it doesn't

### Prevents

- **Agent-mediated cross-tier leak.** An L1 agent literally cannot
  read L2 content; an L2 agent literally cannot read L3 content.
- **Inadvertent over-classification.** When an L2 agent generates
  content for an L1 audience, it's required to summarize and the
  CLAUDE.md spells out the redaction expectation. The agent
  refuses to "just include the L2 detail" in an L1 doc.
- **Stale-credentials persistence.** Per-tier MCP tokens can be
  rotated independently. Compromising the L1 token does not grant
  L2 access.
- **Audit-trail gaps.** Every agent action is logged. A compliance
  reviewer can answer "who accessed this file and when" with a
  query against the audit log.

### Does not prevent

- **Intentional human exfiltration via copy-paste.** An L2 reader
  can paste content into any chat / email / personal note. EKA does
  not solve this; DLP tools and employment-level controls do.
- **Misconfigured ACL.** If a team's `company-docs-readers` team has
  too-broad membership, the L2 boundary is functionally weakened.
  EKA's quarterly access review catches this; it doesn't prevent it.
- **Prompt-injection within source documents.** A malicious or
  compromised document that contains adversarial prompts attempting
  to instruct an L2 agent to leak content. Partial mitigation: hard
  rules in CLAUDE.md + tool scope. Stronger mitigation: input
  sanitization (active research area; not commodity yet).
- **Side-channel inference.** An L1 agent told "C001 launched a
  new product" can infer that C001 is a real customer with an
  active engagement. Codenames prevent name disclosure but not
  existence-of-relationship inference from leaked context.

EKA closes the *accidental* and *agent-mediated* boundary
violations cleanly. The intentional-human and the side-channel
cases require complementary controls outside EKA's scope.

## What's contestable

- **Per-tier separate runtimes** adds operational complexity.
  Smaller orgs may want one agent home with conditional MCP
  loading. EKA's position: the separation is the safety property;
  collapsing to one runtime loses it.
- **CLAUDE.md as the guardrail layer** assumes Claude Code or
  equivalent. Other agent runtimes (LangChain, OpenAI Assistants
  API, custom) need equivalent configuration. EKA's principles
  apply; the implementation differs.
- **Filename-only L3 metadata access** for L2 agents is a
  convenience-versus-security trade-off. Some orgs would prefer no
  cross-tier visibility at all. EKA's position: pointers improve
  usability significantly and filenames at L3 are already
  codenamed.

[The compliance mapping chapter](#chap-compliance-mapping) maps the
controls in this and earlier chapters to NIST SP 800-53, ISO
27002, CIS Controls, and GDPR.
