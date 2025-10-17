from app.models.place import Place
from app.models.user import User
from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self._text = self.string_validation(text, "text")
        self._rating = self.rating_validation(rating)
        self._place_id = self.place_validation(place)
        self._user_id = self.user_validation(user)

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = self.string_validation(value, "text")

    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, value):
        self._rating = self.rating_validation(value)

    @property
    def user_id(self):
        return getattr(self._user_id, "id", None)

    @property
    def place_id(self):
        return getattr(self._place_id, "id", None)

    @staticmethod
    def string_validation(value, field_name, max_length=100):
        """Verify text requirements"""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be less than {max_length} characters")
        return value

    @staticmethod
    def rating_validation(rating):
        """Verify rating requirements"""
        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating <= 0 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
        return rating

    @staticmethod
    def place_validation(place):
        """Verify if place exists"""
        if not isinstance(place, Place):
            raise TypeError(f"place must be a Place instance")
        return place

    @staticmethod
    def user_validation(user):
        """Verify if user exists"""
        if not isinstance(user, User):
            raise TypeError(f"user must be a User instance")
        return user
    
    def to_dict(self):
        """Return a dictionary representation"""
        base_dict = super().to_dict()
        base_dict.update({
            "text": self._text,
            "rating": self._rating,
            "place": self._place.to_dict() if hasattr(self._place, "to_dict") else str(self._place),
            "user": self._user.to_dict() if hasattr(self._user, "to_dict") else str(self._user)
        })
        return base_dict
