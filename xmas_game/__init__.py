from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_sqlalchemy import SQLAlchemy


# instantiate app
app = Flask(__name__)
# load configuration settings
app.config.from_object('config')
# initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# initialize LoginManager
#login_manager = LoginManager()
#login_manager.login_view = 'login'
#login_manager.init_app(app)
# initialize manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server)

from xmas_game import models
