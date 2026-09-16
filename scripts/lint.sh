#!/usr/bin/env bash
set -euo pipefail

echo "Running Ruff linter and formatter checks..."

if command -v ruff &> /dev/null; then
    ruff check .
    ruff format --check .
else
    echo "Ruff not found in current PATH. Checking in .venv..."
    if [ -f ".venv/bin/ruff" ]; then
        .venv/bin/ruff check .
        .venv/bin/ruff format --check .
    else
        echo "Error: ruff is not installed. Run './scripts/setup.sh' first." >&2
        exit 1
    fi
fi

echo " Lint checks passed successfully!"
