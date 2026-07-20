#!/bin/bash
# Run script for Linux

set -e

DESKTOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$DESKTOP_DIR/venv"

echo "Starting YourFreeDownloader..."

# Create virtual environment if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install/update dependencies
pip install --upgrade pip > /dev/null 2>&1
pip install -r "$DESKTOP_DIR/requirements.txt" > /dev/null 2>&1

# Install shared library
pip install -e "$(dirname "$DESKTOP_DIR")/shared" > /dev/null 2>&1

# Check for tkinter
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "Error: tkinter not installed. Install python3-tk (Debian/Ubuntu) or tk (Arch/Fedora)"
    exit 1
fi

# Run application
cd "$DESKTOP_DIR"
python -m ytdlp_desktop