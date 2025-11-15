from flask import Flask, render_template
from flask_cors import CORS
from flask_restx import Api
from app.extensions import db, bcrypt, jwt
import config


def create_app(config_class=config.DevelopmentConfig):
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    @app.route("/login")
    def login_page():
        return render_template("login.html")
    
    @app.route("/index")
    def index_page():
        return render_template("index.html")
    
    return app
