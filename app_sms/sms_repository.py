from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from core.BASE_repository import SQLAlchemyRepository

from app_sms.models import SMSCode
from app_users.models import User
from app_phone_numbers.models import PhoneNumber


class SMSCodeRepository(SQLAlchemyRepository):
    model = SMSCode

    async def get_unused_code_for_phone(
        self,
        code: str,
        phone_id: UUID,
    ) -> None | SMSCode:
        """
        Получить SMSCode по указанному коду, где is_used=False
        и пользователь связан с phone.id = phone_id.
        Возвращает SMSCode или None, если не найдено.
        """
        stmt = (
            select(SMSCode)
            .join(SMSCode.user)  # Присоединяем таблицу User
            .join(User.phone)  # Присоединяем таблицу PhoneNumber
            .where(SMSCode.code == code)
            .where(SMSCode.is_used.is_(False))
            .where(SMSCode.expires_at > func.now())  # проверка неистёкшего срока
            .where(PhoneNumber.id == phone_id)
            .options(joinedload(SMSCode.user))  # Если нужно подгрузить user
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
