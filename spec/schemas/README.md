# EKA Schemas

JSON Schema definitions for every machine-readable file in EKA.
These files **live in the repo** but are NOT rendered as site pages
— they're consumed by validators, tools, and agents.

## Files

| Schema | Validates | View source |
|--------|-----------|-------------|
| `frontmatter.schema.json` | The YAML frontmatter of every `.md` file | [source](frontmatter.schema.json) |
| `classification-yml.schema.json` | The root-level `CLASSIFICATION.yml` of every EKA repo | [source](classification-yml.schema.json) |
| `codenames-yml.schema.json` | The `CODENAMES.yml` file at the root of L2+ repos | [source](codenames-yml.schema.json) |
| `manifest.schema.json` | The frontmatter of `_meta/manifest.md` (extends the frontmatter schema with manifest-specific requirements) | [source](manifest.schema.json) |

## Schema versioning

Every machine-readable file declares the schema version it
conforms to:

```yaml
schema: eka.v1
```

Or for the codenames file:

```yaml
schema: eka.v1.codenames
```

Breaking changes increment to `eka.v2`. Schema files declare
their own version in the `$id` URL.

## Using these schemas

### From Python

```python
import json
import yaml
import jsonschema

# Load the schema
with open("spec/schemas/frontmatter.schema.json") as f:
    schema = json.load(f)

# Load a frontmatter block
with open("path/to/doc.md") as f:
    content = f.read()
fm = yaml.safe_load(content.split("---")[1])

# Validate
jsonschema.validate(fm, schema)
```

### From a pre-commit hook

The reference Python hooks in [`../hooks/`](../hooks/) use this
pattern. Alternative-language implementations should match the
behavior.

### From CI

A GitHub Action that lints frontmatter on every PR runs
`eka validate .` which invokes all schemas. See
[`../ci/`](../ci/).

## Conventions

- All schemas use **JSON Schema draft 2020-12**.
- Property names are `snake_case`.
- Enums are `UPPERCASE` for severity-like values (`LOW`, `MODERATE`,
  `HIGH`) and `lowercase` for type-like values (`public`,
  `customer`, etc.).
- Dates are ISO 8601 (`YYYY-MM-DD`).
- Cadence durations match `^\d+[dwmy]$` (e.g., `90d`, `6m`, `1y`).
