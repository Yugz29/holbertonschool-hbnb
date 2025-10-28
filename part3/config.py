import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/hbnb_db"

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}