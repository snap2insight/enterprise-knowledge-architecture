---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-agent-onboarding
      version: 1.0
      agents: [L1, L2, L3]
      side_effects: no
      duration_estimate: 5-10 minutes
      audience: any AI agent encountering EKA for the first time
---

# Skill: eka-agent-onboarding

## Purpose

Bring a fresh AI agent up to operational competence on EKA. Read
this skill once at the start of a new agent session (or whenever
the agent's context has been cleared). After this, the agent
should be able to:

1. Recognize an EKA-conformant repo
2. Operate within its assigned tier's scope
3. Invoke the right skill for the right task
4. Refuse out-of-scope operations correctly
5. Produce conformant frontmatter for new content

This skill is **runtime-agnostic**. It works for Claude Code,
OpenAI Assistants, LangChain agents, or any LLM-based agent that
can read markdown context.

## When to invoke

- An agent runtime is launching against an EKA repo for the
  first time
- The agent's context is fresh (no prior EKA exposure in this
  conversation)
- A skill has been added or updated and the agent should re-read
  the catalog
- An operator says "start fresh" or "what is EKA?"

## Inputs

| Input | Type | Default |
|-------|------|---------|
| `agent_tier` | enum | inferred from agent home (`L1`, `L2`, or `L3`) |
| `agent_home` | path | current working directory |
| `verbose` | bool | `false` — if true, emit the boot sequence as it executes |

## Steps

### 1. Identify the EKA context

The agent reads, in order:

```
1. {agent_home}/CLAUDE.md
   ↳ tier-scoped guardrails, MCP scopes, behavior rules

2. {repo_root}/_meta/manifest.md
   ↳ what's in this repo + cross-tier references

3. {repo_root}/CLASSIFICATION.yml
   ↳ max tier, default classification, hooks, codename rules

4. {repo_root}/CODENAMES.yml  (if at L2+)
   ↳ entity codes and disclosure status
```

If any file is missing, the agent reports:

> "This doesn't appear to be an EKA-conformant repo. I cannot
> operate against it safely. Please run `eka-bootstrap-repo` to
> set up EKA conformance first."

### 2. Internalize the core mental model

The agent commits the following to its working context:

**The five tiers:**

```
L0 Public      — no auth needed
L1 Internal    — auth required (SSO); read by all employees
L2 Confidential— RBAC + need-to-know; small teams
L3 Restricted  — per-file ACL (object store, not Git)
L4 Live secrets— production systems only; not in docs
```

**The six domains** (every doc belongs to exactly one):

```
public | customer | people | business | product | operational
```

**The classification primitive:** FIPS 199 `{C, I, A}` ∈
`{LOW, MODERATE, HIGH}`. Tier is derived, not declared:

```python
if data_subjects: tier = L3
elif C == HIGH: tier = L2
elif C == MODERATE or I == HIGH or A == HIGH: tier = L1
else: tier = L0
```

**Codename rule (L2+):** Real entity names appear in body text
*at first occurrence only*, paired with the codename. File paths
never contain real entity names — only codes.

### 3. Learn the skill catalog

The agent reads `spec/skills/README.md` to know what skills are
available. Maps operator intent to skill:

| Operator intent | Skill to invoke |
|-----------------|-----------------|
| "Set up a new EKA org" | `eka-bootstrap-org` |
| "Set up a new EKA repo in an existing org" | `eka-bootstrap-repo` |
| "What tier is this doc?" | `eka-classify-doc` |
| "Create a new {proposal/runbook/ADR/post-mortem}" | `eka-new-doc` |
| "Review this doc" or "is this OK?" | `eka-review-doc` |
| "Process this erasure request" | `eka-erasure` |
| "What's stale?" | `eka-audit-stale` |
| "Annual audit" | `eka-classification-audit` |

When unclear, the agent asks the operator which skill applies
rather than guessing.

### 4. Confirm tier scope

The agent runs a quick self-test:

```pseudo
expected_tier = read({agent_home}/CLAUDE.md → declared tier)
visible_repos = list(MCP-accessible Git repos)
visible_drive = list(MCP-accessible Drive folders or "none")

If visible_repos includes anything above expected_tier: WARN
If expected_tier == L3 and visible_drive == "none": WARN
```

If any warning fires: report to operator and stop. The MCP
scoping is misconfigured.

### 5. Acknowledge readiness

The agent emits a brief readiness statement:

> "EKA agent onboarded. Tier: {L1/L2/L3}. Reading scope:
> {list of repos / Drive folders}. Available skills: {N}.
> Ready for tasks. What would you like to do?"

## On-going learning (between sessions)

The agent re-reads on every new conversation:
- `CLAUDE.md` (always)
- `_meta/manifest.md` (always)

The agent re-reads on demand:
- `spec/conformance.md` when asked "is this EKA-conformant?"
- `spec/skills/*.skill.md` when invoking that skill
- `spec/reference/*.md` when needing vocabulary

The agent does NOT need to re-read the primer — that's for human
context. Skills are the agent's working context.

## Multi-runtime adaptation

This skill is written for any agent runtime that can read
markdown. Runtime-specific notes:

### Claude Code

Agent home contains `CLAUDE.md`; Claude Code auto-loads it. This
skill is invoked by the agent reading
`spec/skills/eka-agent-onboarding.skill.md` and following the
steps.

### OpenAI Assistants API

The assistant's `instructions` parameter receives the contents
of `{agent_home}/CLAUDE.md`. This skill is invoked by passing
the skill's body as a user message at session start.

### LangChain / LangGraph

`{agent_home}/CLAUDE.md` is loaded as a `SystemMessage` at chain
init. This skill is invoked as a "tool" that reads its own file
contents and returns guidance.

### Other runtimes

Adapt the file-loading pattern. The semantic content is
runtime-independent.

## What the agent must NOT do during onboarding

- Read content above the declared tier
- Resolve codenames to real names (CODENAMES.yml is read for
  reference, not for output)
- Take destructive actions (no commits, no file moves, no API
  calls with side effects)
- Assume the operator has authorized any operation just because
  the operator asked

## Failure handling

| Failure | Recovery |
|---------|----------|
| `CLAUDE.md` not found | Report; ask operator to set up agent home with the right tier template |
| Manifest not found | Report; suggest the repo isn't EKA-conformant and offer to bootstrap |
| MCP scoping is broader than declared tier | STOP; report; do not proceed |
| MCP scoping is narrower than declared tier | Warn but proceed; the agent will see fewer files than full-tier-scope expects |

## What this skill produces

The onboarding skill itself produces no files. It produces a
readiness statement (above) and a populated working context for
the agent to operate from.

After onboarding, the agent invokes one of the **operating-mode
skills** in response to the operator's first real task.
