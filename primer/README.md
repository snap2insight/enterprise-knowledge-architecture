# EKA Primer

> The **why and the what** of Enterprise Knowledge Architecture.

This section is for readers approaching EKA for the first time —
leaders, reviewers, knowledge architects, anyone trying to decide
whether the framework fits their organization or trying to
understand the reasoning behind specific design choices.

If you already know you want to implement EKA and just need the
artifacts, skip ahead to [the spec](../spec/).

## Reading order

| # | Chapter | What's in it |
|---|---------|--------------|
| 0 | [Introduction](00-introduction.md) | Why classify, why now, what changes with AI agents, what changes for compliance, who should adopt |
| 1 | [Principles](01-principles.md) | The eight principles the framework defends, each with an empirical test for "are we doing this right?" |
| 2 | [Classification model](02-classification-model.md) | FIPS 199 CIA triad, six data domains with baselines, the decision tree for classifying a new document, worked examples |
| 3 | [Tier architecture](03-tier-architecture.md) | L0–L4 access tiers, Zero Trust (NIST 800-207) mapping, storage choice rationale, boundary enforcement, promotion/demotion workflows |
| 4 | [Storage & naming](04-storage-and-naming.md) | Repo structure per tier, folder layout, file-naming conventions, the codename scheme for L2+ content |
| 5 | [Metadata & labeling](05-metadata-and-labeling.md) | Frontmatter schema in narrative form; the rationale for each field |
| 6 | [Lifecycle & review](06-lifecycle-and-review.md) | Review cadence, graduated staleness, GDPR Article 17 erasure, offboarding flows |
| 7 | [Agent topology](07-agent-topology.md) | Per-tier agents, MCP scoping, working-directory boundaries, what this prevents and what it doesn't |
| 8 | [Compliance mapping](08-compliance-mapping.md) | NIST 800-53, ISO/IEC 27002, CIS Critical Security Controls, GDPR Article 25/17, FIPS 199, NIST 800-207 |
| 9 | [Tooling stack](09-tooling-stack.md) | Required tools, recommended tools, what we deliberately don't recommend, source-to-artifact pipeline |
| 10 | [Implementation roadmap](10-implementation-roadmap.md) | Four-week rollout with phase exit gates, cost expectations |

## What's in each chapter

Each primer chapter follows a consistent structure:

1. **Topic motivation** — why this chapter exists in the framework
2. **The model / design** — the prescriptive content
3. **Worked examples** — concrete cases (this is where the rubber
   meets the road)
4. **What's contestable** — design choices reasonable people will
   disagree with, called out explicitly for review

The "What's contestable" sections are the most valuable for peer
review. They surface decisions that warrant debate rather than
quietly defaulting.

## What this is not

The primer is **not** the spec. It does not contain:

- JSON Schema for frontmatter (see [spec/schemas/](../spec/schemas/))
- Ready-to-clone repo templates (see [spec/templates/](../spec/templates/))
- Pre-commit hook implementations (see [spec/hooks/](../spec/hooks/))
- Agent skill definitions (see [spec/skills/](../spec/skills/))
- Operational runbooks (see [spec/operations/](../spec/operations/))

If you're reading the primer and find yourself wanting to know
"OK how do I actually do this in my repo?" — that's your cue to
move to [the spec](../spec/).

## Next steps

After reading the primer, paths diverge:

- **Decide whether to adopt:** Take [Principles](01-principles.md)
  and [Roadmap](10-implementation-roadmap.md) to your leadership
  team. The "What's contestable" sections frame the conversation.
- **Plan the adoption:** Use [Implementation roadmap](10-implementation-roadmap.md)
  + [Tooling stack](09-tooling-stack.md) to size the work.
- **Start building:** Move to [the spec](../spec/) and begin with
  the [bootstrap-org skill](../spec/skills/eka-bootstrap-org.skill.md).
