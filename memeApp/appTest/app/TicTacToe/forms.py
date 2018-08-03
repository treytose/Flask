from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ChessForm(FlaskForm):
	url = StringField('URL', validators=[DataRequired()])
	submit = SubmitField('Submit')