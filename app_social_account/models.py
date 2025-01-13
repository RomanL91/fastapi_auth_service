from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.BASE_model import Base


class SocialAccount(Base):
    """Модель данных о социальных сетях пользователя"""

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )  # Связь с пользователем
    provider: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )  # Название провайдера (например, Google, Facebook)
    provider_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )  # Уникальный идентификатор пользователя у провайдера
    email: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )  # Email, полученный от провайдера (если доступен)
    full_name: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )  # Имя пользователя
    avatar_url: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )  # Ссылка на аватарку от провайдера

    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="social_accounts",
    )
