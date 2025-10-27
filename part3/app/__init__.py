from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    return app
