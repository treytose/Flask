from flask import Flask, g
from flask_socketio import SocketIO
import sqlite3


DATABASE = '/home/olholthe/projects/flaskRepo/Flask/MusicApp/data.db'
socket = SocketIO()

def get_db():
        db = getattr(g, '_database', None)
        if not db:
                db = g._database = sqlite3.connect(DATABASE)
        return db


def create_app():
	app = Flask(__name__)

	# Init Extensions with Flask App #
	socket.init_app(app)

	# Import and register Blueprints #
	from app.main import mainBP
	app.register_blueprint(mainBP)

	return app