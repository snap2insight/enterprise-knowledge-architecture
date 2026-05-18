# EKA URI Schemes

The `related:` frontmatter field accepts URIs from a fixed set of
schemes. The `eka-related-uris-valid` hook validates the syntax.
Agents interpret schemes per the rules below.

## Scheme catalog

| Scheme | Format | Resolves to | Agent behavior |
|--------|--------|-------------|-----------------|
| `repo:` | `repo:{repo-name}/{path/to/file.md}` | Another EKA Git repo's document | Follow if target tier ≤ agent tier; else report as out-of-scope |
| `drive:` | `drive:{drive-file-id}` | Google Drive file by ID | Follow if L3 agent has ACL; else "no access" |
| `drive-folder:` | `drive-folder:{folder-path-or-id}` | Drive folder | Same as `drive:` |
| `plane:` | `plane:{project-id}` or `plane:{project-id}/issue-{nnn}` | Plane ticket / project | L1+ agents may follow via Plane MCP (read-only) |
| `link:` | `link:https://...` | Arbitrary external URL | Probe for liveness only; don't fetch full content |
| `secret:` | `secret:{vault-path}` | Live secret in production vault | NEVER follow; reference only |

## Detailed semantics

### `repo:`

Format: `repo:{repo-name}/{path/to/file.md}`

The `{repo-name}` is the EKA-conformant repo's slug (matching the
`name:` in its `CLASSIFICATION.yml`). The path is repo-root-relative.

The agent resolves `repo-name` against the org's manifest. If the
named repo is at a higher tier than the agent, the reference is
preserved in output but the content is not fetched.

Example:
```yaml
related:
  - repo:acme-company-docs/security/threat-models/auth-detailed.md
```

### `drive:` and `drive-folder:`

Format: `drive:{file-id}` or `drive-folder:{folder-id-or-path}`

Drive file IDs are opaque strings. Use the folder-path form
(`drive-folder:acme-drive/people-confidential/perf-reviews/`) for
references whose stability is more important than direct
resolution (folder structures change less than file IDs).

L3 agents follow these via the Drive MCP, subject to per-file ACL.
L1/L2 agents see the reference but cannot follow.

### `plane:`

Format: `plane:{project-id}` or `plane:{project-id}/issue-{number}`

The project ID is the Plane workspace's project slug. Issue
numbers are project-scoped integers.

Examples:
```yaml
related:
  - plane:acme-platform                    # whole project
  - plane:acme-platform/issue-142          # specific issue
```

### `link:`

Format: `link:https://example.com/...`

For external URLs (vendor docs, OSS projects, blog posts). The
`link:` prefix distinguishes external references from internal
EKA references. Hooks check URL syntax but do not require
liveness.

### `secret:`

Format: `secret:{provider}/{path}` (provider-specific)

Examples:
```yaml
related:
  - secret:keyvault/acme-prod/jwt-signing-key
  - secret:vault/secret/data/customer-c001/api-key
```

**Agents NEVER follow `secret:` references.** The scheme exists
purely to record that a piece of content references a live secret,
so an auditor can trace from the doc to where the secret is
managed. The secret value itself never enters the docs system.

## Adding new schemes

If your org needs a new URI scheme (e.g., for a CRM, an
issue tracker other than Plane, etc.):

1. Add a registration to your repo's `CLASSIFICATION.yml`:

```yaml
extensions:
  uri_schemes:
    crm:
      pattern: "^crm:[A-Z0-9-]+$"
      agent_behavior: "follow via CRM MCP if L2+"
```

2. Implement the corresponding MCP scope (or document that
   following is manual).

3. The `eka-related-uris-valid` hook reads the extension list and
   accepts the new scheme.

Custom schemes are local to the org. Schemes that prove broadly
useful may be promoted into a future EKA spec version.
