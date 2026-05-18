# Agent home for this repo

Agents operating against this repo MUST follow the boot routine
defined here and in `_meta/manifest.md`.

## Pick the right CLAUDE.md

The CLAUDE.md (or equivalent) used by an agent operating in this
repo MUST match the repo's `max_tier`. Templates live in the EKA
spec:

- `spec/templates/claude-md/L1.claude.template.md` → for L1 repos
- `spec/templates/claude-md/L2.claude.template.md` → for L2 repos
- `spec/templates/claude-md/L3.claude.template.md` → for L3 agent
  homes operating against Drive content

Copy the template appropriate for this repo's tier into this
folder as `CLAUDE.md`, fill in the ALL_CAPS placeholders, and
commit. The CLAUDE.md belongs in the repo (so it's auditable);
the agent's MCP tokens do NOT belong in the repo (those live in
the operator's local `.claude/` and are gitignored).

## Boot sequence

When Claude Code (or any agent runtime) launches in a context that
includes this repo:

1. Read `_agents/CLAUDE.md` first.
2. Read `_meta/manifest.md` second.
3. Read `CLASSIFICATION.yml`.
4. (If L2+) Read `CODENAMES.yml`.
5. Confirm MCP scopes match the declared tier.

## Smoke tests

After installing or rotating the agent, run the negative-probe
smoke test for this tier:

```bash
# from your agent home
eka agent-smoke-test --tier {TIER}
```

The test runs:
- 5 positive probes (operations within tier — should succeed)
- 5 negative probes (operations across tier — should refuse + log)

Pass = the agent is ready for production use against this repo.
Failure = stop and investigate; the agent has the wrong tier
scoping.

## Audit log

The agent's audit-log destination is declared in this repo's
`CLASSIFICATION.yml` (`audit_log.destination`). Confirm the
destination is reachable before first use.
