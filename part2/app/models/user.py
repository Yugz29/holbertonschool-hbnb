from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self._first_name = self.string_validation(first_name, "first_name")
        self._last_name = self.string_validation(last_name, "last_name")
        self._email = self.email_validation(email)
        self._is_admin = is_admin

    @staticmethod
    def string_validation(value, field_name, max_length=50):
        """Verify first_name / last_name requirements"""
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be less than {max_length} \
                                characters")
        return value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = self.string_validation(value, "first_name")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = self.string_validation(value, "last_name")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = self.email_validation(value)

    @staticmethod
    def email_validation(email):
        """Verify email requirements"""
        if not isinstance(email, str):
            raise TypeError("email must be a string")
        if not email:
            raise ValueError("email is required")
        if "@" not in email:
            raise ValueError("email must be a valid email address")
        return email

    def to_dict(self):
        """Return a dictionary representation of User"""
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email,
            "is_admin": self._is_admin
        })
        return base_dict

    def __repr__(self):
        return f"<User {self._first_name} {self._last_name} ({self._email})>"