from app.models.base_model import BaseModel
from app.extensions import db
from app.models.associations import place_amenity

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenities'

    """Column"""
    name = db.Column(db.String(50), nullable=False)

    places = db.relationship(
    'Place',
    secondary=place_amenity,
    lazy='subquery',
    backref=db.backref('amenities', lazy=True)
    )
    
    def to_dict(self):
        """Return a dictionary representation of Amenity"""
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "places": [place.id for place in self.places]
        })
        return base_dict
