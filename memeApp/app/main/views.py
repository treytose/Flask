from . import main
from flask import render_template, current_app, request, flash, redirect, url_for, send_from_directory, g, jsonify, escape
import os
from werkzeug.utils import secure_filename
from .forms import CodeForm
from app import get_db, socket
from flask_socketio import emit, send, join_room, rooms

UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

known_ip = {
	'172.17.35.73': 'Trey',
	'172.17.35.76': 'Kenny',
	'172.17.35.87': 'Mike'
}

@main.route('/share', methods=['GET', 'POST'])
def share():
	db = get_db()
	form = CodeForm()
	name = request.remote_addr
	if str(name) in known_ip:
		name = known_ip[str(name)]
		
	if form.validate_on_submit():
		code = form.code.data
		user = form.user.data 
		db.execute("INSERT INTO code (user,code) VALUES(?,?)", (user,code))
		return redirect(url_for('.share'))
		
	form.user.default = name
	form.process()
	code = db.execute("SELECT id,code,user,likes FROM code;").fetchall()
	users = db.execute("SELECT user FROM room").fetchall()
	
	return render_template('code.html', form=form, code=code, user=name, users=users)

@socket.on('like')
def like(id):
	db = get_db()
	num_likes = db.execute("SELECT likes FROM code WHERE id=?", (id,)).fetchone()[0] or 0
	num_likes += 1
	db.execute("UPDATE code SET likes=? WHERE id=?", (str(num_likes), id))
	emit('like', (id,num_likes), room=0)
	
@socket.on('join_room')
def join_handler(msg):
	join_room(0)
	db = get_db()
	name = request.remote_addr
	if str(name) in known_ip:
		name = known_ip[str(name)]

	db.execute("DELETE FROM room WHERE user=?",(name,))
	db.execute("INSERT INTO room (user) VALUES(?)",(name,))
	emit('message', name + ' joined the room', room=0)
	emit('user_joined', name, room=0)


@socket.on('leave')
def leave():
	db = get_db()
	name = request.remote_addr
	if str(name) in known_ip:
		name = known_ip[str(name)]
		db.execute("DELETE FROM room WHERE user=?",(name,))

	emit('message', name + ' left the room', room=0)
	emit('user_left', name, room=0)

@socket.on('message')
def handle_message(message):
		name = request.remote_addr
		if str(name) in known_ip:
			name = known_ip[str(name)]
		emit('message', name + ': ' + message, room=0)	


@main.route('/svg')
def svg():
	return render_template('svg.html')

@main.route('/crash')
def crash():
	return render_template('crash.html')

@main.route('/imageCheck')
def imageCheck():
	dirList = os.listdir('app/static/images')
	dictList = {os.path.getmtime('app/static/images/' + d) : d for d in dirList}
	timeList = sorted(dictList.keys())
	
	if len(dirList) > 1:
		os.remove('app/static/images/' + dictList[timeList[0]])
		return dictList[timeList[1]]
	elif len(dirList) > 0:
		return dirList[0]
	return '#'
	
@main.route('/webCheck')
def webCheck():
	webList = []
	f = open("app/static/webs.txt","r+")
	d = f.readlines()
	if len(d) > 1:
		f.seek(0)
		for i in d:
			if i != d[0]:
				f.write(i)
		f.truncate()
		f.close()
		return d[1]
	f.close()
	return d[0]

			
	return webList[0] or '#'
	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('main.index'))
    return render_template('index.html')

@main.before_request
def before_request():
	print('@main.before_request called in main/views.py')

@main.before_app_request
def before_app_request():
#	if request.remote_addr not in ['172.17.35.74', '172.17.35.80']:
#		return '<h1> Under Maintenance </h1>'
#	print('@main.before_app_request called in main/views.py')
	pass
@main.route('/brute')
def brute():
	return render_template('brute.html')
