# Runbook: Access Review

**When to run:** Quarterly (every 90 days).
**Who runs it:** Repo administrator (L1/L2) + Drive folder owners (L3).
**Duration:** 1–2 hours per tier per quarter.

## Pre-conditions

- [ ] All EKA-tier teams exist in GitHub org settings
- [ ] HRIS roster export is current (within 7 days)
- [ ] Previous quarter's review record is filed in
      `{L2-repo}/audit/access-reviews/{previous-quarter}.md`

## Procedure

### Per L2+ Git repo

1. Export current team membership:
   ```bash
   gh api orgs/{org}/teams/{team-name}/members --jq '.[] | .login' > /tmp/{team}-current.txt
   ```

2. Export HRIS active roster, filtered to relevant department:
   ```bash
   # Org-specific; via HRIS API or admin export
   ```

3. Diff the two:
   ```bash
   diff <(sort /tmp/{team}-current.txt) <(sort /tmp/hris-roster.txt)
   ```

4. For each diff:
   - **In team, not in HRIS active**: revoke (left the org or
     wrong-team membership)
   - **In team, role-changed in HRIS**: re-confirm or revoke per
     new role
   - **Not in team, in HRIS at relevant role**: ask owner whether
     to add

5. Apply revocations:
   ```bash
   for user in $(cat /tmp/to-revoke.txt); do
     gh api -X DELETE orgs/{org}/teams/{team}/memberships/$user
   done
   ```

6. Apply additions (requires owner approval, one at a time):
   ```bash
   gh api -X PUT orgs/{org}/teams/{team}/memberships/$user -f role=member
   ```

### Per L3 Drive folder

1. List current ACL via Workspace admin console (or `gam` CLI):
   ```bash
   gam show acls drivefile {folder-id}
   ```

2. Compare with intended ACL (documented in
   `{L2-repo}/operations/drive-acl-map.md`).

3. Reconcile additions / removals per the same process as above.

4. For sub-folders with JIT access patterns: confirm no stale
   grants persist (active grants from prior quarter should have
   been revoked at end of their stated window).

## Verification

After completion:

```bash
# Run the access-review skill (or eka cli)
eka access-review --report quarter={Q} > {L2-repo}/audit/access-reviews/{Q}.md
git -C {L2-repo} add audit/access-reviews/{Q}.md
git -C {L2-repo} commit -m "Q{N} access review {YYYY}"
```

The report frontmatter sets `next_review = today + 90d`. The next
quarter's reminder triggers on that date.

## Rollback

Revoking access then realizing the user needed it: re-add via the
addition step. There's no harm — audit log records both
revocation and re-addition with timestamps.

Granting access then realizing it shouldn't have been: revoke
immediately; document the brief grant in the next access review.

## Recovery scenarios

### Recovery: HRIS export unavailable

Manual reconciliation per known roster. Mark in the review record
that HRIS was unavailable; schedule a re-check within 30 days.

### Recovery: Team / group ACL inconsistent

Reset to the documented intended state in
`drive-acl-map.md` (or for Git: the team's documented
membership in the L2 repo's manifest). Investigate the divergence
separately.
