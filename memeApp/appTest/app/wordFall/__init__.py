from flask import Blueprint

wordFall = Blueprint('wordFall', __name__)

from . import views
