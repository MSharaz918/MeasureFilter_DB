#!/usr/bin/env python3
"""
Alternative entry point for the MIPS Measure Filter application.
This can be used instead of main.py to start the application.
"""

import os
import logging
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    # Get configuration from environment
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    logging.info(f"Starting MIPS Measure Filter application on {host}:{port}")
    logging.info(f"Debug mode: {debug}")
    
    try:
        app.run(host=host, port=port, debug=debug)
    except Exception as e:
        logging.error(f"Failed to start application: {str(e)}")
        raise
