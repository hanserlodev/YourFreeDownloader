#!/bin/bash
# Build script for Linux

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DESKTOP_DIR="$PROJECT_ROOT/desktop-multiplatform"
BUILD_DIR="$DESKTOP_DIR/build"
DIST_DIR="$DESKTOP_DIR/dist"

echo "Building YourFreeDownloader for Linux..."

# Clean previous builds
rm -rf "$BUILD_DIR" "$DIST_DIR"

# Create virtual environment if not exists
if [ ! -d "$DESKTOP_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$DESKTOP_DIR/venv"
fi

# Activate venv and install dependencies
source "$DESKTOP_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r "$DESKTOP_DIR/requirements.txt"
pip install pyinstaller

# Install shared library in development mode
pip install -e "$PROJECT_ROOT/shared"

# Run PyInstaller
cd "$DESKTOP_DIR"
pyinstaller \
    --name "YourFreeDownloader" \
    --onefile \
    --windowed \
    --add-data "$PROJECT_ROOT/shared/ytdlp_core:ytdlp_core" \
    --collect-all ytdlp_core \
    --collect-all yt_dlp \
    --collect-all customtkinter \
    --collect-all dependency_injector \
    --hidden-import ytdlp_core \
    --hidden-import ytdlp_core.core \
    --hidden-import ytdlp_core.domain \
    --hidden-import ytdlp_core.application \
    --hidden-import ytdlp_core.infrastructure \
    --hidden-import yt_dlp \
    --hidden-import customtkinter \
    --hidden-import dependency_injector \
    src/ytdlp_desktop/__main__.py

echo "Build complete! Executable at: $DIST_DIR/YourFreeDownloader"