from typing import Annotated
from fastapi import Depends

from core.settings import settings
from core.BASE_unit_of_work import IUnitOfWork, UnitOfWork

from app_jwt.utils import JWTBearer


access_token_scheme = JWTBearer(expected_token_type=settings.auth_jwt.access_token_type)
refresh_token_scheme = JWTBearer(
    expected_token_type=settings.auth_jwt.refresh_token_type
)

UOF_Depends = Annotated[IUnitOfWork, Depends(UnitOfWork)]
Access_JWT_Depends = Annotated[str, Depends(access_token_scheme)]
Refresh_JWT_Depends = Annotated[str, Depends(refresh_token_scheme)]
