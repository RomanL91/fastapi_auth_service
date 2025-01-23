from uuid import UUID
from datetime import datetime
from typing import Annotated, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app_social_account.schemas import SocialAccountSchema
from app_phone_numbers.schemas import PhoneNumberSchema


class UserAddressSchema(BaseModel):
    # id: Annotated[UUID, Field(...)]
    street_line1: Annotated[
        str, Field(..., description="Обязательная часть адреса (улица, дом)")
    ]
    street_line2: Annotated[
        str | None, Field(default=None, description="Доп. строка адреса (кв., подъезд)")
    ]
    city: Annotated[str, Field(..., description="Город")]
    state: Annotated[str | None, Field(default=None, description="Область")]
    phone: Annotated[
        str | None,
        Field(
            pattern=r"^(?:\+7|8)\d{10}$", default=None, description="Контактный телефон"
        ),
    ]
    is_default: Annotated[bool, Field(default=False, description="Адрес по умолчанию")]

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    id: Annotated[UUID, Field(...)]
    username: Annotated[str | None, Field(default=None)]
    avatar_path: Annotated[str, Field(...)]
    email: Annotated[EmailStr | None, Field(default=None)]
    last_login: Annotated[datetime | None, Field(default=None)]
    external_id: Annotated[str | None, Field(default=None)]
    phone: Annotated[PhoneNumberSchema | None, Field(default=None)]
    social_accounts: Annotated[List[SocialAccountSchema], Field(default_factory=list)]
    addresses: Annotated[List[UserAddressSchema], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: Annotated[str | None, Field(default=None)]
    # avatar_path: Annotated[str | None, Field(default=None)]
    email: Annotated[EmailStr | None, Field(default=None)]

    model_config = ConfigDict(from_attributes=True)


class UserAvatarSchema(BaseModel):
    avatar_path: Annotated[
        str | None,
        Field(
            default=None,
            description="Path to user's avatar",
        ),
    ]

    model_config = ConfigDict(from_attributes=True)
