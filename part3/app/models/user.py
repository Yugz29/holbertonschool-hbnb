from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base_model import BaseModel


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    """Columns"""
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    """Relationships"""
    places = db.relationship('Place', back_populates='user', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)
    
    """Simple methods"""  
    def hash_password(self, password): # to confirm
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    """Dictonary representation"""
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