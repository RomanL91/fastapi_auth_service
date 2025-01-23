from uuid import UUID

from sqlalchemy.engine import Result
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from core.BASE_repository import SQLAlchemyRepository

from app_users.models import User, UserAddress


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
                selectinload(self.model.phone),  # Загрузка связи PhoneNumber
                selectinload(
                    self.model.social_accounts
                ),  # Загрузка связи SocialAccount
                selectinload(self.model.addresses),
                # selectinload(self.model.points_balances),
                # selectinload(User.tokens),  # Загрузка связи JWToken
                # selectinload(User.sms_codes),  # Загрузка связи SMSCode
            )
            .where(User.id == user_id)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def update_user(self, obj_id: str, **data) -> User | None:

        stmt = (
            update(self.model)
            .options(
                selectinload(self.model.phone),  # Загрузка связи PhoneNumber
                selectinload(self.model.social_accounts),
                selectinload(self.model.addresses),
                selectinload(self.model.points_balances),
            )
            .values(**data)
            .filter_by(id=obj_id)
            .returning(self.model)
        )
        res: Result = await self.session.execute(stmt)
        updated_obj = res.scalar_one_or_none()
        if updated_obj is None:
            raise ValueError(f"Object with id={obj_id} not found")
        return updated_obj


class UserAddressRepository(SQLAlchemyRepository):
    model = UserAddress
