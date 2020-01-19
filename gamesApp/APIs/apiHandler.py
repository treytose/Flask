from flask import Blueprint, jsonify, session, redirect, url_for
from APIs import weatherAPI
from models.UserModel import User


apiBP = Blueprint('api', __name__, template_folder='templates',
                    static_folder='static', static_url_path='/APIs/static',
                    url_prefix='/api')

@apiBP.before_request
def before_request():
    user = getUser()
    if not user:
        return redirect(url_for('index'))

@apiBP.route('/weatherData/<zipcode>')
def weatherData(zipcode=None):
    return jsonify(weatherAPI.get_weather_data(zipcode))

def getUser():
    user = User.json_to_user(session.get('User'))
    return user if user else None
