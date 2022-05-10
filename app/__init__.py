from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config_options

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager=LoginManager()
login_manager.session_protection='strong'


def create_app(config_name):
    global db, login_manager
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Database settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = ''

    db = SQLAlchemy(app)
    db.create_all()
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.init_app(app)

    # Initializing flask extensions
    bootstrap.init_app(app)

     # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app