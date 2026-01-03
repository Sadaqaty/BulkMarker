#!/bin/bash
# Comprehensive build script for Bulk Video Watermarker
# Handles fresh clones: creates venv, installs deps, builds executable

set -e  # Exit on any error

echo "=== Bulk Video Watermarker Build Script ==="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Warning: Failed to upgrade pip, continuing..."
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install requirements."
    exit 1
fi

# Check if FFmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg not found. Video processing may not work in the built executable."
    echo "Install FFmpeg: sudo apt install ffmpeg (Linux) or download from https://ffmpeg.org/"
fi

# Detect OS for PyInstaller data separator
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SEP=":"
    ICON=""
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SEP=":"
    ICON=""
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    SEP=";"
    ICON=""
else
    echo "Error: Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Building for $OSTYPE..."

# Clean previous build
if [ -d "build" ]; then
    rm -rf build
fi
if [ -d "dist" ]; then
    rm -rf dist
fi

# Build with PyInstaller
pyinstaller --onefile --windowed --name bulk-video-watermarker \
    --add-data "src${SEP}src" \
    --add-data "presets${SEP}presets" \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtWidgets \
    --hidden-import moviepy \
    --hidden-import moviepy.video.fx \
    --hidden-import moviepy.video.io.ffmpeg_reader \
    --hidden-import moviepy.video.io.ffmpeg_writer \
    main.py

if [ $? -ne 0 ]; then
    echo "Error: PyInstaller build failed."
    exit 1
fi

echo "=== Build Complete ==="
echo "Executable created: dist/bulk-video-watermarker"
echo "Run it with: ./dist/bulk-video-watermarker"
echo ""
echo "Note: Ensure FFmpeg is installed on the target system for video processing."