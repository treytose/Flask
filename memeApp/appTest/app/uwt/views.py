from . import uwt
from flask import render_template


@uwt.route('/')
def uwt():
	return render_template('uwt.html')
