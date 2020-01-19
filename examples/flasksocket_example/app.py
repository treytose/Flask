from flask import Flask, render_template, session
from flask_socketio import SocketIO, send, emit, join_room, rooms

app = Flask(__name__)
socket = SocketIO(app)

@app.route('/')
def index():
	return render_template('index.html')

@socket.on('join')
def join(roomID):
	session['room'] = roomID
	send('You joined room: ' + roomID + '!')

@socket.on('message')
def handle_message(msg):
	send(msg + ', room: ' + session['room'])

if __name__ == '__main__':
	socket.run(app, host='0.0.0.0', port=5001, debug=True)