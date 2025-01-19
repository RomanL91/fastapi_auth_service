from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.BASE_repository import SQLAlchemyRepository

from app_users.models import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """
        Получает пользователя по user_id с загруженными связями.

        Args:
            user_id (UUID): Идентификатор пользователя.

        Returns:
            User | None: Объект пользователя с загруженными связями или None, если не найден.
        """
        stmt = (
            select(User)
            .options(
                selectinload(User.phone),  # Загрузка связи PhoneNumber
                selectinload(User.social_accounts),  # Загрузка связи SocialAccount
                # selectinload(User.tokens),  # Загрузка связи JWToken
                # selectinload(User.sms_codes),  # Загрузка связи SMSCode
            )
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user
