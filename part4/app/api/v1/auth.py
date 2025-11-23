from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from flask_jwt_extended import decode_token


api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Verify that user.id is valid
        if not getattr(user, 'id', None):
            return {'error': 'User ID is invalid'}, 500

        # Step 3: Create a JWT token with only the user id as identity
        access_token = create_access_token(identity=user.id)
        print(access_token)

        if not access_token:
            return {'error': 'Failed to generate JWT'}, 500

        from flask import make_response
        # Step 4: Return the JWT token in a secure cookie accessible by JS
        response = make_response({'message': 'Login successful'}, 200)
        response.set_cookie(
            'token',
            access_token,
            httponly=False,    # JS peut lire le cookie
            samesite='Lax',   # protège contre certaines attaques CSRF
            path='/',         # disponible sur toutes les routes
            max_age=3600      # durée de validité en secondes (1h)
        )

        print("Login successful: user.id =", user.id, "access_token =", access_token)

        return response
    
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
         """A protected endpoint that requires a valid JWT token"""
         print("jwt------")
         print(get_jwt_identity())
         current_user = get_jwt_identity() # Retrieve the user's identity from the token
         #if you need to see if the user is an admin or not, you can access additional claims using get_jwt() :
         # addtional claims = get_jwt()
         #additional claims["is_admin"] -> True or False
         return {'message': f'Hello, user {current_user}'}, 200

@api.route('/check')
class AuthCheck(Resource):
    def get(self):
        """Check if the user is authenticated based on the JWT token cookie"""
        token = request.cookies.get('token')
        if not token:
            return jsonify({"authenticated": False})
        try:
            decode_token(token)  # Vérifie la validité du JWT
            return jsonify({"authenticated": True})
        except Exception:
            return jsonify({"authenticated": False})
