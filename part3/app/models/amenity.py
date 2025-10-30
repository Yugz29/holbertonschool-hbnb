from app.models.base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    """Column"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """Return a dictionary representation of Amenity"""
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name
        })
        return base_dict
