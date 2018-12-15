from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from models.UserModel import User
import random

gamesBP = Blueprint('games', __name__, template_folder='templates',
                    static_folder='static', static_url_path='/games/static')

@gamesBP.before_request
def before_request():
    user = getUser()
    if not user:
        return redirect(url_for('index'))

@gamesBP.route('/games')
def games():
    return render_template('games.html', username=getUser().username)

@gamesBP.route('/colorsGame')
def colorsGame():
    return render_template('colorsGame.html', username=getUser().username)

@gamesBP.route('/jumpMan')
def jumpManGame():
    return render_template('jumpMan.html', username=getUser().username)

@gamesBP.route('/loadedQuestions')
def loadedQuestions():
    return redirect('/LQ/lobby')

@gamesBP.route('/cowtownCowboy')
def cowtownCowboy():
    return render_template('CowtownCowboy.html', username=getUser().username)

def getUser():
    user = User.json_to_user(session.get('User'))
    return user if user else None
#---------------------------------loadedQuestions
