from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class CodeForm(FlaskForm):
	user = StringField('User',  render_kw={"placeholder": "Username"})
	code = TextAreaField('code', validators=[DataRequired()], render_kw={"placeholder": "Share your code..."})
	submit = SubmitField('Share')