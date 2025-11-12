from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privilege required')
    def post(self):
        """Register a new amenity"""
        identity = get_jwt_identity()
        if not identity or not identity.get('is_admin', False):
            return {'error': 'Admin privilege required'}, 403
        amenity_data = api.payload or {}
        name = amenity_data.get('name', '').strip()
        
        if not name:
            return {'error': 'Invalid input data'}, 400
        new_amenity = facade.create_amenity({'name': name})

        if not new_amenity:
            return {'error': 'Invalid input data'}, 400
        return new_amenity.to_dict(), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privilege required')
    def put(self, amenity_id):
        """Update an amenity's information"""
        identity = get_jwt_identity()
        if not identity or not identity.get('is_admin', False):
            return {'error': 'Admin privilege required'},403
        amenity_data = api.payload or {}
        name = amenity_data.get('name', '').strip()
        
        if not name:
            return {'error': 'Invalid input data'}, 400

        updated_amenity = facade.update_amenity(amenity_id, {'name': name})
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        
        return updated_amenity.to_dict(), 200
    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privilege required')
    def delete(self, amenity_id):
        identity = get_jwt_identity()
        if not identity or not identity.get('is_admin', False):
            return {'error': 'Admin privilege required'}, 403
        amenity = facade.delete_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'message': 'Amenity deleted'}, 200
