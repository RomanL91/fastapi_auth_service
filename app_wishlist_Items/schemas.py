from uuid import UUID
from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# WishlistItem ===========================


class WishlistItemBase(BaseModel):
    product_id: Annotated[int, Field(...)]
    client_uuid: Annotated[UUID, Field(...)]


class WishlistItemCreate(WishlistItemBase):
    user_id: Annotated[UUID | None, Field(default=None)]
    is_active: Annotated[bool | None, Field(...)]


class WishlistItemRead(WishlistItemBase):
    id: Annotated[UUID, Field(...)]
    user_id: Annotated[UUID | None, Field(default=None)]
    created_at: Annotated[datetime, Field(...)]
    is_active: Annotated[bool, Field(...)]
    # updated_at, is_active, etc.
    model_config = ConfigDict(from_attributes=True)


# VievedProducts ===========================


class VievedProductsBase(BaseModel):
    product_id: Annotated[int, Field(...)]
    client_uuid: Annotated[UUID | None, Field(default=None)]


class VievedProductsCreate(WishlistItemBase):
    user_id: Annotated[UUID | None, Field(default=None)]


class VievedProductsRead(WishlistItemBase):
    id: Annotated[UUID, Field(...)]
    user_id: Annotated[UUID | None, Field(default=None)]
    created_at: Annotated[datetime, Field(...)]
    # updated_at, is_active, etc.
    model_config = ConfigDict(from_attributes=True)
