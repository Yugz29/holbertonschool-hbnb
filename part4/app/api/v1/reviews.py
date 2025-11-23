from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        if isinstance(current_user, dict):
            current_user_id = current_user.get('id')
        else:
            current_user_id = current_user

        data_review = api.payload or {}
        text = data_review.get('text')
        rating = data_review.get('rating')
        place_id = data_review.get('place_id')

        if not text or not isinstance(text, str) or text.strip() == "":
            return {'error': 'Text is required'}, 400
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400
        if not place_id:
            return {'error': 'Place ID is required'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 403

        if facade.user_has_reviewed_place(current_user_id, place.id):
            return {'error': 'You have already reviewed this place'}, 409

        new_review = facade.create_review({
            'text': text,
            'rating': rating,
            'user_id': current_user_id,
            'place_id': place_id
        })

        if not new_review:
            return {'error': 'Could not create review'}, 400

        user_name = f"{new_review.user.first_name} {new_review.user.last_name}" if new_review.user else "Anonymous"

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'user_name': user_name,
            'place_id': new_review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        result = []
        for review in reviews:
            user = facade.get_user(review.user_id)
            user_id = review.user_id
            user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"
            result.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': user_id,
                'user_name': user_name,
                'place_id': review.place_id
            })
        return result, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        user = facade.get_user(review.user_id)
        user_id = review.user_id
        user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': user_id,
            'user_name': user_name,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        current_user_id = current_user.get('id') if isinstance(current_user, dict) else current_user
        is_admin = current_user.get('is_admin', False) if isinstance(current_user, dict) else False
        data_review = api.payload or {}

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        if 'text' in data_review and (not data_review['text'] or not isinstance(data_review['text'], str)):
            return {'error': 'Text is required'}, 400
        if 'rating' in data_review and (not isinstance(data_review['rating'], int) or not (1 <= data_review['rating'] <= 5)):
            return {'error': 'Rating must be between 1 and 5'}, 400

        if 'user_id' in data_review:
            data_review.pop('user_id')

        updated_review = facade.update_review(review_id, data_review)
        if not updated_review:
            return {'error': 'Invalid input data'}, 400
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        current_user_id = current_user.get('id') if isinstance(current_user, dict) else current_user
        is_admin = current_user.get('is_admin', False) if isinstance(current_user, dict) else False

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            # Always return a list, even if place not found
            return [], 200

        place_reviews = facade.get_reviews_by_place(place_id)
        result = []
        for review in place_reviews:
            user = facade.get_user(review.user_id)
            user_id = review.user_id
            user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"
            result.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': user_id,
                'user_name': user_name,
                'place_id': review.place_id
            })
        return result, 200
