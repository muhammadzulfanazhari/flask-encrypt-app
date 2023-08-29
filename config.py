from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """Base configuration."""
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    ADMINS = ['muhammadzulfanazhari@gmail.com']


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    #     path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_DATABASE_URI = 'postgres://fhzdbzskqfjbih:acf38aa23207c262d14058c034099c98a3508b79d5c0867e79b6749f023fd15a@ec2-44-213-228-107.compute-1.amazonaws.com:5432/depdancdg96nmn'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # PostgreSQL or MySQL Database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.\
        format(
            environ.get('DB_ENGINE'),
            environ.get('DB_USERNAME'),
            environ.get('DB_PASSWORD'),
            environ.get('DB_HOST'),
            environ.get('DB_PORT'),
            environ.get('DB_NAME'))
