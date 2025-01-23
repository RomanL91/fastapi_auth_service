from uuid import UUID

from enum import Enum as StrEnum

from datetime import datetime

from typing import List

from sqlalchemy import ForeignKey, Integer, String, Enum, text, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.BASE_model import Base

from app_users.models import User


class PointsTransactionType(str, StrEnum):
    CREDIT = "credit"  # Начисление баллов
    DEBIT = "debit"  # Списание баллов


class UserPointsBalance(Base):
    """Кошелёк (или баланс) бонусных баллов пользователя"""

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    # Связь с пользователем
    user: Mapped["User"] = relationship(
        "User", back_populates="points_balance", uselist=False
    )
    # Связь с историей транзакций
    transactions: Mapped[List["UserPointsTransaction"]] = relationship(
        "UserPointsTransaction", back_populates="wallet", cascade="all, delete-orphan"
    )


class UserPointsTransaction(Base):
    """История транзакций бонусных баллов"""

    wallet_id: Mapped[UUID] = mapped_column(
        ForeignKey("userpointsbalances.id", ondelete="CASCADE"),
        nullable=False,
    )
    type: Mapped[PointsTransactionType] = mapped_column(
        Enum(PointsTransactionType),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    wallet: Mapped["UserPointsBalance"] = relationship(
        "UserPointsBalance", back_populates="transactions"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("NOW() + INTERVAL '3 MONTHS'"),
        nullable=False,
    )
