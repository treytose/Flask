#!/usr/bin/python3.6

#Run with: gunicorn -w 4 -b 0.0.0.0:80 manage:app

import os
from app import create_app, db
from app.models import User, Role

config_mode = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_mode)

if __name__ == '__main__':
    print('Running app in config mode: ' + config_mode)
    app.run(host='0.0.0.0', port=80)
