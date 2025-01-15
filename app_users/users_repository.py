from core.BASE_repository import SQLAlchemyRepository

from app_users.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
