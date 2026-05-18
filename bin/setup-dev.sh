#!/usr/bin/env bash
# setup-dev.sh — populate _toolkit/ for local development.
#
# Two modes:
#
# 1) Symlink mode (preferred — shared local toolkit clone)
#    Set TOOLKIT_LOCAL to a path that already contains a clone of
#    myst-docs-toolkit. The script creates _toolkit/ as a symlink to it.
#    Use this when you have several docs sites checked out as siblings
#    of one toolkit clone.
#
#      TOOLKIT_LOCAL=../myst-docs-toolkit ./bin/setup-dev.sh
#
# 2) Clone mode (fallback — local clone inside this repo)
#    If TOOLKIT_LOCAL is unset, the script clones myst-docs-toolkit
#    into _toolkit/ as a real directory.
#
#      ./bin/setup-dev.sh
#
# Either way, after this runs you can `myst build --html`.
#
# `_toolkit/` is gitignored — never committed, regardless of mode.

set -euo pipefail

TOOLKIT_URL="${TOOLKIT_URL:-}"
TOOLKIT_REF="${TOOLKIT_REF:-main}"
TOOLKIT_LOCAL="${TOOLKIT_LOCAL:-}"

# Wipe any existing _toolkit/ — could be a stale symlink or an old clone.
rm -rf _toolkit

if [ -n "$TOOLKIT_LOCAL" ]; then
  if [ ! -d "$TOOLKIT_LOCAL" ]; then
    echo "❌ TOOLKIT_LOCAL=$TOOLKIT_LOCAL does not exist." >&2
    exit 1
  fi
  # Convert to absolute for a stable symlink target.
  TOOLKIT_LOCAL_ABS=$(cd "$TOOLKIT_LOCAL" && pwd)
  ln -s "$TOOLKIT_LOCAL_ABS" _toolkit
  echo "✅ Linked _toolkit → $TOOLKIT_LOCAL_ABS"
elif [ -n "$TOOLKIT_URL" ]; then
  echo "Cloning toolkit ($TOOLKIT_REF) from $TOOLKIT_URL ..."
  git clone --depth 1 --branch "$TOOLKIT_REF" --recurse-submodules "$TOOLKIT_URL" _toolkit >/dev/null 2>&1
  echo "✅ Cloned _toolkit/"
else
  cat >&2 <<'EOF'
❌ Neither TOOLKIT_LOCAL nor TOOLKIT_URL is set.

Set one of them:

  # If you have a local clone of myst-docs-toolkit as a sibling:
  TOOLKIT_LOCAL=../myst-docs-toolkit ./bin/setup-dev.sh

  # Or fetch from a remote:
  TOOLKIT_URL=https://github.com/<org>/myst-docs-toolkit.git ./bin/setup-dev.sh

See README.md "Local development" section for details.
EOF
  exit 1
fi

echo ""
echo "Next: myst build --html"
