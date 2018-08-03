from flask import render_template

from . import auth

@auth.route('/testAuth')
def testAuth():
	return render_template('testAuth.html')


