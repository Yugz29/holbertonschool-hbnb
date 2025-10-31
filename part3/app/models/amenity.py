from app.models.base_model import BaseModel
from app.extensions import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


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
