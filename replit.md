# MIPS Measure Filter - Web Application

## Overview

The MIPS Measure Filter is a Flask-based web application that automates the processing of patient visit data for MIPS (Merit-based Incentive Payment System) quality measures. The application allows healthcare providers to upload Excel files containing patient data and automatically filter patients based on specific MIPS measure criteria, generating downloadable reports with separate sheets for each measure.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite for development, configurable for production databases
- **Authentication**: Flask-Login with session-based authentication
- **File Processing**: Pandas for Excel file manipulation and data processing
- **Form Handling**: WTForms with Flask-WTF for secure form processing

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 dark theme
- **CSS Framework**: Bootstrap 5 with custom CSS overrides
- **JavaScript**: Vanilla JavaScript for client-side interactions
- **Icons**: Feather Icons for consistent iconography

### Data Processing Architecture
- **Modular Measure Processing**: Each MIPS measure has its own Python module in the `/measures` directory
- **Dynamic Loading**: Measure scripts are dynamically imported and executed based on user selection
- **Excel Generation**: OpenpyxL for creating multi-sheet Excel workbooks

## Key Components

### Authentication System
- User registration and login functionality
- Password hashing using Werkzeug security utilities
- Session management with Flask-Login
- User model with basic profile information

### File Upload System
- Drag-and-drop file upload interface
- File validation for Excel formats (.xlsx, .xls)
- 16MB file size limit
- Secure filename handling with Werkzeug

### Measure Processing Engine
- Six supported MIPS measures (47, 130, 226, 279, 331, 317)
- Age-based filtering logic with flexible column detection
- Support for both direct age columns and date-of-birth calculations
- Modular architecture allowing easy addition of new measures

### Job Management
- ProcessingJob model to track file processing status
- Job states: pending, processing, completed, error
- User-specific job history and downloads

### Report Generation
- Multi-sheet Excel workbooks with original data and filtered results
- Separate sheet for each selected measure
- Summary statistics and performance metrics

## Data Flow

1. **User Authentication**: Users register/login to access the application
2. **File Upload**: Users upload Excel files through drag-and-drop interface
3. **Measure Selection**: Users choose which MIPS measures to apply
4. **Data Processing**: Backend reads Excel file and applies measure-specific filtering
5. **Report Generation**: System creates multi-sheet workbook with results
6. **Download**: Users can download processed files from dashboard

## External Dependencies

### Python Packages
- Flask: Web framework
- SQLAlchemy: Database ORM
- Flask-Login: Authentication management
- Pandas: Data manipulation and analysis
- OpenpyXL: Excel file generation
- WTForms: Form handling and validation
- Werkzeug: WSGI utilities and security

### Frontend Libraries
- Bootstrap 5: CSS framework and components
- Feather Icons: Icon library
- Custom JavaScript for file upload and form interactions

## Deployment Strategy

### Local Development
- SQLite database for development
- Flask development server
- Environment variables for configuration
- Virtual environment for dependency isolation

### Production Deployment
- Configurable database URL for production databases
- ProxyFix middleware for reverse proxy compatibility
- Secure session key management
- File upload and download directory configuration

### Hosting Compatibility
- Designed for shared hosting and VPS deployment
- Minimal server requirements
- Self-contained application structure
- Environment-based configuration

## User Preferences

Preferred communication style: Simple, everyday language.

## Local Setup for Hosting

The application is designed to be fully portable and can run on any local server or hosting provider that supports Python/Flask applications:

### Quick Setup Commands
```bash
# 1. Install dependencies
pip install flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl werkzeug wtforms email-validator bcrypt gunicorn

# 2. Create directories
mkdir uploads downloads

# 3. Set environment variable
export SESSION_SECRET="your-secret-key-here"

# 4. Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 5. Run application
python run.py
```

### Alternative Setup
Run the automated setup script:
```bash
python setup.py
```

### Hosting Requirements
- Python 3.8+
- 50MB disk space minimum
- Write permissions for uploads/downloads folders
- No external database required (uses SQLite)

## Changelog

- July 02, 2025: Initial Flask application structure created
- July 02, 2025: Authentication system and file upload implemented
- July 02, 2025: Six MIPS measures processing logic added
- July 02, 2025: Template system and Bootstrap UI completed
- July 02, 2025: JavaScript validation issues fixed, single measure selection working
- July 02, 2025: Local setup documentation and automated setup script created