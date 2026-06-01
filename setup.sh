#!/bin/bash

set -e

echo "==================================="
echo "Setting up project..."
echo "==================================="

echo ""
echo "Creating virtual environment..."

python3 -m venv .venv

echo ""
echo "Upgrading pip..."

.venv/bin/pip install --upgrade pip

echo ""
echo "Installing dependencies..."

.venv/bin/pip install -r requirements.txt

echo ""
echo "Installing project in editable mode..."

.venv/bin/pip install -e .

echo ""
echo "==================================="
echo "Setup completed successfully."
echo "==================================="

echo ""
echo "Activate the virtual environment with:"
echo "source .venv/bin/activate"