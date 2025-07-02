from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=20, message='Username must be between 3 and 20 characters')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, message='Password must be at least 6 characters')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class UploadForm(FlaskForm):
    file = FileField('Excel File', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'Only Excel files are allowed!')
    ])
    submit = SubmitField('Upload File')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MeasureSelectionForm(FlaskForm):
    measures = MultiCheckboxField('Select MIPS Measures', choices=[
        ('47', 'Measure 47 - Advance Care Plan'),
        ('130', 'Measure 130 - Documentation of Current Medications'),
        ('226', 'Measure 226 - Preventive Care and Screening: Tobacco Use'),
        ('279', 'Measure 279 - Depression Screening and Follow-Up Plan'),
        ('331', 'Measure 331 - Adult Sinusitis: Antibiotic Prescribed'),
        ('317', 'Measure 317 - Preventive Care and Screening: Screening for High Blood Pressure')
    ])
    submit = SubmitField('Process File')
