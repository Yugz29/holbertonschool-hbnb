from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Class representing a Place entity"""

    def __init__(self, title, description="", price=0.0, latitude=0.0,
                 longitude=0.0, owner=None):
        super().__init__()
        self.description = description
        self._price = price
        self._latitude = latitude
        self._longitude = longitude
        self._title = title
        self._owner = owner
        self.owner_id = owner.id if owner else None
        self.reviews = []
        self.amenities = []


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if len(value) > 100:
            raise ValueError("Title too long")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if value is not None and not isinstance(value, User):
            raise TypeError("Owner must be a User")
        self._owner = value

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
