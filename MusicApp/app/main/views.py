from flask import render_template, request, redirect, url_for
from . import mainBP
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from app import get_db, socket

UPLOAD_FOLDER = '/home/olholthe/projects/flaskRepo/Flask/MusicApp/app/static/sounds'
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])

@mainBP.route('/')
def index():
	db = get_db()
	json = db.execute("SELECT * FROM music;").fetchall()
	return render_template('index.html', json=json)

##### Web Socket #####



###### File Upload ######
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mainBP.route('/upload', methods=['POST'])
def upload():
		if 'file' not in request.files:
			print('File not in request!')
			return redirect(url_for('.index'))
		file = request.files['file']

		if file.filename == '':
			print('filename is empty')
			return redirect(url_for('.index'))

		print(Path(os.path.join(UPLOAD_FOLDER, file.filename)))

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if not Path(os.path.join(UPLOAD_FOLDER, file.filename)).is_file():
				file.save(os.path.join(UPLOAD_FOLDER, filename))
			slot = request.form['slot']

			db = get_db()
			db.execute('INSERT OR REPLACE INTO music(slot, file) VALUES(?,?);', (slot, filename))

		return redirect(url_for('.index'))

