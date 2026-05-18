#!/usr/bin/env python3
"""eka-frontmatter-required hook.

Every .md file MUST start with YAML frontmatter conforming to
spec/schemas/frontmatter.schema.json (modulo paths excluded via
CLASSIFICATION.yml::exclude_paths).

This file is a contract specification; the reference implementation
shares helpers with eka_tier_consistency.py (parse_frontmatter,
report_error). Re-use the parser; add a jsonschema.validate() call.

Pseudocode:

    for path in args:
        if matches any exclude_paths glob: continue
        fm, err = parse_frontmatter(path)
        if err: report; fail
        try:
            jsonschema.validate(fm, frontmatter_schema)
        except ValidationError as e:
            report(path, message=e.message, fix=...)
            fail

A complete reference implementation will ship alongside the
eka-helpers package; this file documents the contract.
"""

import sys


def main() -> int:
    sys.stderr.write(
        "eka-frontmatter-required: reference implementation not yet in this checkout.\n"
        "Install eka-helpers package, or implement per the contract in the docstring.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
