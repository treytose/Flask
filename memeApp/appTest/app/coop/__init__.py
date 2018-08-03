from flask import Blueprint

coopBP = Blueprint('coop', __name__)

from . import views
