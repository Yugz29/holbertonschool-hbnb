import uuid
from datetime import datetime


class BaseModel:
    """Base class for all entities with shared attributes and methods."""

    def __init__(self):
        """Initialize common attributes."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the 'updated_at' timestamp when the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data: dict):
        """Update object attributes from a dictionary of values."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # refresh updated_at

    def to_dict(self):
        """Convert the object to a dictionary representation."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
