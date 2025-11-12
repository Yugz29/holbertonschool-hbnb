from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('', strict_slashes=False)
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        if not current_user or not getattr(current_user, 'is_admin', False):
            return {'error': 'Admin privilege required'}, 403
        
        user_data = api.payload
        try:
            if facade.get_user_by_email(user_data.get('email')):
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        
    def get(self):
        """Retrive the list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200

@api.route('/<string:user_id>', strict_slashes=False)
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            if user is None:
                return {'error': 'User not found'}, 404
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        if not current_user or not getattr(current_user, 'is_admin', False):
            return {'error': 'Admin privilege required'}, 403
        
        user_data = api.payload.copy()

        user_data.pop('email', None)
        user_data.pop('password', None)

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
    
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        if not current_user or not getattr(current_user, 'is_admin', False):
            return {'error': 'Admin privilege required'}, 403
        
        deleted = facade.delete_user(user_id)
        if not deleted:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted'}, 200
