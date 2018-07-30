from flask import Flask, render_template, flash
from forms import LoginForm

app = Flask(__name__)

app.secret_key = 'asdkfjasdf;kjasdf;kj'

@app.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm()

	if form.validate_on_submit():
		# Do stuff with data here #
		flash('Username: ' + form.username.data)
		flash('Password: ' + form.password.data)

		# redirect here if needed #



	return render_template('index.html', form=form)



if __name__ == '__main__':
	app.run(port=5001, host='0.0.0.0', debug=True)