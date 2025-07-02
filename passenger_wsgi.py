#!/usr/bin/env python3
"""
Passenger WSGI configuration for MIPS Measure Filter application.
This file is used by Passenger-based hosting (common on shared hosting).
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application
from main import app as application

# Passenger expects the WSGI application to be named 'application'
if __name__ == '__main__':
    application.run()