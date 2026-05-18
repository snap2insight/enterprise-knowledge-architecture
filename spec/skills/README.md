# EKA Skills

> Agent-actionable workflow definitions. Each skill is a markdown
> file that an AI agent (Claude Code or equivalent) reads as a
> prompt-context to execute a defined workflow.

## What a skill is

A skill file describes:

1. **Purpose** — what problem the skill solves, in one line
2. **When to invoke** — what user requests trigger it
3. **Preconditions** — what must be true before invoking
4. **Inputs** — what the agent needs to know
5. **Steps** — the workflow as a numbered procedure
6. **Validations** — checks at each step
7. **Outputs** — what the agent produces
8. **Failure handling** — what to do when things go wrong

Skills are designed to be **agent-runnable** rather than
human-runnable. They're written in the imperative voice ("do X,
then verify Y") and assume the agent has the relevant tool
access (file I/O, MCP servers, shell commands).

## The skill catalog

| Skill | What it does | When to invoke |
|-------|--------------|----------------|
| [eka-agent-onboarding](eka-agent-onboarding.skill.md) | Bring a fresh agent up to operational competence on EKA | First conversation in a new agent home; context reset |
| [eka-bootstrap-org](eka-bootstrap-org.skill.md) | Set up an entire EKA-conformant org from blank | New org adopting EKA |
| [eka-bootstrap-repo](eka-bootstrap-repo.skill.md) | Set up a single EKA repo within an existing org | New L1/L2 repo needed |
| [eka-classify-doc](eka-classify-doc.skill.md) | Classify an existing markdown document | Migrating content to EKA; reviewing draft classification |
| [eka-new-doc](eka-new-doc.skill.md) | Create a new document with the right template + frontmatter | Author starting a new proposal/runbook/ADR |
| [eka-review-doc](eka-review-doc.skill.md) | Review an existing doc for tier-appropriateness | PR review, quarterly audit |
| [eka-erasure](eka-erasure.skill.md) | Process a GDPR Article 17 erasure request | Privacy admin received an erasure request |
| [eka-audit-stale](eka-audit-stale.skill.md) | Find stale documents and produce a report | Monthly cadence |
| [eka-classification-audit](eka-classification-audit.skill.md) | Run the annual classification audit | Annual cadence |

## How an agent invokes a skill

In Claude Code (and similar runtimes), the agent reads the skill
file directly via `Read` and then executes the steps. Patterns:

### Operator-initiated

User: *"Bootstrap a new EKA-conformant L1 repo called `acme-eng-docs`."*

Agent:
1. Reads `spec/skills/eka-bootstrap-repo.skill.md`
2. Extracts inputs from operator (or asks): `repo_name`, `tier`,
   `domain`, etc.
3. Executes the skill's steps
4. Reports back

### Agent-initiated (during operation)

When the agent encounters a situation that maps to a skill, it
invokes the skill automatically. Example: an operator pastes a
draft markdown into the conversation; the agent recognizes "this
needs classification" and invokes `eka-classify-doc`.

## How to author a new skill

If you find your team running the same workflow repeatedly,
codify it as a skill:

1. Copy `_template.skill.md` (TODO: ship this template)
2. Fill in the eight sections
3. Test by invoking with a sample input
4. Iterate until the agent produces consistent outputs

A good skill is **idempotent** — running it twice produces the
same result. If your workflow has side effects (creates repos,
sends emails), the skill must declare that explicitly so the
agent doesn't accidentally double-execute.

## Tier scoping for skills

Each skill declares which tier(s) of agent may invoke it:

- `agents: [L1, L2, L3]` — any tier
- `agents: [L2, L3]` — confidential and above
- `agents: [L2]` — L2 only (e.g., codename-management skills)

An L1 agent attempting to invoke an L2-only skill should refuse:

> "This skill requires L2 agent context. Invoke from the
> company-knowledge agent home."
