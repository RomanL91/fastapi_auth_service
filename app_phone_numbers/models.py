from datetime import datetime

from sqlalchemy.sql import func
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.BASE_model import Base


class PhoneNumber(Base):
    """Модель телефонного номера"""

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )  # Связь с пользователем
    phone_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )  # Номер телефона
    verified_at: Mapped[datetime | None] = mapped_column(
        default=func.now(),
    )  # Дата и время подтверждения номера (если применимо)

    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="phone",
    )
