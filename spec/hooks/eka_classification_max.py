#!/usr/bin/env python3
"""eka-classification-max hook.

Contract: see spec/hooks/README.md for the validation this hook performs.

This file is a stub. The complete reference implementation will ship
alongside the eka-helpers package; until then, implement per the contract
in spec/hooks/README.md, sharing helpers (parse_frontmatter, report_error)
with eka_tier_consistency.py.
"""

import sys


def main() -> int:
    sys.stderr.write(
        "eka-classification-max: reference implementation pending.\n"
        "See spec/hooks/README.md for the contract.\n"
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
