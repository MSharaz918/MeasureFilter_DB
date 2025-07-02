# MIPS Measure Filter - Web Application

A Flask-based web application that automates MIPS (Merit-based Incentive Payment System) measure filtering for medical practices. This application processes Excel files containing patient visit data and applies predefined denominator logic to filter eligible patients for selected MIPS Quality Measures.

## Features

- **User Authentication**: Secure login and registration system with SQLite database
- **File Upload**: Upload Excel files (.xlsx, .xls) with drag-and-drop support
- **Measure Selection**: Choose from 6 available MIPS measures (47, 130, 226, 279, 331, 317)
- **Automated Processing**: Apply measure-specific filtering logic to patient data
- **Excel Report Generation**: Download processed workbook with separate sheets for each measure
- **Dashboard**: Track processing jobs and download results
- **Responsive Design**: Works on desktop and tablet devices

## Available MIPS Measures

- **Measure 47**: Advance Care Plan (Age ≥65)
- **Measure 130**: Documentation of Current Medications (Age ≥18)
- **Measure 226**: Preventive Care and Screening: Tobacco Use (Age ≥18, preventive visits)
- **Measure 279**: Depression Screening and Follow-Up Plan (Age ≥12)
- **Measure 331**: Adult Sinusitis: Antibiotic Prescribed (Age ≥18, sinusitis diagnosis)
- **Measure 317**: Screening for High Blood Pressure (Age ≥18, outpatient visits)

## Local Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Download and extract the application files**
   ```bash
   # Extract the downloaded ZIP file to your desired directory
   cd mips-measure-filter
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl werkzeug wtforms email-validator bcrypt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file with your preferred settings
   # On Windows, you can use:
   copy .env.example .env
   ```

5. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

### Running the Application

1. **Start the Flask development server**
   ```bash
   python main.py
   ```
   
   Or alternatively:
   ```bash
   python run.py
   ```

2. **Access the application**
   - Open your web browser and go to: `http://localhost:5000`
   - Create a new account or use existing credentials

3. **Using the application**
   - Register a new account on the login page
   - Upload an Excel file with patient visit data
   - Select the MIPS measures you want to apply
   - Process the file and download the results

### File Structure

