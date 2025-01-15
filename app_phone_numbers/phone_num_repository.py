from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.BASE_repository import SQLAlchemyRepository

from app_phone_numbers.models import PhoneNumber


class PhoneNumberRepository(SQLAlchemyRepository):
    model = PhoneNumber

    async def get_obj_with_user(self, phone_number: str) -> None | PhoneNumber:
        """
        Метод, который подгружает и PhoneNumber, и связанного пользователя.
        """
        stmt = (
            select(PhoneNumber)
            .where(PhoneNumber.phone_number == phone_number)
            .options(joinedload(PhoneNumber.user))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
