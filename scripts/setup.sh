#!/usr/bin/env bash
set -euo pipefail

echo "=========================================="
echo "  Setting up TINO Development Environment"
echo "=========================================="

# Check Python 3 version
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not found in PATH." >&2
    exit 1
fi

# Create virtual environment if not present
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
# shellcheck source=/dev/null
source .venv/bin/activate

# Upgrade pip and install package in editable mode with dev dependencies
echo "Installing TINO and development dependencies..."
pip install --upgrade pip
pip install -e ".[dev]"

echo ""
echo " Setup complete!"
echo "To activate your environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the game:"
echo "  tino"
echo ""
echo "To run tests:"
echo "  ./scripts/test.sh"
