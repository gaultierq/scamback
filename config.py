import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'gHHGtsd65JJ_=~5565TT'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://samback:samback@localhost/samback'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://atanasster:scamback@atanasster.mysql.pythonanywhere-services.com/samback'



class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True