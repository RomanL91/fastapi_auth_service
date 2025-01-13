from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func, text

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
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=(func.now() + text("INTERVAL '5 MINUTE")),
        nullable=False,
    )  # Время истечения кода, через 5 минут после создания
    is_used: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )  # Был ли код использован

    user: Mapped["User"] = relationship(  # type: ignore
        "User",
        back_populates="sms_codes",
    )
