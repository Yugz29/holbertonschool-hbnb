from app.models.base_model import BaseModel
from app.extensions import db
from app.models.associations import place_amenity
from app.models.user import User
from app.models.review import Review
from app.models.amenity import Amenity


class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    """Columns"""
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    """Relationships"""
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery', back_populates='places')

    def to_dict(self):
        """Return a dictionary representation of Place"""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [amenity.to_dict() for amenity in self.amenities],
        })
        return base_dict
