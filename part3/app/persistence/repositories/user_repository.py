from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """Repository spécifique aux utilisateurs."""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retourne un utilisateur via son adresse email."""
        return self.model.query.filter_by(email=email).first()