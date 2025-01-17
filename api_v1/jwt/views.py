from fastapi import APIRouter, status, HTTPException


from api_v1.api_dependencies import UOF_Depends

from app_jwt.schemas import JWTRequestRefresh, JWTSchema
from app_jwt.utils import jwt_util
from app_jwt.jwt_service import JWTService


router = APIRouter(tags=["token"])


@router.post(
    "/refresh",
    status_code=status.HTTP_201_CREATED,
    response_model=JWTSchema,
    summary="Обновить ключ доступа.",
    description="""
        **Через данный endpoint можно получить ключ доступа `типа access` в обмен на ключ доступа `типа refresh`.**
    """,
)
async def refresh(uow: UOF_Depends, token: JWTRequestRefresh):
    data_payload_token = token.model_dump()
    jwt_service = JWTService(uow=uow)

    if data_payload_token:
        user_id = data_payload_token["token"]["user_id"]

        access_token = await jwt_service.create_and_store_access(
            user_id=user_id,
            type=jwt_util.access_token_type,
        )
        return access_token

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unexpected data retrieval error",
    )
