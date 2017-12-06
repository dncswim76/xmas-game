''' Configuration variables specific to application.'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv("SECRET_KEY", "local-key")
#SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "xmas_game.db")
SQLALCHEMY_DATABASE_URI = "sqlite:////var/www/xmas_game/xmas-game/xmas_game.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
