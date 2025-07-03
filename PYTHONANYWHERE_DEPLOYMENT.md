# PythonAnywhere Deployment Guide - MIPS Measure Filter

## Why PythonAnywhere is Perfect for This Project

✓ **Built for Python** - Native Flask support
✓ **Easy Setup** - No complex server configuration
✓ **Free Tier Available** - Great for testing and small usage
✓ **SQLite Support** - Works perfectly with our database
✓ **File Management** - Built-in file manager and console
✓ **HTTPS Included** - Automatic SSL certificates

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account
- Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
- Sign up for a free account (or paid for custom domain)

### 2. Upload Your Files

#### Option A: Using Git (Recommended)
```bash
# In PythonAnywhere console
git clone https://github.com/yourusername/mips-measure-filter.git
cd mips-measure-filter
```

#### Option B: Upload Files Manually
- Use the "Files" tab in PythonAnywhere dashboard
- Create a new directory: `/home/yourusername/mips-measure-filter`
- Upload all your project files

### 3. Set Up Virtual Environment
```bash
# In PythonAnywhere console
cd /home/yourusername/mips-measure-filter
python3.10 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl werkzeug wtforms email-validator bcrypt
```

### 5. Configure Environment
```bash
# Create .env file
cp .env.example .env
nano .env
```

Edit the .env file:
```env
SESSION_SECRET=your-random-secret-key-here
DATABASE_URL=sqlite:///mips_filter.db
UPLOAD_FOLDER=uploads
DOWNLOAD_FOLDER=downloads
MAX_CONTENT_LENGTH=16777216
```

### 6. Initialize Database
```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 7. Configure Web App

1. **Go to Web tab** in PythonAnywhere dashboard
2. **Click "Add a new web app"**
3. **Choose "Manual configuration"**
4. **Select Python 3.10**
5. **Configure the following:**

#### Source Code Path:
```
/home/yourusername/mips-measure-filter
```

#### Working Directory:
```
/home/yourusername/mips-measure-filter
```

#### WSGI Configuration File:
Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import sys
import os

# Add your project directory to the Python path
project_home = '/home/yourusername/mips-measure-filter'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SESSION_SECRET'] = 'your-secret-key-here'
os.environ['DATABASE_URL'] = 'sqlite:///mips_filter.db'

from main import app as application
```

#### Virtual Environment:
```
/home/yourusername/mips-measure-filter/venv
```

### 8. Configure Static Files
In the Web tab, add static file mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/mips-measure-filter/static/` |

### 9. Set Up File Permissions
```bash
chmod 755 uploads downloads
chmod 644 *.py
```

### 10. Reload and Test
- Click "Reload" button in Web tab
- Visit your app at: `https://yourusername.pythonanywhere.com`

## Configuration Details

### Free Account Limitations:
- 1 web app
- 512MB storage
- Custom domain not included
- Basic CPU seconds limit

### Paid Account Benefits:
- Multiple web apps
- More storage
- Custom domain support
- More CPU seconds
- SSH access

## File Structure on PythonAnywhere
```
/home/yourusername/mips-measure-filter/
├── app.py
├── main.py
├── models.py
├── routes.py
├── forms.py
├── utils.py
├── measures/
├── templates/
├── static/
├── uploads/
├── downloads/
├── venv/
└── .env
```

## Troubleshooting

### Common Issues:

1. **Import Errors:**
   - Check virtual environment is properly configured
   - Verify all dependencies are installed

2. **Database Errors:**
   ```bash
   rm mips_filter.db
   python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

3. **File Upload Issues:**
   - Check folder permissions
   - Verify UPLOAD_FOLDER path is correct

4. **Static Files Not Loading:**
   - Verify static file mapping in Web tab
   - Check file paths are correct

### Debugging:
- Check error logs in Web tab
- Use PythonAnywhere console for testing
- Test database connection manually

## Environment Variables Alternative

If .env file doesn't work, set variables directly in WSGI file:
```python
# In WSGI configuration
os.environ['SESSION_SECRET'] = 'your-secret-key'
os.environ['DATABASE_URL'] = 'sqlite:///mips_filter.db'
os.environ['UPLOAD_FOLDER'] = 'uploads'
os.environ['DOWNLOAD_FOLDER'] = 'downloads'
```

## Performance Tips

1. **Use SQLite WAL mode** for better performance:
   ```python
   app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
       'pool_pre_ping': True,
       'pool_recycle': 300,
       'connect_args': {'check_same_thread': False}
   }
   ```

2. **Optimize file uploads:**
   - Consider file cleanup tasks
   - Monitor storage usage

3. **Enable caching** if needed:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

## Advantages of PythonAnywhere

✓ **No server setup required**
✓ **Python-native environment**
✓ **Built-in console access**
✓ **Easy file management**
✓ **Automatic HTTPS**
✓ **Reliable hosting**
✓ **Good for development and production**

## Your App URLs

- **Free Account:** `https://yourusername.pythonanywhere.com`
- **Paid Account:** `https://yourdomain.com` (custom domain)

## Quick Setup Commands

```bash
# All commands for PythonAnywhere console
cd /home/yourusername/mips-measure-filter
python3.10 -m venv venv
source venv/bin/activate
pip install flask flask-sqlalchemy flask-login flask-wtf pandas openpyxl werkzeug wtforms email-validator bcrypt
cp .env.example .env
# Edit .env file with your settings
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
chmod 755 uploads downloads
```

Then configure the Web app in the dashboard and reload!

PythonAnywhere is definitely one of the easiest ways to deploy this Flask application.