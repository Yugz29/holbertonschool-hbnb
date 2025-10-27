from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        data_review = api.payload or {}
        text = data_review.get('text')
        rating = data_review.get('rating')
        user_id = data_review.get('user_id')
        place_id = data_review.get('place_id')

        if not text or not isinstance(text, str):
            return {'error': 'Text is required'}, 400
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400
        if not user_id:
            return {'error': 'User ID is required'}, 400
        if not place_id:
            return {'error': 'Place ID is required'}, 400
        
        new_review = facade.create_review({
            'text': text,
            'rating': rating,
            'user_id': user_id,
            'place_id': place_id
        })

        if not new_review:
            user = facade.get_user(user_id)
            place = facade.get_place(place_id)
            if not user:
                return {'error': 'User not found'}, 400
            if not place:
                return {'error': 'Place not found'}, 400
            return {'error': 'Could not create review'}, 400
        
        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id, 
            'place_id': review.place_id
            }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        data_review = api.payload or {}
        text = data_review.get('text')
        rating = data_review.get('rating')

        if 'text' in data_review and (not text or not isinstance(text, str)):
            return {'error': 'Text is required'}, 400
        if 'rating' in data_review and (not isinstance(rating, int) or not (1 <= rating <= 5)):
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        updated_review = facade.update_review(review_id, data_review)
        if not updated_review:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            return {'error': 'Invalid input data'}, 400
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        place_reviews = facade.get_reviews_by_place(place_id)
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating
        }
        for review in place_reviews
        ], 200
