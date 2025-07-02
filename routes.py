import os
import json
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from app import db, login_manager
from models import User, ProcessingJob
from forms import LoginForm, RegisterForm, UploadForm, MeasureSelectionForm
from utils import process_excel_file, allowed_file

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# Main application routes
@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get recent jobs for the user
    recent_jobs = ProcessingJob.query.filter_by(user_id=current_user.id)\
                                   .order_by(ProcessingJob.created_at.desc())\
                                   .limit(10).all()
    return render_template('dashboard.html', recent_jobs=recent_jobs)

@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                # Add timestamp to avoid conflicts
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Store filename in session for next step
                session['uploaded_file'] = filename
                flash('File uploaded successfully!', 'success')
                return redirect(url_for('main.process'))
                
            except RequestEntityTooLarge:
                flash('File is too large. Maximum size is 16MB.', 'error')
            except Exception as e:
                logging.error(f"Upload error: {str(e)}")
                flash('An error occurred during upload. Please try again.', 'error')
    
    return render_template('upload.html', form=form)

@main_bp.route('/process', methods=['GET', 'POST'])
@login_required
def process():
    # Check if we have an uploaded file
    if 'uploaded_file' not in session:
        flash('Please upload a file first.', 'warning')
        return redirect(url_for('main.upload'))
    
    form = MeasureSelectionForm()
    
    if form.validate_on_submit():
        filename = session['uploaded_file']
        selected_measures = form.measures.data
        
        if not selected_measures:
            flash('Please select at least one measure.', 'warning')
            return render_template('process.html', form=form, filename=filename)
        
        try:
            # Create processing job record
            job = ProcessingJob(
                user_id=current_user.id,
                filename=filename,
                measures=json.dumps(selected_measures),
                status='processing'
            )
            db.session.add(job)
            db.session.commit()
            
            # Process the file
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            result = process_excel_file(filepath, selected_measures, current_app.config['DOWNLOAD_FOLDER'])
            
            if result['success']:
                # Update job status
                job.status = 'completed'
                job.completed_at = datetime.utcnow()
                job.download_path = result['download_path']
                db.session.commit()
                
                # Clean up session
                session.pop('uploaded_file', None)
                
                flash('File processed successfully! You can download it now.', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                job.status = 'error'
                job.error_message = result['error']
                db.session.commit()
                flash(f'Processing failed: {result["error"]}', 'error')
                
        except Exception as e:
            logging.error(f"Processing error: {str(e)}")
            if 'job' in locals():
                job.status = 'error'
                job.error_message = str(e)
                db.session.commit()
            flash('An error occurred during processing. Please try again.', 'error')
    
    filename = session.get('uploaded_file', 'Unknown file')
    return render_template('process.html', form=form, filename=filename)

@main_bp.route('/download/<int:job_id>')
@login_required
def download(job_id):
    job = ProcessingJob.query.filter_by(id=job_id, user_id=current_user.id).first()
    
    if not job:
        flash('Job not found.', 'error')
        return redirect(url_for('main.dashboard'))
    
    if job.status != 'completed' or not job.download_path:
        flash('File is not ready for download.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    if not os.path.exists(job.download_path):
        flash('Download file not found.', 'error')
        return redirect(url_for('main.dashboard'))
    
    return send_file(
        job.download_path,
        as_attachment=True,
        download_name=f"processed_{job.filename}"
    )

@main_bp.route('/jobs')
@login_required
def jobs():
    user_jobs = ProcessingJob.query.filter_by(user_id=current_user.id)\
                                 .order_by(ProcessingJob.created_at.desc()).all()
    return render_template('dashboard.html', recent_jobs=user_jobs)

# Error handlers
@main_bp.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('main.upload'))
