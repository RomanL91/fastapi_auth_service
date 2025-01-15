from core.BASE_repository import SQLAlchemyRepository

from app_social_account.models import SocialAccount


class SocialAccountRepository(SQLAlchemyRepository):
    model = SocialAccount
