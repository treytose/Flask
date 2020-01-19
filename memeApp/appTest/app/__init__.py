from flask import Flask, g 
import config
import sqlite3
from flask_socketio import SocketIO


DATABASE = '/home/olholthe/projects/appTest/data.db'
# declare extensions here #
socket = SocketIO()

def get_db():
        db = getattr(g, '_database', None)
        if not db:
                db = g._database = sqlite3.connect(DATABASE)
        return db

def create_app(config_name='default'):
	app = Flask(__name__)
	app.config.from_object(config.config[config_name])
	
	# init extensions here #
	socket.init_app(app)
	
	# Register Blueprints here #
	from app.main import main as mainBP
	from app.auth import auth as authBP
	from app.TicTacToe import ticTacToe as tBP
	from app.uwt import uwt as uwtBP
	from app.coop import coopBP
	from app.wordFall import wordFall as wfBP
	from app.pong import pongBP

	app.register_blueprint(mainBP)
	app.register_blueprint(authBP, url_prefix='/auth')
	app.register_blueprint(tBP)
	app.register_blueprint(uwtBP, url_prefix='/uwt')
	app.register_blueprint(coopBP)
	app.register_blueprint(wfBP)
	app.register_blueprint(pongBP, url_prefix='/pong')

	return app
