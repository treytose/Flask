from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from models.UserModel import User
import random

budgetBP = Blueprint('budget', __name__, template_folder='templates',
                    static_folder='static', static_url_path='/budget_calculator/static')

@budgetBP.before_request
def before_request():
    user = getUser()
    if not user:
        return redirect(url_for('index'))

@budgetBP.route('/budget')
def budget():
    return render_template('budget.html', username=getUser().username)


def getUser():
    user = User.json_to_user(session.get('User'))
    return user if user else None
