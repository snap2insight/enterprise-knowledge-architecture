# EKA Glossary

Terms used throughout the spec, defined.

| Term | Definition |
|------|------------|
| **Access tier (L0-L4)** | EKA's five-level access classification: L0 Public, L1 Internal, L2 Confidential, L3 Restricted, L4 Live secrets (out of docs scope) |
| **Agent home** | A working directory holding a tier-scoped agent's `CLAUDE.md`, MCP config, and audit log. Different tiers have different homes |
| **Audit log** | Append-only record of every agent (and ideally human) read/write action against EKA stores. Retained per tier |
| **CIA triad** | Confidentiality, Integrity, Availability — the three security objectives per FIPS 199 |
| **Classification** | A document's `{C, I, A}` impact tuple per FIPS 199, recorded in frontmatter |
| **CLASSIFICATION.yml** | Per-repo configuration file declaring `max_tier`, baselines, hook configuration, retention. Schema: [`schemas/classification-yml.schema.json`](../schemas/classification-yml.schema.json) |
| **Codename** | Stable alphanumeric code (e.g., `C001`) substituted for an externally-confidential entity name in L2+ file paths and structural references |
| **CODENAMES.yml** | L2-classified file mapping codenames to real entity names + mnemonic display names. Schema: [`schemas/codenames-yml.schema.json`](../schemas/codenames-yml.schema.json) |
| **Conformance level** | A claim about which EKA requirements the deployment meets: L1 structural, L2 operational, L3 fully-tiered. See [`conformance.md`](../conformance.md) |
| **Data subject** | An identifiable individual (employee, candidate, board member, customer-side person). Documents mentioning data subjects use `EMP-NNN` / `CAND-NNN` codes |
| **Domain** | One of EKA's six data domains: Public, Customer, People, Business, Product, Operational. Determines baseline classification |
| **Erasure** | Removing or tombstoning a data subject's identifiable content per GDPR Article 17. See the [erasure runbook](../operations/erasure.runbook.md) |
| **FIPS 199** | NIST standard defining the CIA triad classification format. EKA uses its `{(C, impact), (I, impact), (A, impact)}` notation directly |
| **Frontmatter** | YAML metadata block at the top of every markdown file. Schema: [`schemas/frontmatter.schema.json`](../schemas/frontmatter.schema.json) |
| **Graduated staleness** | EKA's escalation pattern for review-overdue docs: yellow flag (30d) → red flag + archive (90d) → purge candidate (365d) |
| **Hook** | A pre-commit script enforcing one EKA rule (e.g., codename discipline, tier consistency). See [`hooks/`](../hooks/) |
| **JIT (Just-In-Time)** | Time-bounded access elevation for sensitive L3 sub-tiers — granted on request, expires automatically |
| **Manifest** | `_meta/manifest.md` — the agent-readable index of what's in a repo and cross-references to other stores. See [`templates/repo-skeleton/_meta/manifest.template.md`](../templates/repo-skeleton/_meta/manifest.template.md) |
| **MCP** | Model Context Protocol — the standard interface between agent runtimes and external services. EKA agents use MCPs with tier-scoped auth realms |
| **Mnemonic** | Human-readable display name (e.g., "Vesta") for an entity, used in body text alongside the structural codename |
| **NIST 800-53** | US federal control catalog. EKA maps to ~25 controls; see [`primer/08-compliance-mapping.md`](../../primer/08-compliance-mapping.md) |
| **NIST 800-207** | Zero Trust Architecture standard. EKA's tiers map directly to ZTA trust levels |
| **Override reason** | A required explanation when a document's classification differs from its domain baseline. Only DOWNWARD overrides are allowed |
| **Promotion / Demotion** | Moving content between tiers. Promotion is safe (pre-commit blocks); demotion requires a two-reviewer PR to prevent leak |
| **Skill** | A markdown file describing an agent-runnable workflow (e.g., bootstrap, classify, audit). See [`skills/`](../skills/) |
| **Tier** | Derived from `derive_tier(classification, data_subjects)`. Determines storage location, ACL, agent scope |
| **Tombstone** | Placeholder text replacing erased content, with reference to the audit-log entry that explains why |
| **URI scheme** | EKA's vocabulary for cross-tier references: `repo:`, `drive:`, `plane:`, `link:`, `secret:`. See [`reference/uri-schemes.md`](uri-schemes.md) |
| **Zero Trust** | Access architecture in which every read/write is authenticated, authorized, and verified — never trusted by network position alone. Source: NIST SP 800-207 |
