from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

from core.BASE_repository import SQLAlchemyRepository

from app_social_account.models import SocialAccount


class SocialAccountRepository(SQLAlchemyRepository):
    model = SocialAccount

    async def get_obj(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by).limit(1)
        try:
            res: Result = await self.session.execute(stmt)
            return res.scalar_one()
        except NoResultFound:
            return None
