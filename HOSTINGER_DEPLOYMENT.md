# Hostinger Deployment Guide - MIPS Measure Filter

## Prerequisites

- Hostinger hosting account with Python support
- SSH access to your hosting account
- Domain name configured

## Step-by-Step Deployment

### 1. Prepare Your Files

1. **Download all project files** from your development environment
2. **Create a ZIP file** containing all the project files:
   ```
   mips-measure-filter/
   ├── app.py
   ├── main.py
   ├── run.py
   ├── models.py
   ├── routes.py
   ├── forms.py
   ├── utils.py
   ├── measures/
   ├── templates/
   ├── static/
   ├── uploads/
   ├── downloads/
   ├── .env.example
   └── setup.py
   ```

### 2. Upload to Hostinger

#### Method 1: File Manager (Easiest)
1. Login to your Hostinger control panel
2. Go to **File Manager**
3. Navigate to `public_html` folder
4. Upload your ZIP file
5. Extract it in the `public_html` directory

#### Method 2: FTP/SFTP
1. Use an FTP client (FileZilla, WinSCP)
2. Connect using your Hostinger FTP credentials
3. Upload files to the `public_html` directory

### 3. SSH Setup (If Available)

1. **Connect via SSH:**
   ```bash
   ssh your-username@your-domain.com
   ```

2. **Navigate to your domain folder:**
   ```bash
   cd public_html
   ```

### 4. Install Dependencies

#### Option 1: Using pip (if available)
```bash
pip install --user flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl werkzeug wtforms email-validator bcrypt gunicorn
```

#### Option 2: Virtual Environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl werkzeug wtforms email-validator bcrypt gunicorn
```

### 5. Configure Environment

1. **Create .env file:**
   ```bash
   cp .env.example .env
   nano .env
   ```

2. **Edit the .env file:**
   ```env
   SESSION_SECRET=your-random-secure-secret-key-change-this
   DATABASE_URL=sqlite:///mips_filter.db
   UPLOAD_FOLDER=uploads
   DOWNLOAD_FOLDER=downloads
   MAX_CONTENT_LENGTH=16777216
   ```

3. **Set proper permissions:**
   ```bash
   chmod 755 uploads downloads
   chmod 644 *.py
   chmod 600 .env
   ```

### 6. Initialize Database

```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 7. Create WSGI Application File

Create `wsgi.py` in your root directory:
```python
#!/usr/bin/env python3
import sys
import os

# Add your project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from main import app

if __name__ == "__main__":
    app.run()
```

### 8. Configure Web Server

#### For Apache (most common on Hostinger):

Create `.htaccess` file in your root directory:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ wsgi.py/$1 [QSA,L]

# Python handler
AddHandler cgi-script .py
Options +ExecCGI

# Security headers
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"

# File upload limits
LimitRequestBody 16777216

# Cache static files
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|svg)$">
    ExpiresActive On
    ExpiresDefault "access plus 1 month"
</FilesMatch>
```

#### Alternative: Create passenger_wsgi.py (if using Passenger)
```python
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from main import app as application

if __name__ == '__main__':
    application.run()
```

### 9. Test Your Deployment

1. **Visit your domain:** `https://yourdomain.com`
2. **Check if the application loads**
3. **Test registration and login**
4. **Try uploading a small test file**

## Alternative Deployment Methods

### Method 1: Using Gunicorn (if supported)

1. **Create startup script** `start_app.sh`:
   ```bash
   #!/bin/bash
   cd /path/to/your/app
   source venv/bin/activate
   gunicorn --bind 0.0.0.0:8000 --workers 2 main:app
   ```

2. **Make it executable:**
   ```bash
   chmod +x start_app.sh
   ```

### Method 2: Using systemd service (VPS)

Create `/etc/systemd/system/mips-filter.service`:
```ini
[Unit]
Description=MIPS Measure Filter Application
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/venv/bin
ExecStart=/path/to/your/app/venv/bin/gunicorn --bind 0.0.0.0:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mips-filter
sudo systemctl start mips-filter
```

## Troubleshooting

### Common Issues

1. **Permission Errors:**
   ```bash
   chmod 755 uploads downloads
   chown -R your-username:your-username /path/to/app
   ```

2. **Python Path Issues:**
   - Ensure all Python files are in the correct directory
   - Check Python version compatibility (`python3 --version`)

3. **Database Errors:**
   ```bash
   rm mips_filter.db
   python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Module Import Errors:**
   - Verify all dependencies are installed
   - Check virtual environment is activated

### File Permissions

```bash
# Set correct permissions
find . -type f -name "*.py" -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
chmod 755 uploads downloads
chmod 600 .env
```

### Environment Variables

If .env doesn't work, set environment variables directly:
```bash
export SESSION_SECRET="your-secret-key"
export DATABASE_URL="sqlite:///mips_filter.db"
```

## Performance Optimization

### For Production:

1. **Enable caching:**
   ```python
   # In app.py
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

2. **Optimize database:**
   ```python
   # Consider PostgreSQL for high traffic
   DATABASE_URL=postgresql://user:pass@localhost/mips_filter
   ```

3. **Use CDN for static files**

4. **Enable gzip compression in .htaccess:**
   ```apache
   <IfModule mod_deflate.c>
       AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
   </IfModule>
   ```

## Security Considerations

1. **Change default secret key**
2. **Use HTTPS (SSL certificate)**
3. **Regular database backups**
4. **Monitor file upload directory**
5. **Keep dependencies updated**

## Support

If you encounter issues:
1. Check Hostinger's Python documentation
2. Contact Hostinger support for Python-specific questions
3. Review application logs for error messages
4. Test locally first before deploying

## Quick Deployment Checklist

- [ ] Upload all project files
- [ ] Install Python dependencies
- [ ] Create and configure .env file
- [ ] Set proper file permissions
- [ ] Initialize database
- [ ] Configure web server (.htaccess or passenger_wsgi.py)
- [ ] Test application functionality
- [ ] Verify file upload/download works
- [ ] Check SSL certificate
- [ ] Set up regular backups