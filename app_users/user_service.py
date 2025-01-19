from uuid import UUID

from core.BASE_unit_of_work import UnitOfWork

from app_users.models import User


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_user_info(self, user_id: UUID) -> User | None:
        """
        Получает полную информацию о пользователе по user_id.

        Args:
            user_id (UUID): Идентификатор пользователя.

        Returns:
            Optional[User]: Объект пользователя с загруженными связями или None, если не найден.
        """
        async with self.uow as uow:
            user = await uow.user.get_user_by_id(user_id)
            return user
