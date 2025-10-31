from app.extensions import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from app.models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    """Columns"""
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places_id = db.Column(db.String, db.ForeignKey('places.id'), nullable=False)
    reviews_id = db.Column(db.String, db.ForeignKey('reviews.id'), nullable=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self._first_name = self.string_validation(first_name, "first_name")
        self._last_name = self.string_validation(last_name, "last_name")
        self._email = self.email_validation(email)
        self._is_admin = bool(is_admin)
        self._set_password(password)

    """Validation Methods"""
    @staticmethod
    def string_validation(value, field_name, max_length=50):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be less than {max_length} \
                                characters")
        return value

    @staticmethod
    def email_validation(email):
        """Verify email requirements"""
        if not isinstance(email, str):
            raise TypeError("email must be a string")
        if not email:
            raise ValueError("email is required")
        if "@" not in email:
            raise ValueError("email must be a valid email address")
        return email

    """Properties"""
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self.string_validation(value, "first_name")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self.string_validation(value, "last_name")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self.email_validation(value)

    @property
    def is_admin(self):
        return self._is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = bool(value)

    """Password Methods"""  
    def _set_password(self, password): # to confirm
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    """Dictonary representation"""
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email,
            "is_admin": self._is_admin
        })
        return base_dict

    def __repr__(self):
        return f"<User {self._first_name} {self._last_name} ({self._email})>"