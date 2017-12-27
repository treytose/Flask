from flask import Flask, render_template, url_for, request, redirect, flash, session
from models.UserModel import User
import os #for creating random secret_key
from subprocess import call
from emailHandler import send_email
import requests #used to call googles recatpcha api for /register

import socket

#Blueprints
from games import games
from games.loadedQuestions import loadedQuestions
from games.trivia import trivia
from APIs import apiHandler

app = Flask(__name__)

def register_blueprints(blueprints):
    for b in blueprints:
        app.register_blueprint(b)

register_blueprints([games.gamesBP, trivia.triviaBP, loadedQuestions.loadedQuestionsBP, apiHandler.apiBP])


app.secret_key = os.urandom(24)

hacker_keywords = ['php', 'myadmin', 'sql']
@app.before_request
def ip_tracker():
    if any(val in request.path.lower() for val in hacker_keywords):
        call(["ipset", "add", "blacklist", request.remote_addr])
        send_email('Hack Attempt Detected', 'A hack attempt from IP: ' +
            request.remote_addr + ' has been detected and blacklisted.')

@app.route("/")
def index():
    if 'User' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
    user = (User.find_by_username(request.form.get('username')))
    if user and user.check_pass(request.form.get('password')):
        session['User'] = user.toJSON()
        return redirect(url_for('dashboard'))

    flash('*Invalid Username or Password')
    return redirect(url_for('index'))

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = {    #data for googles recaptcha api
        'secret': '6LerdTwUAAAAAOVc_RKwqdsK9I-gKxZ8_xdhnT4j',
        'response': request.form['g-recaptcha-response'],
        'remoteip': request.remote_addr
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    captcha_success = response.json()['success']

    if captcha_success:
        register_success = User.register_user(**request.form)

        if not register_success:    #registering unsuccessful
            flash("*Username already exists")
            return redirect(url_for('register'))
        return redirect(url_for('index'))   #redirect to login page on succesful registery

    flash("Are you a robot?")    #captcha unsuccessful
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    user = User.json_to_user(session.get('User'))
    if user is None:
        flash('*You must sign in first.')
        return redirect(url_for('index'))
    return render_template('dashboard.html', title='Home', username=user.username.title())


@app.route('/logout', methods=['POST'])
def logout():
    user = User.json_to_user(session.get('User'))
    if user is None:
        return redirect(url_for('index'))
    session.pop('User', None)
    flash('Sign Out Successful')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
