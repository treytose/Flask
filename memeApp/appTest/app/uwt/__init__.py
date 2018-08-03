from flask import Blueprint

uwt = Blueprint('uwt', __name__)

from . import views
