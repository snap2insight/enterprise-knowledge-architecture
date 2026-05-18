# Runbook: GDPR Article 17 Erasure

**When to run:** A verified erasure request received from a data subject.
**Who runs it:** Privacy admin (with L2 + L3 read access).
**Duration:** 2–4 hours per request (including human-judgment steps).
**Companion skill:** [`eka-erasure`](../skills/eka-erasure.skill.md) — automates the mechanical portions.

## Pre-conditions

- [ ] Request is **verified** — the subject's identity is confirmed
      per the org's privacy-request authentication procedure
- [ ] Request is **timely** — within the regulator's 30-day fulfillment window
- [ ] No active **legal hold** prevents erasure
- [ ] Subject ID is identified in EKA's coding system (`EMP-NNN`,
      `CAND-NNN`, etc.)

## Procedure

### 1. Open request record

Create a new file in the L2 repo's audit-log folder:

```
{L2-repo}/audit/erasure-requests/{date}-{request-ref}.md
```

Use the runbook's request-record template
(`spec/templates/content-types/runbook.template.md` is the closest
template; add the erasure-specific fields).

### 2. Invoke the eka-erasure skill (mechanical discovery)

```bash
eka skill invoke eka-erasure \
  --subject-id {SUBJECT-ID} \
  --request-reference {REQUEST-REF} \
  --request-date {YYYY-MM-DD} \
  --requester-role "Privacy admin: {email}" \
  --dry-run true
```

The skill produces a candidate redaction list across all
accessible stores (Git + Drive). Review the list.

### 3. Identify retention exceptions

For each candidate, determine whether erasure is blocked:

| Exception | Action |
|-----------|--------|
| Active legal hold | Block; document the hold reference |
| Tax / accounting regulatory retention | Block; document the regulation + retention period |
| Customer-contractual retention | Block; document the contract clause + expiry |
| None | Approve for erasure |

Record decisions per item.

### 4. Approve erasure batch

Confirm the candidate list (minus exceptions) for processing.
Re-invoke the skill with `--dry-run false` and the explicit
approval list.

The skill applies redactions across Git (as PRs) and Drive
(direct edits with audit-log entries).

### 5. Human review of PRs

Each per-repo PR is reviewed by:
- Privacy admin (final approver)
- Repo owner (for sanity check)

PRs land within the 30-day window.

### 6. Notify the subject

Use the org's privacy-response template. Include:
- Confirmation of erasure
- Description of any retention exceptions (per regulation, the
  subject is entitled to know what was retained and why)
- Contact for follow-up

### 7. File the closing record

Append to the request record (step 1):

```markdown
## Closing record

- Erasure completed: {date}
- PRs: {list of PR URLs}
- Drive edits: {summary}
- Retention exceptions: {list with reasons}
- Subject notified: {date}, via {channel}
- Privacy admin sign-off: {name}, {date}
```

Commit and mark `status: approved`.

## Verification

After completion:

- [ ] No documents in scope retain references to the subject
      (except in retained-exception items, which have explicit
      tombstones / preservation notes)
- [ ] Audit-log entry committed
- [ ] Subject notified within 30 days of request
- [ ] Closing record is filed and approved

## Rollback

GDPR-mandated erasure is generally not rollback-able. If the
agent or operator accidentally redacted content that should have
been retained (e.g., a contractual-retention exception missed):

1. Restore the affected content from Git history (`git revert` on
   the redaction PR) or from Drive version history
2. Document the recovery in the request record's closing log
3. Re-file the request with corrected exception handling

## Recovery scenarios

### Recovery: subject identity cannot be verified

Refuse the request per the org's authentication policy. Document
the refusal reason; respond to the subject with the verification
procedure they should follow.

### Recovery: agent reports broader access than expected

If the agent's Drive scan reveals access to subject files in
folders the privacy admin didn't expect: STOP, investigate the
ACL misconfiguration, then resume erasure once the broader ACL
issue is resolved.

### Recovery: production system also holds subject data

Out of EKA scope. Coordinate with the data-team's
customer-offboarding playbook (production database, data lake,
cache layers).
