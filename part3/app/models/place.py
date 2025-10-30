from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity
from app.extensions import db


class Place(BaseModel):
    __tablename__ = 'places'

    """Columns"""
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


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
