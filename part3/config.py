import os
from pathlib import Path

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'une_clé_secrète_par_défaut_123!')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Chemin ABSOLU vers part3/sql/hbnb.db
    BASE_DIR = Path(__file__).resolve().parent  # ← Racine de part3/
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/sql/hbnb.db'  # ← Chemin correct
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://user:password@localhost/hbnb_db"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}