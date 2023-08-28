from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()], render_kw={'readonly': True})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'readonly': True})
    position = StringField('Position', validators=[DataRequired()])  # New attribute: Position
    department = StringField('Department', validators=[DataRequired()])  # New attribute: Department
    submit = SubmitField('Update')
    

class DocumentForm(FlaskForm):
    file_name = StringField('File Name', validators=[DataRequired()])
    document = FileField('Document', validators=[DataRequired()])
    encryption_key = PasswordField('Encryption Key', validators=[DataRequired()])
    submit = SubmitField('Upload Document')

    def validate_encryption_key(form, field):
        if len(field.data) != 16:
            raise ValidationError('Encryption key must be 16 characters long.')
