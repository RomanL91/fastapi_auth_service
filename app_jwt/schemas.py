from datetime import datetime

from fastapi import status, HTTPException

from typing_extensions import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    UUID4,
    Field,
    field_validator,
)

from app_jwt.utils import jwt_util


class JWTSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "example": {
                "user_id": "2cdb7fba2050471792632ebe72bf0267",
                "issued_at": "2024-09-27T23:39:31.781647+05:00",
                "expires_at": "2024-09-27T23:44:31.781647+05:00",
                "token_type": "access_token | refresh_token",
                "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMmNkYjdmYmEtMjA1MC00NzE3LTkyNjMtMmViZTcyYmYwMjY3IiwidHlwZSI6ImFjY2Vzc190b2tlbiIsImV4cCI6MTcyNzQ2MjY3MSwiaWF0IjoxNzI3NDYyMzcxfQ.BZ-NLCWzuwGtqEFsf6Nshex7ag5SCqOODg7D909RerCI91wjkTkklPii0DP1A98ydabMe6F3hBmP65umCFTDeGMt1Oi1ohBk3O8rHBoEdomseg4HepjnAKzpPWa-9GHeleFlVKOwYevYjw86mGJg5-evT8XAdHVv3MkX4Wwg74mUecUiAc_DOktb73cHWf4nh6j2LbdTcyIgh2pSQasopT6z2hV6oKRwn3lqX7ECADG6lDVZ66DnD0xXPmgDr7xXVt4X8vi1OsspYIQhoeKLUvkpqOGsI4Q6KGX71geqAkEWVb7G2NdkmUbWdBvfbfQo7caOIR8S8hsin6BS52E6DQ",
                "revoked": False,
            }
        },
    )
    user_id: UUID4
    issued_at: datetime
    expires_at: datetime
    token_type: str
    token: str
    revoked: bool = False


class JWTPairResponse(BaseModel):
    access: JWTSchema
    refresh: JWTSchema


class JWTRequestRefresh(BaseModel):
    token: Annotated[
        str,
        Field(
            ...,
            description="JWT токен",
            example="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
        ),
    ]

    @field_validator("token")
    def validate_token_and_extract_payload(cls, value):
        payload_data = jwt_util.decode_jwt(value)
        if payload_data["type"] == jwt_util.refresh_token_type:
            return jwt_util.decode_jwt(value)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )
