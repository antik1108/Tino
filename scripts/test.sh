#!/usr/bin/env bash
set -euo pipefail

echo "Running pytest test suite..."

if command -v pytest &> /dev/null; then
    pytest -v "$@"
else
    if [ -f ".venv/bin/pytest" ]; then
        .venv/bin/pytest -v "$@"
    else
        echo "pytest not found in PATH or .venv. Falling back to python3 -m unittest..."
        python3 -m unittest discover -s tests -v
    fi
fi
