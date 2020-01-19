from . import mainBP
from flask import render_template


@mainBP.route('/')
def index():
    return render_template('main/index.html')


@mainBP.route('/auth-level-1')
def auth_level_1():
    return 'TODO'

# TODO create different authentication levels
