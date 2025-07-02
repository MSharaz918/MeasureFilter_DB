#!/usr/bin/env python3
"""
MIPS Measure Filter - Quick Setup Script
This script helps set up the application locally with minimal effort.
"""

import os
import sys
import subprocess
import sqlite3

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return False

def create_directories():
    """Create required directories."""
    dirs = ['uploads', 'downloads']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"✓ Created directory: {dir_name}")
        else:
            print(f"✓ Directory already exists: {dir_name}")

def setup_environment():
    """Set up environment variables."""
    env_file = '.env'
    if not os.path.exists(env_file):
        env_content = """# MIPS Measure Filter Environment Configuration
SESSION_SECRET=mips-filter-secret-key-change-this-in-production
DATABASE_URL=sqlite:///mips_filter.db
UPLOAD_FOLDER=uploads
DOWNLOAD_FOLDER=downloads
MAX_CONTENT_LENGTH=16777216
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✓ Created {env_file} with default settings")
    else:
        print(f"✓ Environment file already exists: {env_file}")

def install_packages():
    """Install required Python packages."""
    packages = [
        'flask',
        'flask-sqlalchemy', 
        'flask-login',
        'flask-wtf',
        'pandas',
        'openpyxl',
        'werkzeug',
        'wtforms',
        'email-validator',
        'bcrypt',
        'gunicorn'
    ]
    
    print("Installing required packages...")
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package}"):
            print(f"Warning: Failed to install {package}")
            return False
    return True

def initialize_database():
    """Initialize the SQLite database."""
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 50)
    print("MIPS Measure Filter - Quick Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Setup steps
    steps = [
        ("Creating directories", create_directories),
        ("Setting up environment", setup_environment),
        ("Installing packages", install_packages),
        ("Initializing database", initialize_database)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"✗ Setup failed at: {step_name}")
            return False
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("=" * 50)
    print("\nTo start the application:")
    print("  python run.py")
    print("\nThen open your browser to:")
    print("  http://localhost:5000")
    print("\nTo stop the application, press Ctrl+C")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)