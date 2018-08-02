from flask import render_template, request, session, redirect, url_for, flash
from . import pongBP
from app import get_db, socket
from flask_socketio import emit, send, join_room, rooms

@pongBP.route('/', methods=["GET", "POST"])
def pong():
	return render_template('playPong.html')

@socket.on('join_pong_room')
def join_pong_room(json):

	session['room'] = json['room']
	session['name'] = json['name']

	join_room(session['room'])

	db = get_db()
	db.execute("DELETE FROM pong WHERE name=?", (session['name'],))
	db.execute("INSERT INTO pong(name, room) VALUES(?,?)", (session['name'], session['room']))
	db.commit()

	room_info = db.execute("SELECT * FROM pong WHERE room=?", (session['room'],)).fetchall()

	emit('joined_pong', {'room': session['room'], 'name': session['name'], 'room_info': room_info}, room=session['room'])

@socket.on('start_pong')
def start_pong():
	db = get_db()
	room_info = db.execute("SELECT * FROM pong WHERE room=?", (session['room'],)).fetchall()
	socket.emit('start_pong', {'room_info': room_info}, room=session['room'])

@socket.on('upp')
def update_pong_position(json):
	socket.emit('upp', json, room=session['room'])

@socket.on('updateBall')
def update_ball(json):
	socket.emit('updateBall', json, room=session['room'])
