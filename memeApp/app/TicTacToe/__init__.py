from flask import Blueprint

ticTacToe = Blueprint('ticTacToe', __name__)

from . import views
