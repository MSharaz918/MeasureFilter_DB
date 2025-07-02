# Hostinger Deployment Checklist

## Files to Upload
Make sure you upload ALL these files to your Hostinger public_html folder:

### Core Application Files
- [ ] app.py
- [ ] main.py
- [ ] run.py
- [ ] models.py
- [ ] routes.py
- [ ] forms.py
- [ ] utils.py
- [ ] wsgi.py
- [ ] passenger_wsgi.py
- [ ] .htaccess
- [ ] .env.example

### Folders (with all contents)
- [ ] measures/ (contains 47.py, 130.py, 226.py, 279.py, 331.py, 317.py, __init__.py)
- [ ] templates/ (contains all .html files)
- [ ] static/ (contains CSS, JS, and other assets)
- [ ] uploads/ (empty folder, will store uploaded files)
- [ ] downloads/ (empty folder, will store processed files)

## Step-by-Step Deployment

### 1. Upload Files
- [ ] Connect to Hostinger File Manager
- [ ] Navigate to public_html folder
- [ ] Upload all project files and folders

### 2. Install Dependencies (via SSH if available)
```bash
pip install --user flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl werkzeug wtforms email-validator bcrypt
```

### 3. Configure Environment
- [ ] Copy .env.example to .env
- [ ] Edit .env file:
  ```
  SESSION_SECRET=your-random-secret-key-here
  DATABASE_URL=sqlite:///mips_filter.db
  UPLOAD_FOLDER=uploads
  DOWNLOAD_FOLDER=downloads
  MAX_CONTENT_LENGTH=16777216
  ```

### 4. Set Permissions
```bash
chmod 755 uploads downloads
chmod 644 *.py
chmod 600 .env
```

### 5. Initialize Database
```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 6. Test Your Site
- [ ] Visit your domain: https://yourdomain.com
- [ ] Register a new account
- [ ] Login successfully
- [ ] Upload a test Excel file
- [ ] Select measures and process file
- [ ] Download results

## Alternative: Quick Setup Script

If you have SSH access, you can use the setup script:
```bash
python3 setup.py
```

## Common Hostinger-Specific Notes

1. **Python Version**: Hostinger typically uses Python 3.8+
2. **File Permissions**: Hostinger may require specific permissions
3. **Database**: SQLite works on most Hostinger plans
4. **File Uploads**: 16MB limit should work on most plans

## If Something Goes Wrong

### Check These Common Issues:
1. **500 Error**: Check file permissions and Python syntax
2. **Module Not Found**: Ensure all dependencies are installed
3. **Database Error**: Reinitialize the database
4. **Upload Issues**: Check folder permissions

### Get Help:
1. Check Hostinger's Python hosting documentation
2. Contact Hostinger support
3. Review server error logs if available

## Success Indicators
- [ ] Homepage loads without errors
- [ ] User registration works
- [ ] File upload completes
- [ ] Processing generates results
- [ ] Download links work
- [ ] All pages display correctly

Your MIPS Measure Filter application should now be live and accessible to users!