#!/usr/bin/env python3
"""
Bulk Video Overlay and Watermarking Tool
Main entry point for the GUI application.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui import main
except ImportError as e:
    if 'PySide6' in str(e) or 'moviepy' in str(e):
        print("Error: Required packages not found. Please activate the virtual environment:")
        print("  source venv/bin/activate")
        print("  python main.py")
        print("Or use the run script: ./run.sh")
        sys.exit(1)
    else:
        raise

if __name__ == "__main__":
    main()
