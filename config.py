# -*- encoding: utf-8 -*-
import os
from decouple import config

# base config
class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default=os.environ['SECRET_KEY'])

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# production child config
class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    # SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
    #     config('DB_ENGINE'  , default='postgresql'    ),
    #     config('DB_USERNAME', default='df'       ),
    #     config('DB_PASS'    , default='pass'          ),
    #     config('DB_HOST'    , default='localhost'     ),
    #     config('DB_PORT'    , default=5432            ),
    #     config('DB_NAME'    , default='appseed-flask' )
    # )

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


# Debug child config
class DebugConfig(Config):
    DEBUG = True


# return configuration classes
config_dict = {
    'Production': ProductionConfig,
    'Debug' : DebugConfig
}
