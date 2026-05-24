---
title: "ADR-NNNN — DECISION_TITLE"
options:
  eka:
    schema: eka.v1
    domain: product
    classification: {C: MODERATE, I: HIGH, A: LOW}
    tier: L1
    owner: DECIDING_ARCHITECT
    status: proposed        # proposed | accepted | superseded | deprecated
    last_reviewed: YYYY-MM-DD
    next_review: YYYY-MM-DD
    review_cadence: 365d
    codename_refs: []
    data_subjects: []
    labels: [adr, architecture]
    related: []
    supersedes:
    superseded_by:
---

# ADR-NNNN — DECISION_TITLE

| Field | Value |
|-------|-------|
| **Status** | proposed |
| **Confidence** | high |
| **Date** | YYYY-MM-DD |
| **Decision-makers** | NAME, NAME |
| **Consulted** | NAME, NAME |
| **Informed** | NAME, NAME |
| **Supersedes** | — |
| **Superseded by** | — |
| **Related** | [linked doc](path/to/doc) |

<!--
SCOPE GUARD — Read before writing.

This template aligns with the Nygard ADR format
(https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html)
and MADR (https://adr.github.io/madr/), extending both with EKA-specific
fields: Confidence level, explicit Tradeoffs table, Rationale sub-section,
and RACI Consulted/Informed rows.

An ADR records ONE decision. It is not a design guide, not a proposal,
and not a tutorial. If explaining HOW to implement the decision is
necessary, write a proposal or runbook and link it from § References.

The ADR must stand alone: a reader who cannot open any linked document
should still understand what was decided and why. Links are for depth,
not load-bearing.

Multi-phase decisions: if the decision has distinct phases where each
phase could be reconsidered independently, write one ADR per phase.

Style: pithy, assertive, present tense, factual. Target 1–2 pages.
Avoid hedging. "We store X in Y" — not "We will consider storing X in Y".
-->

## Context

<!--
State the problem and the forces at play — NOT the solution.
Answer:
  - What system or constraint triggered this decision NOW?
  - What happens if no decision is made?
  - What changed since the last related decision?
-->

DESCRIBE_THE_PROBLEM_AND_FORCES.

## Decision Drivers

<!--
OPTIONAL. List the specific criteria used to evaluate the options.
These are the forces that matter most for this decision — functional
requirements, quality attributes, constraints, risks. Keep it short;
each driver should appear in the pros/cons under § Options considered.

Example drivers:
- Must not increase operational complexity
- Must stay within current Azure budget envelope
- Must be reversible within one sprint
-->

- DRIVER_1
- DRIVER_2

## Options considered

<!--
List every option you seriously evaluated, including the status quo.
"We didn't consider X" is a gap in the record.
One or two sentences per option + pros/cons is the right depth.
Reference the decision drivers above in the pros/cons where relevant.
-->

### Option A — NAME

BRIEF_DESCRIPTION.

**Pros:** …
**Cons:** …

### Option B — NAME

BRIEF_DESCRIPTION.

**Pros:** …
**Cons:** …

### Option C — Status quo (do nothing)

**Pros:** …
**Cons:** …

## Decision

**We will DECISION_STATEMENT_IN_PRESENT_TENSE.**

### Rationale

<!--
Explain WHY this option, not the others. Don't repeat the pros/cons;
make the argument. What was the decisive factor? What did you weigh
more heavily? What specific condition would cause you to revisit?
-->

DECISIVE_REASONING_HERE.

## Tradeoffs

<!--
State what we are giving up or accepting in exchange for this outcome.
Be honest. If there are no tradeoffs, the decision was not real.

This section is NOT the same as § Consequences:
  - Tradeoffs are deliberate exchanges (we trade X for Y).
  - Consequences are downstream effects of having made the decision.
-->

| We gain | We give up / accept |
|---------|---------------------|
| … | … |

## Consequences

<!--
ALL material consequences — positive, negative, and neutral.
No hidden consequences: if you know about a downside, list it here.
A reviewer who finds an unlisted consequence should reject the ADR
and ask for a revision.
-->

### Positive

- …

### Negative

- …

### Neutral

- …

### Risks

<!--
Known conditions under which this decision could prove wrong.
For each risk: state the trigger that would invalidate the decision
and the mitigation or re-evaluation path.
-->

| Risk | Trigger | Mitigation / re-evaluation |
|------|---------|---------------------------|
| … | … | … |

## Confirmation

<!--
OPTIONAL. How do we know this decision was implemented correctly?
Describe what reviewers or automated checks should verify.

Examples:
- "Architecture review in the next design sync."
- "Integration test covers the X path end-to-end."
- "A follow-up ADR is required before phase 3 begins."
- "Monitored via the SLA dashboard for 30 days post-deploy."
-->

CONFIRMATION_METHOD_OR_OMIT_SECTION.

## References

<!--
Link supplemental material — design docs, proposals, vendor benchmarks —
but the ADR must stand alone. A reader who cannot open these links should
still understand the decision.

See also: https://adr.github.io/ for the community ADR standard this
template is based on.
-->

- …
