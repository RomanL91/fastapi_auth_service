from uuid import UUID
from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


# 1. Enum для типа транзакции
class PointsTransactionType(StrEnum):
    CREDIT = "credit"
    DEBIT = "debit"


# 2. Транзакции (UserPointsTransaction)
class UserPointsTransactionBase(BaseModel):
    type: PointsTransactionType = Field(..., description="Тип транзакции: credit/debit")
    amount: Annotated[
        int, Field(..., description="Количество баллов, списанных/начисленных")
    ]
    description: Annotated[
        str | None, Field(default=None, description="Комментарий (причина)")
    ]
    expires_at: Annotated[
        datetime, Field(..., description="Когда баллы сгорят, если не потратить")
    ]

    model_config = ConfigDict()


class UserPointsTransactionCreate(UserPointsTransactionBase):
    """
    Схема для создания транзакции баллов.
    """

    pass


class UserPointsTransactionRead(UserPointsTransactionBase):
    """
    Схема чтения транзакции (GET).
    """

    id: Annotated[UUID, Field(...)]
    created_at: Annotated[datetime, Field(...)]
    updated_at: Annotated[datetime, Field(...)]
    is_active: Annotated[bool, Field(..., description="Актуальна ли транзакция")]

    model_config = ConfigDict(from_attributes=True)


# 3. Баланс (UserPointsBalance)
class UserPointsBalanceBase(BaseModel):
    balance: Annotated[int, Field(..., description="Текущее количество баллов")]

    model_config = ConfigDict()


class UserPointsBalanceCreate(UserPointsBalanceBase):
    """
    Схема для создания кошелька (если нужно явно).
    """

    pass


class UserPointsBalanceRead(UserPointsBalanceBase):
    """
    Схема для чтения баланса и, при желании, списка транзакций.
    """

    id: Annotated[UUID, Field(...)]
    user_id: Annotated[UUID, Field(...)]
    created_at: Annotated[datetime, Field(...)]
    updated_at: Annotated[datetime, Field(...)]
    is_active: Annotated[bool, Field(...)]
    transactions: Annotated[
        list[UserPointsTransactionRead] | None, Field(default=None)
    ] = None

    model_config = ConfigDict(from_attributes=True)
