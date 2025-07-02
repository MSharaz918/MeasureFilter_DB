# MIPS Measure Filter - Local Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation Steps

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd mips-measure-filter

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file, install packages individually:
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl bcrypt email-validator werkzeug wtforms gunicorn psycopg2-binary sqlalchemy
```

### 4. Set Environment Variables
Create a `.env` file in the project root:
```env
SESSION_SECRET=your-secret-key-here-change-this-to-something-random
DATABASE_URL=sqlite:///mips_filter.db
UPLOAD_FOLDER=uploads
DOWNLOAD_FOLDER=downloads
MAX_CONTENT_LENGTH=16777216
```

### 5. Create Required Directories
```bash
mkdir uploads downloads
```

### 6. Initialize Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 7. Run the Application

#### Option 1: Development Server (Flask built-in)
```bash
python run.py
```

#### Option 2: Production Server (Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

#### Option 3: Direct Flask Run
```bash
python main.py
```

## Access the Application

Open your web browser and navigate to:
- http://localhost:5000
- http://127.0.0.1:5000

## Default Configuration

- **Database**: SQLite (stored as `mips_filter.db`)
- **Upload Folder**: `uploads/`
- **Download Folder**: `downloads/`
- **Max File Size**: 16MB
- **Supported Formats**: .xlsx, .xls

## Usage

1. **Register**: Create a new user account
2. **Login**: Sign in with your credentials
3. **Upload**: Drag and drop or select Excel files with patient data
4. **Select Measures**: Choose one or more MIPS measures to apply
5. **Process**: Wait for the system to filter and generate results
6. **Download**: Get your processed Excel file with results

## Supported MIPS Measures

- **Measure 47**: Advance Care Plan (Age ≥65)
- **Measure 130**: Documentation of Current Medications (Age ≥18)
- **Measure 226**: Preventive Care and Screening: Tobacco Use (Age ≥18)
- **Measure 279**: Depression Screening and Follow-Up Plan (Age ≥12)
- **Measure 331**: Adult Sinusitis: Antibiotic Prescribed (Age ≥18)
- **Measure 317**: Preventive Care and Screening: High Blood Pressure (Age ≥18)

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure the `uploads` and `downloads` folders are writable
2. **Database Errors**: Delete `mips_filter.db` and reinitialize the database
3. **Import Errors**: Make sure all dependencies are installed in your virtual environment
4. **Port Already in Use**: Change the port in the run command: `--bind 0.0.0.0:8000`

### File Format Requirements

Your Excel file should contain patient data with:
- Age information (either direct age column or date of birth)
- Patient visit records
- Standard medical data format

### Performance Notes

- Processing time depends on file size and number of selected measures
- Large files (>1000 patients) may take 30-60 seconds to process
- Results are saved with timestamp: `processed_mips_report_YYYYMMDD_HHMMSS.xlsx`

## Production Deployment

For production deployment (like Hostinger), see the `DEPLOYMENT.md` file for detailed instructions on:
- Shared hosting setup
- Database configuration
- File permissions
- Security considerations