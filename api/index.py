"""
Vercel Serverless Function Wrapper for Flask App
This file allows the Flask app to run on Vercel's serverless platform
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import app
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, parent_dir)

from app import app

# Vercel expects the app to be exported as 'app'
# The Flask app will be automatically handled by Vercel's Python runtime
