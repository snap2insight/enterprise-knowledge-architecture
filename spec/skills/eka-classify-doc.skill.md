---
options:
  eka:
    schema: eka.v1.skill
    skill:
      skill_id: eka-classify-doc
      version: 1.0
      agents: [L1, L2, L3]
      side_effects: no
      duration_estimate: 2-5 minutes
---

# Skill: eka-classify-doc

## Purpose

Given a markdown document (existing or draft), determine its EKA
classification: FIPS 199 CIA tuple, domain, tier, and any required
`data_subjects` / `codename_refs` declarations.

## When to invoke

- Migrating an existing document into an EKA-conformant repo
- Reviewing a draft to decide where it belongs
- Auditing a repo to spot misclassified content
- An operator pastes a doc into chat and asks "what tier is this?"

## Inputs

Required:

| Input | Type | Notes |
|-------|------|-------|
| `document_text` | string or file path | The full markdown content |

Optional:

| Input | Default | Description |
|-------|---------|-------------|
| `intended_repo` | autodetect | Which repo this would land in |
| `target_audience` | derived | Who'll read it — affects tier |

## Steps

### 1. Read the document

If a file path: read it; report any frontmatter that already exists
(may inform but does NOT override the agent's classification).

If a text blob: parse as markdown; extract title (first H1), prose
body, any inline references.

### 2. Identify the domain

Apply the decision tree (mentally; from the primer):

1. Is this externally-facing / publishable? → `public`
2. Does it reference individuals (employees, candidates,
   board members, customer-side people)? → `people`
   (or `customer` if customer-side data subjects)
3. Does it contain customer-relationship specifics
   (RFP, contract, customer-engagement strategy)? → `business`
   (Customer Data is L3 territory; this is `business` for
   summaries and meta-content)
4. Customer-identifiable records, raw customer data? →
   `customer` (almost always L3)
5. Strategy / financials / RFP / board content? → `business`
6. Source code design, IP, ML model design? → `product`
7. Infrastructure plans, operational secrets, runbooks? →
   `operational`

If multiple apply, pick the *primary* one (the one whose owner is
most directly responsible).

### 3. Rate confidentiality, integrity, availability

For each of C, I, A: apply the worst-case-loss test.

| Axis | LOW | MODERATE | HIGH |
|------|-----|----------|------|
| C | Embarrassing if leaked; no regulatory exposure | Damages competitive position; customer/employee trust hit; investigation | Customer contract termination, regulatory action, individual privacy harm |
| I | Wrong content is annoying but not harmful | Wrong content damages decisions; recovery weeks | Wrong content harms customers / breaks regulatory commitments |
| A | Inconvenient if unavailable; can wait days | Affects operations during the outage; recovery hours | Business stops or incident escalates |

Reason out loud before deciding; pick the rating only after
explicitly considering each level.

### 4. Identify data subjects

Scan body for any identifiable individual references:

- Named employees → likely `EMP-NNN` (operator must confirm code)
- Named candidates → `CAND-YYYY-WNN-NNN`
- Named board members → `BOARD-NNN`
- Customer-side individuals → flag as "customer PII; consider L3"

If `data_subjects` is non-empty, the tier is at least L2.

### 5. Identify codename refs

Scan body for any externally-confidential entities. If the agent is
L2-scoped, cross-reference against `CODENAMES.yml`. If L1-scoped,
flag potential codename candidates without confirming names.

### 6. Derive the tier

```
if data_subjects: tier = L3
elif C == HIGH: tier = L2
elif C == MODERATE or I == HIGH or A == HIGH: tier = L1
else: tier = L0
```

### 7. Produce the classification recommendation

Output the suggested frontmatter block:

```yaml
domain: ...
classification:
  C: ...
  I: ...
  A: ...
tier: ...
data_subjects: [...]
codename_refs: [...]
```

Plus reasoning:

> "Classified as L2 because:
> - Contains customer-specific RFP language → C HIGH
> - References named customer (mapped to C001) → codename_ref [C001]
> - No identifiable individuals beyond corporate entities → no data_subjects
> - Domain = business (customer-engagement strategy)
> - Suggested home: `{org}-company-docs/customer/rfps/c001-...md`"

### 8. Identify any issues for the operator

- "This doc cannot live at L1 — has HIGH confidentiality"
- "The doc mentions individuals; needs L3 placement and EMP codes"
- "The file path you proposed contains a real customer name;
  rename to c001-..."

## Validations

- Every classification field is present
- The classification → tier derivation is consistent
- Recommended path follows L2+ codename rules

## Outputs

A classification recommendation document with:

1. The full frontmatter block (ready to paste)
2. The reasoning (3-5 bullet points)
3. The recommended repo and file path
4. Any flags the operator must address before commit

## Failure handling

| Failure | Recovery |
|---------|----------|
| Document is empty or trivially short | Decline to classify; ask for substantive content |
| Document mixes multiple distinct topics | Recommend splitting; classify each fragment separately |
| Agent's tier doesn't permit reading the doc | Refuse; recommend higher-tier agent |
| Cannot decide between two domains | Ask operator; offer both with pros/cons |
