from uuid import UUID

from typing import Annotated

from pydantic import BaseModel, Field, field_validator, ConfigDict

from app_phone_numbers import utils


class PhoneNumberSchema(BaseModel):
    number: Annotated[str, Field(...)]
    # Дополнительные поля при необходимости

    model_config = ConfigDict(from_attributes=True)


class PhoneNumberRequest(BaseModel):
    phone_number: str = Field(
        ...,
        pattern=r"^(?:\+7|8)\d{10}$",  # Номер должен начинаться с +7 или 8 и содержать 10 цифр после этого
        description="Телефонный номер должен начинаться с +7 или 8 и содержать 10 цифр. Пример: +71234567890 или 81234567890",
    )

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        # некоторая логика (например, нормализация номера)
        return utils.normalize_phone(value)


class PhoneNumberResponse(BaseModel):
    id: UUID = Field(
        ...,
        description="Уникальный идентификатор записи телефонного номера",
    )
