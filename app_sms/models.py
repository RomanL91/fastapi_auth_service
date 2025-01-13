from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, text

from core.BASE_model import Base


class SMSCode(Base):
    """Модель для хранения SMS-кодов авторизации"""

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )  # Связь с пользователем
    code: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
    )  # Сам код (например, 6-значный)
    expires_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=text(
            "NOW() + INTERVAL '5 MINUTE'"
        ),  # Устанавливаем значение по умолчанию на уровне базы данных
        nullable=False,
    )  # Время истечения кода
    is_used: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )  # Был ли код использован

    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="sms_codes",
    )
