from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class SocialAccountSchema(BaseModel):
    provider: Annotated[str, Field(...)]
    provider_id: Annotated[str, Field(...)]
    email: Annotated[EmailStr | None, Field(default=None)]
    full_name: Annotated[str | None, Field(default=None)]
    avatar_url: Annotated[str | None, Field(default=None)]

    model_config = ConfigDict(from_attributes=True)
