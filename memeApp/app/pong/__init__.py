from flask import Blueprint

pongBP = Blueprint('pong', __name__)

from . import views