from typing import List
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.BASE_model import Base

DEFAULT_AVATAR_PATH = "avatar_default.png"


class ClientUUID(Base):
    """Модель для хранения UUID, генерируемых на клиенте"""

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )  # Пользователь (если авторизован)
    client_uuid: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )  # UUID от клиента
    ip_address: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )  # IP-адрес пользователя
    device_type: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )  # Тип устройства (например, desktop, mobile)

    user: Mapped["User | None"] = relationship(  # type: ignore
        "User",
        back_populates="client_uuids",
    )


class User(Base):
    """Модель пользователя"""

    __tablename__ = "users"

    username: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True,
    )
    avatar_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=DEFAULT_AVATAR_PATH,
    )
    email: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        unique=True,
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    external_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        unique=True,
    )
    phone: Mapped["PhoneNumber"] = relationship(  # type: ignore
        "PhoneNumber",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    social_accounts: Mapped[List["SocialAccount"]] = relationship(  # type: ignore
        "SocialAccount",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    tokens: Mapped[List["JWToken"]] = relationship(  # type: ignore
        "JWToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    sms_codes: Mapped[List["SMSCode"]] = relationship(  # type: ignore
        "SMSCode",
        back_populates="user",
        cascade="all, delete-orphan",
    )
