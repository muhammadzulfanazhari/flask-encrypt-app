import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from importlib import import_module

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Hey there! Please log in to access this page.'
moment = Moment()


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)


def register_blueprints(app):
    for module_name in ('auth', 'errors', 'home'):
        module = import_module(f'app.{module_name}.routes')
        app.register_blueprint(module.blueprint)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    register_extensions(app)
    register_blueprints(app)

    return app
