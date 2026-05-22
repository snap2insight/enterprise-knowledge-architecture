# docs automation.
#
# Same recipes run locally and in CI. Run `just` (no args) to list them.

# ── Default ───────────────────────────────────────────────────────────────

# Show the available recipes.
default:
    @just --list --unsorted

# ── Setup ─────────────────────────────────────────────────────────────────

# Bootstrap: Python deps + npm-global mystmd. Run once after clone.
setup: python-deps node-deps
    @echo ""
    @echo "✅ Setup complete. Try: just docs-dev"

# Install Python dependencies.
python-deps:
    pip install pyyaml jsonschema

# Install mystmd globally via npm.
node-deps:
    @command -v myst >/dev/null || npm install -g mystmd

# ── Docs ──────────────────────────────────────────────────────────────────

# Build the docs site. Reads BASE_URL env (defaults to empty).
docs:
    BASE_URL="${BASE_URL:-}" myst build --html
    @echo "✅ Built _build/html/"

# Live dev server for the docs site (hot reload).
docs-dev:
    myst start

# Static-serve the built docs at :8000.
docs-preview: docs
    @echo "Serving _build/html at http://localhost:8000 — Ctrl+C to stop"
    cd _build/html && python3 -m http.server 8000

# Wipe docs build output.
docs-clean:
    rm -rf _build

# Update last-updated dates in frontmatter from git history.
# Run before `just docs` to refresh `{{ date }}` substitutions.
update-dates: python-deps
    python bin/update-dates.py

# ── CI entrypoints ────────────────────────────────────────────────────────

ci-docs: update-dates docs
