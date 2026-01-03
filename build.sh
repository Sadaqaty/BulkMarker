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
PYINSTALLER_CMD="pyinstaller --onefile --windowed --name bulk-video-watermarker \
    --add-data \"src${SEP}src\" \
    --add-data \"presets${SEP}presets\" \
    --collect-all moviepy \
    --collect-all imageio \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtWidgets \
    --hidden-import numpy \
    --hidden-import PIL \
    --hidden-import cv2 \
    --hidden-import tqdm \
    --hidden-import decorator \
    --hidden-import proglog \
    --hidden-import importlib.metadata"

# Add icon if available
if [ -f "assets/icon.png" ]; then
    PYINSTALLER_CMD="$PYINSTALLER_CMD --icon assets/icon.png"
    echo "Using icon: assets/icon.png"
else
    echo "Warning: assets/icon.png not found, building without icon"
fi

eval $PYINSTALLER_CMD main.py

if [ $? -ne 0 ]; then
    echo "Error: PyInstaller build failed."
    exit 1
fi

# For Linux, create AppImage if appimagetool is available
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f "./appimagetool" ]; then
        echo "Creating AppImage..."
        
        # Create AppDir structure
        APPDIR="AppDir"
        mkdir -p "$APPDIR/usr/bin"
        mkdir -p "$APPDIR/usr/share/applications"
        mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"
        
        # Copy executable
        cp "dist/bulk-video-watermarker" "$APPDIR/usr/bin/"
        
        # Copy icon if available
        if [ -f "assets/icon.png" ]; then
            cp "assets/icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/bulk-video-watermarker.png"
            cp "assets/icon.png" "$APPDIR/bulk-video-watermarker.png"
        fi
        
        # Create desktop file
        cat > "$APPDIR/usr/share/applications/bulk-video-watermarker.desktop" << EOF
[Desktop Entry]
Name=Bulk Video Watermarker
Exec=bulk-video-watermarker
Icon=bulk-video-watermarker
Type=Application
Categories=AudioVideo;Video;
EOF
        
        # Also copy desktop file to AppDir root for appimagetool
        cp "$APPDIR/usr/share/applications/bulk-video-watermarker.desktop" "$APPDIR/"
        
        # Create AppRun script
        cat > "$APPDIR/AppRun" << EOF
#!/bin/bash
HERE="\$(dirname "\$(readlink -f "\${0}")")"
export PATH="\$HERE/usr/bin:\$PATH"
export LD_LIBRARY_PATH="\$HERE/usr/lib:\$LD_LIBRARY_PATH"
exec "\$HERE/usr/bin/bulk-video-watermarker" "\$@"
EOF
        chmod +x "$APPDIR/AppRun"
        
        # Build AppImage
        ./appimagetool "$APPDIR" "dist/bulk-video-watermarker.AppImage"
        
        if [ $? -eq 0 ]; then
            echo "AppImage created: dist/bulk-video-watermarker.AppImage"
        else
            echo "Warning: AppImage creation failed"
        fi
        
        # Clean up
        rm -rf "$APPDIR"
    else
        echo "appimagetool not found in root directory, skipping AppImage creation."
    fi
fi

echo "=== Build Complete ==="
echo "Executable created: dist/bulk-video-watermarker"
if [[ "$OSTYPE" == "linux-gnu"* ]] && [ -f "dist/bulk-video-watermarker.AppImage" ]; then
    echo "AppImage created: dist/bulk-video-watermarker.AppImage"
fi
echo "Run it with: ./dist/bulk-video-watermarker"
echo ""
echo "Note: Ensure FFmpeg is installed on the target system for video processing."