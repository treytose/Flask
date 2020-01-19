from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import Required, Email, Length, EqualTo, Regexp

# Using Flask-Wtf to create the login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email(), Length(4,64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    
