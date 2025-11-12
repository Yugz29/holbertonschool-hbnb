from app.models.base_model import BaseModel
from app.extensions import db


class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    """Columns"""
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    """Relationship"""
    user = db.relationship('User', back_populates='reviews')
    place = db.relationship('Place', back_populates='reviews')
    
    def to_dict(self):
        """Return a dictionary representation"""
        base_dict = super().to_dict()
        base_dict.update({
            "text": self.text,
            "rating": self.rating,
            "place": self.place.to_dict() if self.place else self.place_id,
            "user": self.user.to_dict() if self.user else self.user_id
        })
        return base_dict
