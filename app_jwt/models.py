from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy.sql import func
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.BASE_model import Base  # Базовая модель


class TokenTypeEnum(str, PyEnum):
    """Тип токена"""

    ACCESS = "access_token"
    REFRESH = "refresh_token"


class JWToken(Base):
    """Модель JWT токенов"""

    user_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )  # Связь с пользователем, может быть NULL
    issued_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False,
    )  # Время выпуска токена
    expires_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )  # Время истечения токена
    token_type: Mapped[TokenTypeEnum] = mapped_column(
        Enum(TokenTypeEnum),
        nullable=False,
    )  # Тип токена (ACCESS/REFRESH)
    token: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )  # Токен в виде строки
    revoked: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )  # Флаг отзыва токена

    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="tokens",
    )
