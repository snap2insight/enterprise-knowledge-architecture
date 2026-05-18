# CLAUDE.md templates (per tier)

The agent-runtime guardrails for each access tier. Copy the
template matching the agent's tier into the agent's home
directory as `CLAUDE.md`.

## Templates

| Tier | Template | Use case |
|------|----------|----------|
| L1 | [`L1.claude.template.md`](L1.claude.template.md) | Internal eng-docs agent — read/write L1 content, read Plane, read Chat |
| L2 | [`L2.claude.template.md`](L2.claude.template.md) | Confidential agent — read L1+L2, list (but not read) L3 metadata, codename discipline |
| L3 | [`L3.claude.template.md`](L3.claude.template.md) | Restricted agent — Drive-scoped to operator's accessible folders, per-file ACL discipline |

## Agent-runtime adaptation

These files are named `CLAUDE.md` because [Claude Code](https://claude.ai/code)
auto-loads files of that name. **The content is portable to any
agent runtime.** Adaptation paths:

| Runtime | How to load |
|---------|-------------|
| Claude Code | Place at `~/agents/{name}/CLAUDE.md`; Claude Code reads it as system context automatically |
| OpenAI Assistants API | Pass the file content as the assistant's `instructions` parameter; refresh on tier change |
| LangChain / LangGraph | Load as a `SystemMessage` at the start of every chain run |
| Custom agent | Read the file at agent boot; prepend to system prompt; reload on every conversation |

For multi-runtime support: keep one `CLAUDE.md` per agent home as
the canonical source; have a small wrapper script that translates
to whatever your runtime needs (most runtimes accept markdown
verbatim).

> **Conformance note:** The EKA spec is runtime-agnostic. The
> CLAUDE.md naming is the only Claude-specific convention; it
> survives non-Claude runtimes because the content is just
> markdown + structured rules.

## Per-tier setup

### L1

```bash
mkdir -p ~/agents/{org}-eng-knowledge
cp spec/templates/claude-md/L1.claude.template.md \
   ~/agents/{org}-eng-knowledge/CLAUDE.md
# Edit placeholders: {org}, MCP tokens, etc.
```

### L2

```bash
mkdir -p ~/agents/{org}-company-knowledge
cp spec/templates/claude-md/L2.claude.template.md \
   ~/agents/{org}-company-knowledge/CLAUDE.md
```

### L3

```bash
mkdir -p ~/agents/{org}-people-knowledge
cp spec/templates/claude-md/L3.claude.template.md \
   ~/agents/{org}-people-knowledge/CLAUDE.md
# Configure Drive MCP with OAuth scoped to operator's folders
```

## Smoke test after setup

Run the negative-probe smoke test for the tier:

```bash
eka agent-smoke-test --tier L1 --home ~/agents/{org}-eng-knowledge/
```

A passing test confirms the agent can do what it should and
refuses what it shouldn't. See
[`primer/07-agent-topology.md`](../../../primer/07-agent-topology.md)
for the smoke-test rationale.
