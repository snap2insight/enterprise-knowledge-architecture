# docs automation.
#
# Same recipes run locally and in CI. Run `just` (no args) to list them.
# Install just: https://github.com/casey/just#installation
# Install uv:   https://docs.astral.sh/uv/getting-started/installation/

# ── Vars ──────────────────────────────────────────────────────────────────
root          := justfile_directory()
venv          := root + "/.venv"
venv_bin      := venv + "/bin"
python        := venv_bin + "/python"
requirements  := root + "/requirements.txt"

# ── Default ───────────────────────────────────────────────────────────────

# Show the available recipes.
default:
    @just --list --unsorted

# ── Setup ─────────────────────────────────────────────────────────────────

# Bootstrap: Python venv (uv) + npm-global mystmd. Run once after clone.
setup: venv python-deps node-deps
    @echo ""
    @echo "✅ Setup complete. Try: just docs-dev"

# Create a uv-managed Python virtualenv at .venv/. Idempotent — no-op if
# the venv already exists (multiple recipes may declare this as a prereq
# within the same `just` invocation).
venv:
    @command -v uv >/dev/null || { echo "❌ Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
    @test -d {{venv}} || uv venv {{venv}}

# Install Python dependencies from requirements.txt into the venv.
python-deps: venv
    uv pip install --python {{python}} -r {{requirements}}

# Install mystmd globally via npm. Idempotent.
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

# Static-serve the built docs at :8000 — matches what GH Pages will serve.
# (`myst start` is a dev-server with different routing; use this for
# debugging "works locally / 404s in prod" cases.)
docs-preview: docs
    @echo "Serving _build/html at http://localhost:8000 — Ctrl+C to stop"
    cd _build/html && python3 -m http.server 8000

# Wipe docs build output.
docs-clean:
    rm -rf _build

# Update last-updated dates in frontmatter from git history.
# Run before `just docs` to refresh `{{ date }}` substitutions.
update-dates: python-deps
    {{python}} bin/update-dates.py

# ── CI entrypoints ────────────────────────────────────────────────────────

# Single recipe invoked by .github/workflows/docs.yml.
ci-docs: update-dates docs
