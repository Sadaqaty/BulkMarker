#!/usr/bin/env python3
"""
Bulk Video Overlay and Watermarking Tool
Main entry point for the GUI application.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui import main

if __name__ == "__main__":
    main()
