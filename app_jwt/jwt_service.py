from uuid import UUID
from typing import Any, Dict

from core.BASE_unit_of_work import IUnitOfWork

from app_jwt.utils import jwt_util

from app_jwt.schemas import JWTSchema


class JWTService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
        self.jwt_util = jwt_util

    async def create_and_store_token(
        self, user_id: UUID, **kwargs: Any
    ) -> Dict[str, JWTSchema]:
        """
        Генерирует 2 токена (ACCESS, REFRESH) из переданных данных,
        сохраняет их в БД и возвращает словарь вида:
        {
            "access": JWTSchema(...),
            "refresh": JWTSchema(...),
        }
        где каждый JWTSchema содержит (token, expires_at, user_id, token_type, и т.д.).
        """

        # Подготавливаем payload для access-токена
        # Например, передаём user_id, type="ACCESS", а также любые другие поля из kwargs
        payload_access = dict(kwargs)
        payload_access["user_id"] = str(user_id)  # encode_jwt ждёт строку
        payload_access["type"] = self.jwt_util.access_token_type

        # Аналогично для refresh-токена
        payload_refresh = dict(kwargs)
        payload_refresh["user_id"] = str(user_id)
        payload_refresh["type"] = self.jwt_util.refresh_token_type

        # 1. Генерируем оба токена (JWTSchema) через JWTUtil
        access_token_schema: JWTSchema = self.jwt_util.encode_jwt(payload_access)
        refresh_token_schema: JWTSchema = self.jwt_util.encode_jwt(payload_refresh)

        # 2. Сохраняем в БД
        async with self.uow as uow:
            # Сохраняем ACCESS-токен
            await uow.jwt.create_obj(
                user_id=access_token_schema.user_id,
                token=access_token_schema.token,
                token_type=access_token_schema.token_type,  # Enum TokenTypeEnum.ACCESS
                expires_at=access_token_schema.expires_at,
                issued_at=access_token_schema.issued_at,
                revoked=False,
            )

            # Сохраняем REFRESH-токен
            await uow.jwt.create_obj(
                user_id=refresh_token_schema.user_id,
                token=refresh_token_schema.token,
                token_type=refresh_token_schema.token_type,  # Enum TokenTypeEnum.REFRESH
                expires_at=refresh_token_schema.expires_at,
                issued_at=refresh_token_schema.issued_at,
                revoked=False,
            )

            # Фиксируем изменения одной транзакцией
            await uow.commit()

        # 3. Возвращаем оба токена
        return {
            "access": access_token_schema,
            "refresh": refresh_token_schema,
        }

    async def create_and_store_access(
        self,
        **kwargs,
    ):
        payload_access = dict(kwargs)
        access_token_schema: JWTSchema = self.jwt_util.encode_jwt(payload_access)

        async with self.uow as uow:
            # Сохраняем ACCESS-токен
            await uow.jwt.create_obj(
                user_id=access_token_schema.user_id,
                token=access_token_schema.token,
                token_type=access_token_schema.token_type,  # Enum TokenTypeEnum.ACCESS
                expires_at=access_token_schema.expires_at,
                issued_at=access_token_schema.issued_at,
                revoked=False,
            )
            await uow.commit()

        return {
            "access": access_token_schema,
        }
