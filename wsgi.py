#!/usr/bin/env python3
"""
WSGI configuration for MIPS Measure Filter application.
This file is used by web servers to serve the application.
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application
from main import app

# For WSGI servers
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)