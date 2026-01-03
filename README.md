# Bulk Video Overlay and Watermarking Tool

A production-grade desktop GUI application for bulk video overlay and watermarking, designed for creators, agencies, and automation workflows.

## Features

- Bulk processing of 100+ videos
- Support for image, video, and text overlays
- Presets for YouTube Shorts, Reels, TikTok, etc.
- Drag & drop support
- Preview system
- Queue system with pause/resume
- Export options with custom resolutions and bitrates
- Preset management (save, load, delete)
- Overlay editor for configuring overlays
- Error handling and progress tracking

## Installation

1. Clone the repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Ensure FFmpeg is installed: `sudo apt install ffmpeg` (on Linux)

## Building

To build a standalone executable for your platform (handles fresh clones automatically):

```bash
./build.sh
```

This script will:
- Create a virtual environment if it doesn't exist
- Install all required dependencies
- Check for FFmpeg availability
- Build the executable with PyInstaller
- Output the executable in `dist/bulk-video-watermarker`

The build script is designed for multi-platform use - run it on Linux, macOS, or Windows to build for that platform.

## Usage

Activate the virtual environment and run the application:

```bash
source venv/bin/activate
python main.py
```

Or use the provided run script:

```bash
./run.sh
```

### Interface

The application features a streamlined single-panel interface for bulk video processing:

- **Input Folder**: Select the folder containing videos to process
- **Output Folder**: Choose where processed videos will be saved
- **Overlay Type**: Choose between Image, Video, or Text overlays
- **Overlay Configuration**: Configure scale, position, opacity, and other settings
- **Process Button**: Start bulk processing with real-time progress updates

### Presets

Sample presets are included:
- YouTube Shorts: Corner watermark
- TikTok: Logo in bottom right

### CSV Mapping

Use CSV for per-video customization. Sample CSV:

```
video,watermark,text,position
video1.mp4,logo.png,Title 1,center
video2.mp4,watermark.png,Title 2,right-bottom
```

## Building

Use PyInstaller to package: `pyinstaller --onefile --windowed main.py`

## Requirements

- Python 3.8+
- FFmpeg
- PySide6
- MoviePy
- OpenCV
- Pillow
- NumPy

## Folder Structure

```
.
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md               # This file
├── sample_csv.csv          # Sample CSV for mapping
├── src/
│   └── gui.py              # GUI application
├── assets/                 # Icons, sample files
├── presets/                # Preset files
└── tests/                  # Unit tests
```