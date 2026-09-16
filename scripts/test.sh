#!/usr/bin/env bash
set -euo pipefail

echo "Running test suite..."

# Ensure src is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH:-}:src"

if command -v pytest &> /dev/null; then
    pytest -v "$@"
elif [ -f ".venv/bin/pytest" ]; then
    .venv/bin/pytest -v "$@"
else
    echo "Note: pytest not detected in environment. Running standard unittest discover..."
    python3 -m unittest discover -s tests -v
fi
