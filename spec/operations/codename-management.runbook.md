# Runbook: Codename Management

**When to run:** New customer / partner / competitor enters scope; existing entity changes disclosure status; codename theme exhausted.
**Who runs it:** L2 repo owners + relationship owners.
**Duration:** 5–10 minutes per entity.

## Pre-conditions

- [ ] CODENAMES.yml exists in the L2 repo
- [ ] The org has a documented codename theme (Roman gods, etc.)
- [ ] Operator has L2 repo write access

## Procedure: Add a new codename

### 1. Identify the next code

```bash
# Find the highest existing code in the relevant class
grep -oE '^  C[0-9]+:' CODENAMES.yml | sort -V | tail -1
# Next code is highest + 1
```

### 2. Pick a mnemonic from the theme

Constraints:
- Single capitalized word
- Not already used (any class)
- Avoids real-world political / current-celebrity figures
- Pronounceable in the org's working language(s)

### 3. Add the entry

```yaml
customers:
  C00N:
    name: "Real Entity Name"             # or "{Confidential Customer N}" if not yet public
    mnemonic: "Mnemonic"
    disclosure: confidential              # or acknowledged-public
    since: 2026-Q2
    primary_owner: {owner-email}
    notes: "Brief context."
```

### 4. Commit on a branch and PR

```bash
git checkout -b codename/add-{code}
git add CODENAMES.yml
git commit -m "Add codename {code} ({mnemonic}) for {confidential/named} entity"
gh pr create --title "Add codename {code}" --body "See CODENAMES.yml diff."
```

Reviewer: any L2 repo owner; merge after sanity-check.

## Procedure: Change disclosure status

When a confidential entity goes public (e.g., a customer issues a
press release):

1. Update `disclosure: acknowledged-public` in CODENAMES.yml
2. Add to `notes:` the public-disclosure date and reference
3. **DO NOT** rename files or paths — the codename stays for
   consistency. The body text MAY now use real names at L1 if
   appropriate.

## Procedure: Mark an entity historical

When a relationship ends:

1. Update `disclosure: historical`
2. Add `until: YYYY-QN` field
3. The code is NOT reused for a different entity. Codename
   stability is critical for audit history.

## Verification

```bash
eka validate --schema codenames CODENAMES.yml
eka codename audit --check-references .   # ensures all codename_refs in repo resolve
```

## Anti-patterns

- ✗ Reusing a code after an entity becomes historical
- ✗ Picking a mnemonic from a different theme ("just this one time")
- ✗ Storing a confidential customer's real name in CODENAMES.yml
- ✗ Renaming an existing codename to a "better" name
