from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """Base class for all entities with shared attributes and methods."""
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    """Columns"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the 'updated_at' timestamp when the object is modified and save to the database."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update_from_dict(self, data: dict):
        """Update object attributes from a dictionary of values and commit changes."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def to_dict(self):
        """Convert the object to a dictionary representation."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
