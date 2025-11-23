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
        """Return a dictionary representation without recursion"""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "place_id": self.place_id,
            "user_name": self.user.first_name if self.user else "Anonymous",
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
