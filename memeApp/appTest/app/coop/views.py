from . import coopBP
from flask import render_template
from flask_socketio import emit, send, join_room
from app import get_db, socket

@coopBP.route('/coop')
def coop():
	return render_template('coop.html')
	
@coopBP.route('/coopEdit')
def coopEdit():
	return render_template('coopEdit.html')
	
@socket.on('join_coop')
def join_coop(data):
	join_room(1)
	with open('app/templates/coopEdit.html', 'r') as f:
		text = ''.join(f.readlines())
	emit('update', text, room=1)
	
@socket.on('update')
def update(text):
	with open('app/templates/coopEdit.html', 'w') as f:
		f.write(text)
	print("UPDATED")
	emit('update', text, room=1)