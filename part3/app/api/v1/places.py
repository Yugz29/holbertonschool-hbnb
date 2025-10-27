from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return {'error': 'Invalid input data'}, 400
        
        data['owner_id'] = current_user_id
        
        amenities_ids = data.get('amenities', [])
        valid_amenities = []
        for amenity_id in amenities_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': f"amenity with ID {amenity_id} does not exist"}, 400
            valid_amenities.append(amenity)
        data['amenities'] = valid_amenities

        try:
            new_place = facade.create_place(data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        places_dicts = [place.to_dict() for place in places]
        return {'places': places_dicts}, 200

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user_id = get_jwt_identity()
        data = request.get_json()

        lat = data.get('latitude')
        lng = data.get('longitude')

        if lat is None or not (-90 <= lat <= 90):
            return {'error': 'Latitude must be between -90 and 90'}, 400
        if lng is None or not (-180 <= lng <= 180):
           return {'error': 'Longitude must be between -180 and 180'}, 400

        if not data:
            return {'error': 'Invalid input data'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        if 'owner_id' in data:
            del data['owner_id']
        
        amenities_ids = data.get('amenities')
        if amenities_ids is None or not amenities_ids:
            return {'error': 'Amenities list is required'}, 400
        
        valid_amenities = []
        for amenity_id in amenities_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': f"amenity with ID {amenity_id} does not exist"}, 400
            valid_amenities.append(amenity)

        data['amenities'] = valid_amenities
        
        if 'title' in data and not isinstance(data['title'], str):
            return {'error': 'title must be a string'}, 400
        if 'price' in data and data['price'] <= 0:
            return {'error': 'price must be positive'}, 400

        try:
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return updated_place.to_dict(), 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200
