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

        
        
# class RegisterItemForm(FlaskForm):
#     item_code = StringField('Kode Barang', validators=[DataRequired()])
#     item_name = StringField('Nama barang', validators=[DataRequired()])
#     submit = SubmitField('Tambah')

#     def validate_item_code(self, item_code):
#         item_code = Item.query.filter_by(item_code=item_code.data).first()
#         if item_code is not None:
#             raise ValidationError('Kode barang sudah ada.')

# class UpdateItemForm(FlaskForm):
#     item_code = StringField('Kode Barang', validators=[DataRequired()])
#     item_name = StringField('Nama barang', validators=[DataRequired()])
#     submit = SubmitField('Edit')

#     def validate_item_code(self, item_code):
#         item_code = Item.query.filter_by(item_code=item_code.data).first()
#         if item_code is not None:
#             raise ValidationError()
