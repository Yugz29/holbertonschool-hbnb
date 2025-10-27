from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Class representing an Amenity entity"""

    def __init__(self, name):
        super().__init__()
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name.strip():
            raise ValueError("name cannot be empty")
        if len(name) > 50:
            raise ValueError("name cannot exceed 50 characters")
        self.name = name

    def to_dict(self):
        """Return a dictionary representation of Amenity"""
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name
        })
        return base_dict
