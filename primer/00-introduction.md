(chap-introduction)=
# 00 — Introduction

## The problem

Most companies grow their documented knowledge by accretion. Engineers
write a runbook in one repo, a design doc in another, a 1:1 note in a
shared Drive folder, a strategy memo in someone's local Notion. Each
document is born in whichever tool was open at the time. Classification —
the question of "who should be able to read this?" — gets answered
implicitly by storage choice, and is reviewed by no one.

This worked, in a brittle way, when consumption was human-only. A
careless storage choice mostly hurt findability (people couldn't locate
the doc) rather than leaking it (the doc was internal anyway, in some
tool that auth-gated everything). The penalty for poor structure was
"wasted minutes searching."

Two changes break that equilibrium:

1. **LLM-based agents now read and write documents at machine scale.**
   An agent answering an engineer's question doesn't manually browse —
   it ingests whatever it can reach. If the agent's reach crosses
   classification boundaries (intentionally or accidentally), the
   classification breach is no longer a worst-case scenario but a
   default outcome.
2. **Enterprise customers demand evidence.** A Fortune-500 customer's
   security questionnaire now asks "show us your data classification
   scheme" and "show us how access is controlled per classification."
   "We use Confluence with team-based permissions" is no longer a
   sufficient answer.

The cost of leaving knowledge organization implicit has gone up.

## What changes when AI agents enter the picture

Agents change three things about how a knowledge base must be designed:

1. **Boundaries must be machine-enforceable, not policy-based.**
   "Don't read sensitive content" doesn't work as an instruction to an
   agent, the same way it doesn't work as an instruction to a query
   optimizer. The boundaries must be expressed in the structure
   (separate stores, separate auth realms) so that no instruction is
   needed.

2. **Metadata becomes load-bearing.** Humans can infer that a document
   in a folder called "Customer RFPs" is confidential. Agents need it
   declared. The frontmatter field `classification.confidentiality:
   HIGH` is no longer documentation overhead — it's the agent's only
   reliable signal.

3. **Cross-tier reasoning becomes a deliberate operation.** A human
   working on a project can hold both an internal-tier design doc and a
   confidential customer-specific requirement in their head and produce
   output that respects both boundaries. An agent will produce output
   that *mixes* them unless the architecture prevents that mix from
   forming in the first place.

EKA addresses all three: classification is in-document metadata,
boundaries are storage-level (different repos, different stores),
agents are tier-scoped and audit-logged.

## What changes for compliance

The same metadata that makes a knowledge base safe for agents makes it
auditable for compliance frameworks. Specifically:

- **NIST SP 800-53** Access Control (AC) and Audit (AU) families need
  evidence that classified data has classified controls. EKA's
  per-document classification, repo-tier ACLs, and pre-commit
  enforcement provide that evidence as a queryable artifact.
- **ISO/IEC 27002** Controls 5.12 (Classification of information) and
  5.13 (Labelling of information) are satisfied by EKA's frontmatter
  schema and the validation hooks that enforce it.
- **GDPR Article 25** (Data protection by design and by default) is
  satisfied by EKA's pseudonymization (codenames at L2+),
  data-minimization defaults, and erasure-compatible metadata
  (`data_subjects:` tagging).
- **CIS Critical Security Control 3** (Data Protection) sub-controls
  3.1–3.7 map directly to EKA practices.

A company that adopts EKA does not have to retrofit a classification
scheme later — it ships with one. That is the "by design" part of the
tagline.

## What changes for humans

The day-to-day experience of writing docs *barely changes*:

- Authors write markdown in their preferred editor.
- Frontmatter adds ~10 fields at the top of each new file (auto-filled
  by templates 90% of the time).
- File names get a small adjustment at L2+ (codenames instead of real
  entity names). One lookup table.
- A pre-commit hook occasionally rejects a commit that classifies
  wrongly. Five-second fix.

The high-leverage part is what *doesn't* happen: arguments about where
to put a doc, weeks-long retrofits for a customer audit, agents that
return uncomfortable responses, lost work when an employee leaves and
their personal Notion goes with them.

## Why a startup should care now

The argument "we'll deal with knowledge architecture when we hit 500
engineers" is the same argument that produced messy codebases at 50
engineers. The right time to set classification conventions is when
there are still few enough documents to migrate, few enough teams to
align, and few enough customers asking for evidence.

EKA is designed to be **adoptable in four weeks by a startup of <30
engineers, with zero new vendor contracts**. The next-to-last chapter
sketches the rollout in detail.

## What's contestable

A few choices in this introduction reasonable people will disagree
with:

- **"AI agents read and write at machine scale" assumes a future where
  agents are deeply integrated into knowledge workflows.** If your
  company isn't using agents, the agent-specific parts of EKA are
  forward-investment, not present-tense need. (But the
  classification-by-design parts pay off independently.)
- **"Enterprise customers demand evidence."** True if you sell into
  regulated industries or large enterprises. Less pressing if your
  customer base is SMB. The framework still applies; the urgency
  shifts.
- **"Classification by design is feasible at startup scale."** Some
  practitioners argue that startups should *not* prematurely
  formalize, on the grounds that it slows them down. EKA explicitly
  rejects this position — the marginal effort is low and the cost of
  retrofitting later is high — but the position exists and is worth
  hearing out before committing.

[The principles chapter](#chap-principles) lays out the eight design
principles that the rest of the spec defends.
