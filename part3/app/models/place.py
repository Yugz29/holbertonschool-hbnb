from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.extensions import db


class Place(BaseModel):
    """Class representing a Place entity"""
    __tablename__ = 'places'

    """Columns"""
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def add_review(self, review):
        """Add a review instance to the place"""
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity instance to the place"""
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance")
        self.amenities.append(amenity)

    def update(self, data: dict):
        """Update Place attributes from a dictionary"""
        for key, value in data.items():
            if key == 'price':
                if value < 0:
                    raise ValueError("price must be more than 0")
            elif key == 'latitude':
                if not (-90.0 <= value <= 90.0):
                    raise ValueError("latitude must be between -90.0 and 90.0")
            elif key == 'longitude':
                if not (-180.0 <= value <= 180.0):
                    raise ValueError("longitude must be between -180.0 and 180.0")
            elif key == 'title':
                if not isinstance(value, str):
                    raise TypeError("title must be a string")
                if len(value) >= 100:
                   raise ValueError("title must be less or equal to 100 characters")
            elif key == 'owner':
                if value is not None and not isinstance(value, User):
                    raise TypeError("owner must be a User instance")
                
            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

    def to_dict(self):
        """Return a dictionary representation of Place"""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id if self.owner else None,
            "reviews": [review.id for review in self.reviews],
            "amenities": [amenity.id for amenity in self.amenities]
        })
        return base_dict
