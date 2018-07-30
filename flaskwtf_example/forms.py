from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from flask import flash

def CustomValidator(form, field):
	if len(field.data) < 3:
		flash('Field must be at least 3 characters long!')
		raise ValidationError('Field must be at least 3 characters long!')

class LoginForm(FlaskForm):
	username = StringField('Username',  render_kw={"placeholder": "Username"})
	password = PasswordField('Password', validators=[DataRequired(), CustomValidator])
	submit = SubmitField('Login')

