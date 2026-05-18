# Content-type templates

Pre-filled frontmatter + body skeletons for common document
types. Copy the right template, then customize.

## Templates

| Type | Template | Default cadence | Default classification |
|------|----------|-----------------|------------------------|
| Proposal / RFC | [`proposal.template.md`](proposal.template.md) | 180d | { C: MODERATE, I: HIGH, A: LOW } |
| Runbook | [`runbook.template.md`](runbook.template.md) | 180d | { C: MODERATE, I: HIGH, A: HIGH } |
| ADR (Architecture Decision Record) | [`adr.template.md`](adr.template.md) | 365d | { C: MODERATE, I: HIGH, A: LOW } |
| Post-mortem | [`post-mortem.template.md`](post-mortem.template.md) | 365d | { C: MODERATE, I: HIGH, A: MODERATE } |
| Weekly digest | [`digest.template.md`](digest.template.md) | 7d | { C: LOW, I: MODERATE, A: LOW } |

## How an agent uses these

[`eka-new-doc`](../../skills/eka-new-doc.skill.md) picks the
template by `content_type` input and pre-fills frontmatter. Manual
equivalent:

```bash
cp spec/templates/content-types/proposal.template.md \
   proposals/my-thing/00-summary.md
# Edit body and fill placeholders
```

## Customizing per tier

The default classifications above are for L1 internal content.
When authoring at L2, raise classification.C to HIGH and add
`codename_refs:` for any entities referenced. The agent's
`eka-classify-doc` skill can recommend adjustments.
