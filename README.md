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

## Usage

Run the application: `python main.py`

### Tabs

- **Dashboard**: Overview and quick actions
- **Bulk Processing**: Select input/output folders, watermark, settings, and process videos
- **Overlay Editor**: Configure image, video, and text overlays
- **Presets**: Manage presets (YouTube Shorts, TikTok, etc.)
- **Export & Queue**: Manage export settings and processing queue
- **Settings**: Application settings

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