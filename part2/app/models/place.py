from app.models.base_model import BaseModel
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class Place(BaseModel):
    """Class representing a Place entity"""

    def __init__(self, title, description="", price=0.0, latitude=0.0,
                 longitude=0.0, owner=None):
        super().__init__()
        self.description = description

        if price < 0:
            raise ValueError("price must be more than 0")
        self.price = price

        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        self.latitude = latitude
        self.longitude = longitude

        if len(title) >= 100:
            raise ValueError("title must be less or equal to 100 characters")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        self.title = title

        if owner is not None and not isinstance(owner, User):
            raise TypeError("owner must be a User instance")
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review instance to the place"""
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
