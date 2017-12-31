from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500) #NOTE: use app_errorhandler to catch application-wide errors
def internal_server_error():    #   instead of errors for just this blueprint.
    return render_template('500.html'), 500
