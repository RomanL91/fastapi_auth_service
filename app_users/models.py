from typing import List, Optional
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from core.BASE_model import Base

DEFAULT_AVATAR_PATH = "avatar_default.png"


class User(Base):
    """Модель пользователя"""

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
    points_balance: Mapped[Optional["UserPointsBalance"]] = relationship(  # type: ignore
        "UserPointsBalance",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    addresses: Mapped[List["UserAddress"]] = relationship(
        "UserAddress",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    wishlist_items: Mapped[list["WishlistItem"]] = relationship(  # type: ignore
        back_populates="user",
        cascade="all, delete-orphan",
    )
    vieved_products: Mapped[list["ViewedProduct"]] = relationship(  # type: ignore
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserAddress(Base):
    """
    Адрес доставки пользователя
    """

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Поля адреса
    street_line1: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    street_line2: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    city: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    state: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    # Дополнительный номер телефона, указанный при доставке
    phone: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # Связь с пользователем
    user: Mapped["User"] = relationship(
        "User",
        back_populates="addresses",
    )
