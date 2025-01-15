from core.BASE_repository import SQLAlchemyRepository

from app_jwt.models import JWToken


class JWTokenRepository(SQLAlchemyRepository):
    model = JWToken
