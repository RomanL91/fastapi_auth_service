import jwt
import uuid

from typing import TYPE_CHECKING

from datetime import datetime, timedelta, timezone

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# == Exceptions
from fastapi import HTTPException, status

# == Core
from core.settings import SettingsAuth

if TYPE_CHECKING:
    # == Schema
    from app_jwt.schemas import JWTSchema


class JWTUtil:
    def __init__(self, settings: SettingsAuth):
        # super() ?? TODO
        self.private_key = settings.private_key_path.read_text()
        self.public_key = settings.public_key_path.read_text()
        self.algorithm = settings.algorithm
        self.access_token_expire = settings.access_token_expire
        self.refresh_token_expire = settings.refresh_token_expire
        self.timezone = settings.timezone
        self.token_type = settings.token_type
        self.token_type_field = settings.token_type_field
        self.access_token_type = settings.access_token_type
        self.refresh_token_type = settings.refresh_token_type

    def encode_jwt(self, payload: dict) -> "JWTSchema":
        # now = datetime.now(self.timezone)
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        expire = now + timedelta(minutes=self.access_token_expire)
        if self.refresh_token_type in payload.values():
            expire = now + timedelta(minutes=self.refresh_token_expire)
        payload.update(exp=expire, iat=now)
        token_value = jwt.encode(
            payload=payload, key=self.private_key, algorithm=self.algorithm
        )
        from app_jwt.schemas import JWTSchema  # Локальный импорт TODO эт конечно п..ц.

        token = JWTSchema(
            user_id=self.convet_str_to_uuid(payload.get("user_id")),
            issued_at=now,
            expires_at=expire,
            token_type=payload.get("type", "unknown"),
            token=token_value,
        )
        return token

    def decode_jwt(self, jwt_key: str) -> dict:
        # TODO Пересмотреть обработку исключений
        # return jwt.decode(jwt_key, key=self.public_key, algorithms=[self.algorithm])
        try:
            return jwt.decode(jwt_key, key=self.public_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired."
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
        except Exception as e:
            # Для любых других JWT ошибок
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token."
            )

    def convet_str_to_uuid(self, user_id: str):
        return uuid.UUID(user_id)


jwt_util = JWTUtil(settings=SettingsAuth())


class JWTBearer(HTTPBearer):
    def __init__(self, expected_token_type: str, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.expected_token_type = expected_token_type

    async def __call__(self, request: Request) -> str | None:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if credentials.scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            payload_data = self.verify_jwt(credentials.credentials)
            return payload_data
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )

    def verify_jwt(self, jwtoken: str) -> dict:
        try:
            payload_data = jwt_util.decode_jwt(jwtoken)
        except HTTPException as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=e.detail,
            )
        if payload_data.get("type") == self.expected_token_type:
            return payload_data
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type.",
        )
