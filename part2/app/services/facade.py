from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place



class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    """user methods"""
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    """amenity methods"""
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    """place methods"""
    def create_place(self, place_data):
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            place_data['owner'] = owner
            del place_data['owner_id']

        amenities = place_data.pop("amenities", [])

        place = Place(**place_data)
        self.place_repo.add(place)

        for name in amenities:
            amenity = self.amenity_repo.get_by_attribute('name', name)
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
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

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
       if not user or not place:
           return None
       
       review = Review(text, rating, place, user)
       self.review_repo.add(review)
       return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        all_reviews = self.get_all_reviews()
        matching_reviews = []
        for review in all_reviews:
            if review.place_id == place_id:
                matching_reviews.append(review)
        return matching_reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None
        
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return None

        if 'user_id' in review_data and not self.get_user(review_data['user_id']):
            return None
        if 'place_id' in review_data and not self.get_place(review_data['place_id']):
            return None
        
        if 'text' in review_data:
            text = review_data['text']
            if not text or not isinstance(text, str):
                return None
        
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
