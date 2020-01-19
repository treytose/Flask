from flask import render_template, redirect, url_for, session
from . import ticTacToe
from .forms import ChessForm
from .. import get_db

@ticTacToe.route('/play', methods=['GET', 'POST'])
def play():
	db = get_db()
	chessList = db.execute("SELECT url FROM chess;").fetchall()
	form = ChessForm()
	if form.validate_on_submit():
		url = form.url.data
		session['url'] = url
		db.execute("INSERT INTO chess (url) VALUES(?)", (url,))
		return redirect(url_for('.play'))
	return render_template('play.html', form=form, chessList=chessList, url=session.get('url'))


'''
 CREATE TRIGGER delete_first AFTER INSERT ON chess
   ...> BEGIN
   ...> WHEN (SELECT count(*) FROM chess) > 1
   ...> BEGIN
   ...> DELETE FROM chess WHERE id in (SELECT id FROM chess LIMIT 1);
   ...> END;
'''