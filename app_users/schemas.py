from uuid import UUID
from datetime import datetime
from typing import Annotated, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app_social_account.schemas import SocialAccountSchema
from app_phone_numbers.schemas import PhoneNumberSchema


class UserSchema(BaseModel):
    id: Annotated[UUID, Field(...)]
    username: Annotated[str | None, Field(default=None)]
    avatar_path: Annotated[str, Field(...)]
    email: Annotated[EmailStr | None, Field(default=None)]
    last_login: Annotated[datetime | None, Field(default=None)]
    external_id: Annotated[str | None, Field(default=None)]
    phone: Annotated[PhoneNumberSchema | None, Field(default=None)]
    social_accounts: Annotated[List[SocialAccountSchema], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)
