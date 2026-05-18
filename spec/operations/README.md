# EKA Operations Runbooks

Human-runnable procedures for ongoing operation of an
EKA-conformant deployment. Each runbook describes WHO runs it,
WHEN, and the step-by-step procedure.

## Runbook catalog

| Runbook | Cadence | Who runs it |
|---------|---------|-------------|
| [ACL automation](acl-automation.runbook.md) | One-time setup + ongoing automation | Platform + HR/IT integration owner |
| [Access review](access-review.runbook.md) | Quarterly (or verification-only when automation is in place) | Repo / Drive admin |
| [Erasure (GDPR Art. 17)](erasure.runbook.md) | Per-request | Privacy admin |
| [Offboarding](offboarding.runbook.md) | Per departure (synchronous; automation if available) | HR + Engineering lead |
| [Codename management](codename-management.runbook.md) | Ongoing | L2 repo owners |
| [Annual classification audit](annual-audit.runbook.md) | Yearly | Compliance lead |

## Runbook structure

Every EKA runbook follows the structure in
[`spec/templates/content-types/runbook.template.md`](../templates/content-types/runbook.template.md):

- **When to run** — trigger conditions
- **Pre-conditions** — checklist before starting
- **Procedure** — numbered steps with commands
- **Verification** — how to confirm success
- **Rollback** — how to undo (where applicable)
- **Recovery scenarios** — what to do when specific steps fail

## Automation

Several runbooks have agent skill counterparts that automate most
of the procedure:

| Runbook | Skill | Manual portion |
|---------|-------|----------------|
| Erasure | [`eka-erasure`](../skills/eka-erasure.skill.md) | Identity verification, retention exceptions, subject notification |
| Audit | [`eka-classification-audit`](../skills/eka-classification-audit.skill.md) | Final review and sign-off |
| Stale-doc cleanup | [`eka-audit-stale`](../skills/eka-audit-stale.skill.md) | Purge-candidate decisions |

The skills handle the mechanical steps; runbooks include the
human-judgment steps.
