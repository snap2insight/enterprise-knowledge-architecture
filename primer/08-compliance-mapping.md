(chap-compliance-mapping)=
# 08 — Compliance Mapping

This chapter maps EKA's controls to recognized standards so that the
same frontmatter, hooks, and processes produce compliance evidence
for multiple frameworks at once.

Contents:

- [The compliance stack](#sec-compliance-stack)
- [NIST SP 800-53 control mapping](#sec-nist-800-53)
- [ISO/IEC 27002 control mapping](#sec-iso-27002)
- [CIS Critical Security Control 3](#sec-cis-3)
- [FIPS 199 (already used)](#sec-fips-199-mapping)
- [GDPR Article 25 and 17](#sec-gdpr)
- [NIST SP 800-207 Zero Trust](#sec-zero-trust-mapping)
- [Evidence package for an audit](#sec-audit-evidence)

---

(sec-compliance-stack)=
## The compliance stack

EKA references multiple standards because no single standard covers
everything. The stack:

| Layer | Standard | What it gives EKA |
|-------|----------|-------------------|
| Strategy | ISO/IEC 27001 | Information Security Management System framework — the "you have a program" anchor |
| Controls | NIST SP 800-53 | Comprehensive control catalog — vocabulary for what's in place |
| Classification | NIST SP 800-60 + FIPS 199 | How to label data by impact |
| Tactics | CIS Critical Security Controls | What to do first, second, third |
| Architecture | NIST SP 800-207 (Zero Trust) | How to enforce access |
| Privacy | GDPR (esp. Art. 25, 17, 32) | EU privacy by-design + erasure |
| US Privacy | CCPA/CPRA, HIPAA-adjacent, FTC Safeguards | State + sectoral privacy |
| International | ISO/IEC 27002 5.12 + 5.13 | Classification + labeling concrete controls |

Different audiences read different parts. An EU customer's vendor
questionnaire asks about ISO 27001 + GDPR. A US enterprise customer
asks about NIST 800-53 + SOC 2. A regulated-industry customer adds
their sector standard (HITRUST, PCI, FedRAMP). EKA's job is to
expose evidence in whatever vocabulary the audience needs.

(sec-nist-800-53)=
## NIST SP 800-53 control mapping

The controls EKA implements, by family:

### AC — Access Control

| Control | EKA implementation |
|---------|-------------------|
| **AC-2 Account Management** | Tier-team membership tracked in GitHub; quarterly access review; offboarding workflow ([chapter 6](#sec-offboarding)) |
| **AC-3 Access Enforcement** | Repo-level ACL per tier ([P2](#chap-principles)); pre-commit hook enforces classification ≤ max_tier ([P5](#sec-pre-commit)) |
| **AC-4 Information Flow Enforcement** | Cross-tier reference resolution restricted by agent scope ([P6](#chap-agent-topology)); MCP scoping per tier |
| **AC-6 Least Privilege** | Per-tier agents with scoped MCPs; CLAUDE.md guardrails; need-to-know required for L2 |
| **AC-22 Publicly Accessible Content** | L0 tier deliberately separated; demotion workflow requires reviewer ([sec-promotion-demotion](#sec-promotion-demotion)) |

### AU — Audit and Accountability

| Control | EKA implementation |
|---------|-------------------|
| **AU-2 Event Logging** | Every agent action logged ([sec-audit](#sec-audit)); GitHub audit log retained 12+ months; Drive audit log per Workspace policy |
| **AU-3 Content of Audit Records** | Audit format includes operator, action, target, classification, intent, outcome |
| **AU-9 Protection of Audit Information** | Audit logs append-only; logs are L2-classified; periodic integrity verification |
| **AU-11 Audit Record Retention** | Per-tier retention: L1=12mo, L2=24mo, L3=36mo |

### IA — Identification and Authentication

| Control | EKA implementation |
|---------|-------------------|
| **IA-2 User Identification and Authentication** | GitHub Enterprise SSO; Workspace SSO; per-tier MCP tokens with separate auth realms |
| **IA-5 Authenticator Management** | Per-tier tokens rotated independently; secrets gitignored; OAuth scopes minimized for Drive MCP |

### MP — Media Protection

| Control | EKA implementation |
|---------|-------------------|
| **MP-6 Media Sanitization** | GDPR Article 17 erasure workflow ([sec-erasure](#sec-erasure)); tombstone format; optional `git filter-repo` for severe cases |

### SC — System and Communications Protection

| Control | EKA implementation |
|---------|-------------------|
| **SC-7 Boundary Protection** | Per-tier repos / stores; storage-enforced boundaries ([sec-boundaries](#sec-boundaries)); MCP scoping |
| **SC-8 Transmission Confidentiality and Integrity** | TLS everywhere — Git over HTTPS / SSH; Drive over HTTPS; MCP over authenticated TLS |
| **SC-12 Cryptographic Key Management** | Codename mapping in CODENAMES.yml is itself L2-classified; production secrets in Key Vault (L4, out of EKA scope) |
| **SC-28 Protection of Information at Rest** | Git repository contents encrypted at rest by provider; Drive at-rest encryption by provider; device-level encryption (FileVault / BitLocker) required for laptops storing synced markdown |

### SI — System and Information Integrity

| Control | EKA implementation |
|---------|-------------------|
| **SI-12 Information Handling and Retention** | Classification + lifecycle ([chapter 6](#chap-lifecycle-and-review)); retention per tier; review cadence enforced |

### PS — Personnel Security

| Control | EKA implementation |
|---------|-------------------|
| **PS-3 Personnel Screening** | Out of EKA scope; HR responsibility. EKA flags personnel-sensitive content via `data_subjects:` and L3 placement |
| **PS-4 Personnel Termination** | Offboarding workflow ([sec-offboarding](#sec-offboarding)); access revocation; ownership reassignment |

### RA — Risk Assessment

| Control | EKA implementation |
|---------|-------------------|
| **RA-2 Security Categorization** | FIPS 199 SC tuple per document; per-domain baselines; pre-commit validation |
| **RA-3 Risk Assessment** | Annual classification audit ([sec-annual-audit](#sec-annual-audit)); threat models live at L2 |

### CM — Configuration Management

| Control | EKA implementation |
|---------|-------------------|
| **CM-2 Baseline Configuration** | `CLASSIFICATION.yml` per repo declares baseline; deviations require explicit `override_reason` |

(sec-iso-27002)=
## ISO/IEC 27002 control mapping

ISO 27002 is the operational companion to ISO 27001. EKA satisfies
key clauses:

| ISO 27002 control | EKA implementation |
|-------------------|--------------------|
| **5.12 Classification of information** | FIPS 199-based CIA classification per document; six-domain decomposition; domain baselines |
| **5.13 Labelling of information** | Frontmatter labels with title, classification, tier, domain, owner, status, codenames, data_subjects |
| **5.14 Information transfer** | Cross-tier reference scheme with URI types (`repo:`, `drive:`, `plane:`); explicit promotion / demotion workflow |
| **5.15 Access control** | Per-tier RBAC via GitHub teams + Drive folder ACLs; least-privilege agent topology |
| **5.18 Access rights** | Quarterly access review; offboarding revokes immediately; CODENAMES.yml's `disclosure` field tracks ongoing relevance |
| **5.31 Legal, statutory, regulatory and contractual requirements** | Compliance mapping (this chapter); per-tier retention; GDPR erasure workflow |
| **5.34 Privacy and protection of PII** | Pseudonymization via codenames; `data_subjects` tagging; L3 separation for personnel data |
| **6.3 Information security awareness, education and training** | The EKA spec itself; per-tier CLAUDE.md guardrails for agents |
| **8.10 Information deletion** | Tombstone format; archive workflow; quarterly purge-candidate review |
| **8.11 Data masking** | Codename scheme in body text; redaction format for demotion |
| **8.12 Data leakage prevention** | Pre-commit hooks (catch classification drift before commit); agent tier-scoping (catch cross-tier reads at runtime) |

(sec-cis-3)=
## CIS Critical Security Control 3 (Data Protection)

CIS Control 3 provides the staged-rollout priority. EKA implements
sub-controls 3.1 through 3.7:

| CIS sub-control | EKA implementation | Implementation phase |
|------------------|--------------------|--------------------|
| **3.1 Establish and maintain a data management process** | EKA spec itself; CLASSIFICATION.yml per repo | Phase 1 (Q1) |
| **3.2 Establish and maintain a data inventory** | `_meta/manifest.md` per repo; cross-repo inventory in the eng-docs manifest | Phase 1 (Q1) |
| **3.3 Configure data access control lists** | Per-tier repo / Drive ACLs; pre-commit hooks; agent MCP scoping | Phase 1 (Q1) |
| **3.4 Enforce data retention** | Tier-specific retention; lifecycle workflow ([chapter 6](#chap-lifecycle-and-review)) | Phase 2 (Q2) |
| **3.5 Securely dispose of data** | GDPR Article 17 erasure workflow; tombstone format; quarterly purge review | Phase 2 (Q2) |
| **3.6 Encrypt data on end-user devices** | Mandatory FileVault / BitLocker on laptops handling synced markdown; documented in onboarding | Phase 1 (Q1) |
| **3.7 Establish and maintain a data classification scheme** | FIPS 199 CIA + six domains + tiers; this whole spec | Phase 1 (Q1) |

Higher-numbered CIS-3 sub-controls (3.8 onwards — primarily about
cryptographic protection of data in transit, encryption of mobile
endpoints, etc.) are organizational concerns outside EKA's primary
scope. EKA references them but does not implement.

(sec-fips-199-mapping)=
## FIPS 199 mapping

FIPS 199 is already EKA's core classification language. Mapping is
identity:

| FIPS 199 | EKA |
|----------|-----|
| Security Objective: Confidentiality | `classification.C` in frontmatter |
| Security Objective: Integrity | `classification.I` |
| Security Objective: Availability | `classification.A` |
| Impact level: LOW / MODERATE / HIGH | Same |
| Security Category (SC) tuple | `classification` block as a whole |
| Information type | `domain` field |

A FIPS 199 audit would read EKA's frontmatter directly. No
translation layer needed.

(sec-gdpr)=
## GDPR Article 25 and 17

### Article 25 — Data protection by design and by default

| GDPR Art. 25 requirement | EKA implementation |
|--------------------------|--------------------|
| **Data minimization** | Per-document classification forces explicit reasoning about *what data is in this doc*; minimization happens at authoring time, not retroactively |
| **Pseudonymization** | Codename scheme at L2+; `EMP-NNN` / `CAND-NNN` for individuals; CODENAMES.yml separates mapping from content |
| **Data protection by default** | Domain baselines default to the more restrictive setting; override-down requires explicit reason; tier derivation is conservative |
| **Storage limitation** | Tier-based retention policy; archive workflow; purge candidates surface in annual audit |

### Article 17 — Right to erasure

| GDPR Art. 17 requirement | EKA implementation |
|--------------------------|--------------------|
| **Erasure request handling** | `data_subjects:` frontmatter makes erasure a query, not a grep; agent finds all references in <1 minute ([sec-erasure](#sec-erasure)) |
| **Documented response** | Audit log records each erasure with timestamp, request reference, files affected, redaction format |
| **Without undue delay** | Workflow targets fulfillment within 30 days; tombstone replacement is fast (single PR per repo) |
| **Onward erasure** | Cross-tier references in `related:` field allow checking that erased subject's content does not persist via reference |

### CCPA / CPRA

Most CCPA / CPRA controls overlap with GDPR. The specific California
addition — "Do Not Sell or Share" — does not directly affect EKA
docs (docs are not "sold"), but the right to delete maps to the same
Art. 17 workflow.

(sec-zero-trust-mapping)=
## NIST SP 800-207 Zero Trust mapping

NIST 800-207 defines a continuum from untrusted to fully-trusted.
EKA's tiers (already covered in [chapter 3](#chap-tier-architecture)):

| Zero Trust trust level | EKA tier | Authentication added |
|------------------------|----------|----------------------|
| Untrusted | L0 | None |
| Authenticated | L1 | SSO |
| Authenticated + authorized | L2 | RBAC + need-to-know |
| Authenticated + authorized + verified context | L3 | MFA + per-file ACL + (sometimes) JIT |
| Out of scope of docs | L4 | Production system controls |

Two NIST 800-207 design tenets are particularly important:

- **Tenet 5: "All resource authentication and authorization are
  dynamic and strictly enforced before access is allowed."** EKA's
  per-tier agent topology with separate MCP auth realms satisfies
  this: an L1 agent's authentication doesn't grant L2 access ever,
  regardless of context.
- **Tenet 7: "The enterprise collects as much information as
  possible about the current state of assets, network
  infrastructure, and communications and uses it to improve its
  security posture."** EKA's audit log per tier, plus quarterly /
  annual reviews, satisfies the data-collection part. Posture
  improvement is downstream of these reviews.

(sec-audit-evidence)=
## Evidence package for an audit

When an auditor or customer asks "show me your data classification
and access control evidence," the EKA-using org assembles:

| Evidence item | Where to find |
|----------------|---------------|
| The classification scheme | This spec + each repo's CLASSIFICATION.yml |
| The labeling scheme | Frontmatter schema ([chapter 5](#chap-metadata-and-labeling)) + sample documents |
| Access control matrix | GitHub team membership exports + Drive folder ACL reports |
| Enforcement controls | Pre-commit hook configuration + sample failed-commit log |
| Audit logs | Per-tier audit log files (sampled with PII redaction if necessary) |
| Retention policy | CLASSIFICATION.yml per repo + this chapter's retention table |
| Erasure workflow | [Chapter 6 §erasure](#sec-erasure) + audit-log entries showing past erasures |
| Annual classification audit | The most recent audit report |
| Risk register | The threat model docs in L2 `org-company-docs/security/threat-models/` |
| Agent guardrails | Per-tier CLAUDE.md files + smoke-test results |

A reference "compliance evidence" markdown template (a single doc
that aggregates pointers to all of the above) ships with the EKA
reference implementation.

## What's not in scope

EKA implements controls **at the documentation layer**. The
following standard-mandated controls live elsewhere in the org:

- **Physical security** (NIST PE family) — not docs
- **Contingency planning** (NIST CP family) — operational
- **Incident response** (NIST IR family) — operational; EKA hosts
  the runbooks but doesn't implement IR
- **System and services acquisition** (NIST SA family) — procurement
- **Awareness and training** (NIST AT family) — HR / training programs;
  EKA can host training materials but doesn't deliver training

These are referenced in EKA-hosted operational docs but their
implementation is outside the spec.

## What's contestable

- **Mapping to NIST 800-53 vs. NIST 800-171** depends on the
  org's regulatory context. NIST 800-171 is a subset for
  Controlled Unclassified Information (CUI) handling, relevant for
  Defense Industrial Base contractors. The 800-53 mapping above is
  the superset; 800-171 mapping is a refinement.
- **GDPR coverage assumes EU customer or EU-resident data.** Orgs
  with no EU exposure may skip Article 25/17 implementations
  (though EKA's design is unchanged either way; the controls just
  go unused).
- **CIS staging vs. NIST staging.** EKA recommends CIS Control 3
  staging because it's actionable. NIST 800-53 itself has no
  staging guidance; the choice of what to implement first is the
  user's. CIS is just one defensible staging.

[The tooling stack chapter](#chap-tooling) covers what software you
need to operate EKA day-to-day.
