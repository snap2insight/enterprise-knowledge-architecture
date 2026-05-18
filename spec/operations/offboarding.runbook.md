# Runbook: Employee Offboarding

**When to run:** An employee leaves the org (voluntary or otherwise).
**Who runs it:** HR + Engineering manager + IT.
**Duration:** Day-of departure: 1 hour. 30-day cleanup: ~2 hours total.

## Pre-conditions

- [ ] Departure date confirmed
- [ ] HR has updated HRIS to "departing" status
- [ ] Engineering manager has identified content-ownership transfers

## Day of departure

### 1. Revoke access (Engineering / IT)

```bash
# Remove from all GitHub teams
for team in $(gh api orgs/{org}/members/{user}/teams --jq '.[].slug'); do
  gh api -X DELETE orgs/{org}/teams/$team/memberships/{user}
done

# Or remove user from org entirely
gh api -X DELETE orgs/{org}/memberships/{user}
```

Drive: HR-managed group memberships are removed via Workspace
admin console (or `gam` CLI).

MCP tokens: revoke any agent tokens issued to the departing employee.

### 2. Reassign content ownership

Find all docs the employee owned:

```bash
eka query --owner {departing-email}
```

For each, identify a new owner (manager or designate). Update
frontmatter via a bulk PR:

```bash
eka reassign-owner --from {departing-email} --to {new-owner-email} --dry-run
# review, then:
eka reassign-owner --from {departing-email} --to {new-owner-email}
```

### 3. Handle their 1:1 / feedback notes

Drive folder `people-confidential/1on1s/{employee-codename}/`:
- Manager retains read access (per existing ACL)
- Departing employee loses read access (via group removal)
- Folder is NOT moved or deleted; retention follows employment-data policy

## Within 30 days

### 4. Personal notes / drafts

The departing employee may have authored content in:
- Personal Drive folders (org-managed Drive: review for org-relevant content)
- Scratch repos or branches (org-owned: review)
- The L1 `_inbox/` or `digests/` areas

For each item with org value: migrate to the appropriate tier
with a new owner. Discard the rest per the retention policy.

### 5. Codename mapping updates

If the departing employee was `primary_owner` for any entity in
`CODENAMES.yml`, update to the new owner.

### 6. Documentation of any L2-grade knowledge

If the employee held important context not yet documented
(specialty expertise, customer-relationship history), schedule an
"exit knowledge transfer" interview before departure where
possible. Capture into L1 or L2 as appropriate.

## Within 90 days

### 7. Audit-log review

The departing employee's audit-log entries are retained per
standard policy (12+ months). No special action — just confirm
the policy is being applied.

## Verification

```bash
# Verify no current EKA repo lists the departed user as owner
eka audit --check-owners --departed {departing-email}

# Verify no current GitHub team membership
gh api users/{user}/orgs --jq '.[].login' | grep -c {org} # should be 0
```

## Recovery scenarios

### Recovery: departure happens before content reassignment

Content is orphaned (no owner). The repo's `_meta/ownership.yml`
gets an "(orphaned)" marker; the next person to touch the file
takes ownership. The owner field cannot remain pointing at the
departed account.

### Recovery: discover ungroomed content months later

The annual classification audit surfaces departed-employee
ownership as a finding. Reassign per the standard process; treat
as overdue, not as an incident.
