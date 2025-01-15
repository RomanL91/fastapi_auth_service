from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, UUID4


class SMSCodeRequest(BaseModel):
    model_config = ConfigDict(
        strict=False,
        json_schema_extra={
            "example": {
                "code": "9087",
                "phone_number_id": "d7983b4c-6595-4c07-9d76-c8dbd80c8d8c",
            }
        },
    )
    code: Annotated[
        str,
        Field(
            ...,
            min_length=4,
            max_length=4,
            pattern=r"^\d{4}$",
            description="4-значный код в формате XXXX.",
        ),
    ]
    phone_number_id: Annotated[
        UUID4,
        Field(
            ...,
            description="ID телефонного номера, на который выслан код.",
        ),
    ]
