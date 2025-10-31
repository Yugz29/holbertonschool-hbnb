from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.extensions import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    """Columns"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    reviews_id = db.Column(db.String, db.ForeignKey('reviews.id'), nullable=False)
    amenities_id = db.Column(db.String, db.ForeignKey('amenities.id'), nullable=False)


    def to_dict(self):
        """Return a dictionary representation of Place"""
        base_dict = super().to_dict()
        base_dict.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
        })
        return base_dict
