import os

import aiofiles

from uuid import UUID

from fastapi import Request, UploadFile, HTTPException, status

from core.settings import settings
from core.BASE_unit_of_work import UnitOfWork

from app_users.models import User

from app_users.schemas import UserUpdateSchema, UserSchema


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

    async def update_user_info(
        self, user_id: UUID, user_update: UserUpdateSchema
    ) -> User | None:
        """
        Обновляет информацию о пользователе.

        Args:
            user_id (UUID): Идентификатор пользователя.
            user_update (UserUpdateSchema): Данные для обновления.

        Returns:
            Optional[User]: Обновлённый объект пользователя или None, если не найден.
        """
        update_data = user_update.model_dump(exclude_unset=True)
        async with self.uow as uow:
            try:
                updated_user = await uow.user.update_user(str(user_id), **update_data)
                await uow.commit()
                return updated_user
            except ValueError as ve:
                raise ve

    async def payload_avatar(
        self, unique_name: str, request: Request, file: UploadFile
    ) -> User | None:
        avatar_url = str(request.url_for("avatars", path=unique_name))
        file_path = os.path.join(settings.avatar_directory, unique_name)
        # Валидация типа файла (например, только изображения)
        if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only JPEG, PNG, and GIF are allowed.",
            )
        try:
            # Асинхронная запись файла
            async with aiofiles.open(file_path, "wb") as buffer:
                content = await file.read()
                await buffer.write(content)
            # Обновление avatar_path пользователя
            async with self.uow as uow:
                updated_user = await uow.user.update_user(
                    unique_name, avatar_path=avatar_url
                )
                await uow.commit()
                return UserSchema.model_validate(updated_user)
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload avatar. \n -> {e}",
            )
