from flask import Flask
from flask_login import LoginManager

# declare the login manager - initted in create_app()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # init extensions here #
    login_manager.init_app(app)

    # import & register blueprints here #
    from app.main import mainBP
    from app.auth import authBP

    app.register_blueprint(mainBP)
    app.register_blueprint(authBP, url_prefix='/auth')

    return app

# standard config options for the flask app
class config:
    SECRET_KEY = 'randomSuperSecretKey'
