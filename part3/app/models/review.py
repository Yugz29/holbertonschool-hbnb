from app.models.base_model import BaseModel
from app.extensions import db


class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    """Columns"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Interger, nullable=False)
    place_id = db.Column(db.String, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        """Return a dictionary representation"""
        base_dict = super().to_dict()
        base_dict.update({
            "text": self._text,
            "rating": self._rating,
            "place": self._place.to_dict() if hasattr(self._place, "to_dict") else str(self._place),
            "user": self._user.to_dict() if hasattr(self._user, "to_dict") else str(self._user)
        })
        return base_dict
