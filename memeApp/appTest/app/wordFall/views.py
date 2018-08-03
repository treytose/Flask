from flask import render_template, session, request
from . import wordFall
from flask_socketio import emit, send, join_room
from app import get_db, socket
import time
from random import randint

known_ip = {
	'172.17.35.73': 'Trey',
	'172.17.35.65': 'Kenny',
	'172.17.35.87': 'Mike'
}

randWords = ["Adult", "Aeroplane", "Air", "Aircraft Carrier", "Airforce", "Airport", 
			"Album", "Alphabet", "Apple", "Arm", "Army", "Baby", "Baby", "Backpack", 
			"Balloon", "Banana", "Bank", "Barbecue", "Bathroom", "Bathtub", "Bed", "Bed", 
			"Bee", "Bible", "Bible", "Bird", "Bomb", "Book", "Boss", "Bottle", "Bowl", "Box", 
			"Boy", "Brain", "Bridge", "Butterfly", "Button", "Cappuccino", "Car", "Car-race", 
			"Carpet", "Carrot", "Cave", "Chair", "Chess Board", "Chief", "Child", "Chisel",
			 "Chocolates", "Church", "Church", "Circle", "Circus", "Circus", "Clock", "Clown", 
			 "Coffee", "Coffee-shop", "Comet", "Compact Disc", "Compass", "Computer", "Crystal", 
			 "Cup", "Cycle", "Data Base", "Desk", "Diamond", "Dress", "Drill", "Drink", "Drum", 
			 "Dung", "Ears", "Earth", "Egg", "Electricity", "Elephant", "Eraser", "Explosive", 
			 "Eyes", "Family", "Fan", "Feather", "Festival", "Film", "Finger", "Fire", "Floodlight", 
			 "Flower", "Foot", "Fork", "Freeway", "Fruit", "Fungus", "Game", "Garden", "Gas", "Gate", "Gemstone", "MikeSucks",
			 ""]

@wordFall.route('/wordFall')
def wordFall():
	return render_template('wordFall.html')

@socket.on('join_wordFall')
def join_wordFall(room):
	join_room(room)
	session['room'] = room
	name = request.remote_addr
	if str(name) in known_ip:
		name = known_ip[str(name)]
	emit('joined_wf', name, room=session['room'])

@socket.on('start_wf')
def start_wf(msg):
	emit('start_wf', msg, room=session['room'])


@socket.on('move_word')
def move_word():
	emit('move_word', randWords[randint(0,len(randWords)-1)].lower(), room=session['room'])


@socket.on('scored')
def scored(points, word):
	name = request.remote_addr
	if str(name) in known_ip:
		name = known_ip[str(name)]
	emit('scored', (name, points), room=session['room'])
	emit('remove_word', word, room=session['room'])

@socket.on('present')
def present():
	name = request.remote_addr
	if str(name) in known_ip:
		name = known_ip[str(name)]
	emit('joined_wf', name,  room=session['room'])

@socket.on('winner')
def winner(name):
	emit('winner', name + ' has won the game!', room=session['room'])