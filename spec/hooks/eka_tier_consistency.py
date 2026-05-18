#!/usr/bin/env python3
"""eka-tier-consistency hook.

Validates that every markdown file's `tier` field equals the value
derived from `classification` + `data_subjects`. Inconsistency
indicates an author tried to over- or under-classify by hand,
which the hook prevents.

This is the reference implementation. The derive_tier() function
here is the canonical authority — alternative-language hook
implementations MUST produce identical output for the same input.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml  # pip install pyyaml


# ----------------------------- Core logic --------------------------------

VALID_IMPACTS = {"LOW", "MODERATE", "HIGH"}


def derive_tier(classification: dict, data_subjects: list) -> str:
    """Compute the tier from classification + data_subjects per EKA v1.

    Authoritative rule. Any other tool computing tier must produce
    identical output for the same input.
    """
    c = classification.get("C")
    i = classification.get("I")
    a = classification.get("A")

    if c not in VALID_IMPACTS or i not in VALID_IMPACTS or a not in VALID_IMPACTS:
        raise ValueError(
            f"Classification impact must be one of {VALID_IMPACTS}; got C={c} I={i} A={a}"
        )

    # L3: any document with identifiable individuals
    if data_subjects:
        return "L3"

    # L2: HIGH confidentiality
    if c == "HIGH":
        return "L2"

    # L1: MODERATE confidentiality, or HIGH integrity/availability
    if c == "MODERATE" or i == "HIGH" or a == "HIGH":
        return "L1"

    # L0: everything else
    return "L0"


# --------------------------- Frontmatter parser ---------------------------


def parse_frontmatter(path: Path) -> tuple[dict | None, str | None]:
    """Returns (frontmatter, error_message). One of them is None.

    Frontmatter is a dict if successfully parsed; None otherwise.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "no YAML frontmatter (file does not start with '---')"

    end_marker = text.find("\n---\n", 4)
    if end_marker < 0:
        return None, "frontmatter not terminated with closing '---'"

    fm_text = text[4:end_marker]
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        return None, f"frontmatter is not valid YAML: {e}"

    if not isinstance(fm, dict):
        return None, "frontmatter must be a YAML mapping"

    return fm, None


# ------------------------------- Error reporter ---------------------------


def report_error(path: Path, line: int | None, message: str, fix: str | None = None) -> None:
    """Emit a hook error in the EKA standard format."""
    loc = f"{path}:{line if line is not None else '-'}"
    sys.stderr.write(f"{loc}: eka-tier-consistency: {message}\n")
    if fix:
        sys.stderr.write(f"  └── Fix: {fix}\n")


# --------------------------------- Main -----------------------------------


def check_file(path: Path) -> bool:
    """Returns True if the file passes the hook; False otherwise.

    Reads from frontmatter.options.eka.* (EKA v1 namespace).
    Falls back to top-level keys for documents that haven't yet been
    migrated to the namespaced format (transitional support).
    """
    fm, err = parse_frontmatter(path)
    if err is not None:
        report_error(path, None, err)
        return False

    # We don't enforce frontmatter presence here — eka-frontmatter-required
    # is the hook for that. Tier-consistency only checks if the relevant
    # fields are present and consistent.

    # New namespaced location (EKA v1 standard).
    eka = (fm.get("options") or {}).get("eka") or {}

    # Transitional fallback: pre-migration files have keys at top level.
    classification = eka.get("classification", fm.get("classification"))
    data_subjects = eka.get("data_subjects", fm.get("data_subjects", []))
    declared_tier = eka.get("tier", fm.get("tier"))

    if not isinstance(classification, dict):
        report_error(
            path, None,
            "frontmatter missing 'classification' block",
            "Add `classification: { C: ..., I: ..., A: ... }`. See spec/schemas/frontmatter.schema.json"
        )
        return False

    if not isinstance(data_subjects, list):
        report_error(
            path, None,
            "frontmatter `data_subjects` must be a list",
            "Set `data_subjects: []` if no individuals are mentioned."
        )
        return False

    if not declared_tier:
        report_error(
            path, None,
            "frontmatter missing 'tier'",
            "Add the derived tier (see derive_tier rule)."
        )
        return False

    try:
        expected_tier = derive_tier(classification, data_subjects)
    except ValueError as e:
        report_error(path, None, str(e))
        return False

    if declared_tier != expected_tier:
        report_error(
            path, None,
            f"declared tier '{declared_tier}' does not match derived tier '{expected_tier}'",
            f"Set `tier: {expected_tier}` in frontmatter. The derivation rule is fixed; "
            "if you intend a different tier, change the classification or data_subjects."
        )
        return False

    return True


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        sys.stderr.write("Usage: eka_tier_consistency.py <file> [<file> ...]\n")
        return 2

    all_ok = True
    for arg in argv[1:]:
        path = Path(arg)
        if not path.is_file():
            sys.stderr.write(f"{path}: not a file (skipped)\n")
            continue
        if path.suffix.lower() != ".md":
            # Non-markdown files don't need EKA frontmatter
            continue
        if not check_file(path):
            all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
