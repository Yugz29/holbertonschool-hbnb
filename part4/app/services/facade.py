from sqlalchemy.orm import joinedload
from app.persistence.repositories.user_repository import UserRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()        
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    """user methods"""
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all() 
    
    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)
    
    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return None
        self.user_repo.delete(user.id)
        return user

    """amenity methods"""
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return amenity

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)
    
    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.delete(amenity_id)
        return amenity

    """place methods"""
    def create_place(self, place_data):
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place_data['owner'] = owner
            del place_data['owner_id']

        amenities_ids = place_data.pop("amenities", [])
        place = Place(**place_data)
        self.place_repo.add(place)

        for aid in amenities_ids:
            amenity = self.get_amenity(aid)
            if amenity:
                place.add_amenity(amenity)

        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        place.owner = self.user_repo.get(place.owner_id)
        place.amenities = [self.amenity_repo.get(aid) for aid in getattr(place, 'amenity_ids', [])]
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        for place in places:
            place.owner = self.user_repo.get(place.owner_id)
            place.amenities = [self.amenity_repo.get(aid) for aid in getattr(place, 'amenity_ids', [])]
        return places

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place_data['owner'] = owner
            del place_data['owner_id']

        if 'amenities' in place_data:
            valid_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} does not exist")
                valid_amenities.append(amenity)
            place_data['amenities'] = valid_amenities

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)
    
    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    """review methods"""
    def create_review(self, review_data):
       text = review_data.get('text')
       rating = review_data.get('rating')
       user_id = review_data.get('user_id')
       place_id = review_data.get('place_id')

       if not text or not isinstance(text, str):
           return None
       if not isinstance(rating, int) or not (1 <= rating <= 5):
           return None
       if not user_id or not place_id:
           return None
       
       user = self.get_user(user_id)
       place = self.get_place(place_id)
       if not user:
           raise ValueError("User not found")
       if not place:
           raise ValueError("Place not found")
       
       review = Review(text=text, rating=rating, place=place, user=user)
       self.review_repo.add(review)
       return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return (
            Review.query
            .filter_by(place_id=place_id)
            .options(joinedload(Review.user))
            .all()
        )

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")

        if 'user_id' in review_data:
            user = self.get_user(review_data['user_id'])
            if not user:
                raise ValueError("User not found")
            review_data['user']= user
            del review_data['user_id']

        if 'place_id' in review_data:
            place = self.get_place(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            review_data['place'] = place
            del review_data['place_id']
        
        if 'text' in review_data:
            text = review_data['text']
            if not text or not isinstance(text, str):
                raise ValueError("Text is required")
        
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review

    def user_has_reviewed_place(self, user_id, place_id):
        """Return True if the user has already reviewed the given place"""
        reviews = self.review_repo.get_all()
        return any(r.user_id == user_id and r.place_id == place_id for r in reviews)