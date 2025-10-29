from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from app.models.base_model import BaseModel
from app import db, bcrypt


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    """Column"""
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    """Validations"""
    @validates('first_name')
    def validate_first_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("first_name must be a string")
        if not value:
            raise ValueError("first_name is required")
        if len(value) > 50:
            raise ValueError("first_name must be less than 50 characters")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("last_name must be a string")
        if not value:
            raise ValueError("last_name is required")
        if len(value) > 50:
            raise ValueError("last_name must be less than 50 characters")
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("email must be a string")
        if not value:
            raise ValueError("email is required")
        if "@" not in value:
            raise ValueError("email must be a valid email address")
        return value

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        })
        return base_dict

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.email})>"
