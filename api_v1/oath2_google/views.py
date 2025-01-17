from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.settings import settings
from api_v1.api_dependencies import UOF_Depends

from app_jwt.jwt_service import JWTService
from app_social_account.soc_acc_service import SocAccService

from app_jwt.schemas import JWTPairResponse


router = APIRouter(tags=["google"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


@router.get(
    "/login/google/",
    status_code=status.HTTP_200_OK,
    summary="Получить ссылку на авторизацию через Google.",
)
async def login_google():
    return {
        # TODO вынести в настройки
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.google_auth.google_client_id}&redirect_uri={settings.google_auth.google_redirect_url}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get(
    "/auth/google",
    status_code=status.HTTP_201_CREATED,
    response_model=JWTPairResponse,
    summary="Получить ключи от обратного вызова Google",
    description="""
        **Внимание! Сервис OAuth2 Google сам вызывает данный endpoint.**<br><br>
        Эндпоинт принимает в query `code`, который присылает сервис OAuth2 Google.<br>
    """,
)
async def auth_google(
    uow: UOF_Depends,
    code: str,
):
    # Инициализируем сервисы
    soc_acc_service = SocAccService(uow=uow)
    jwt_service = JWTService(uow=uow)

    soc_acc = await soc_acc_service.authenticate_google_user(code=code)
    if soc_acc:
        tokens = await jwt_service.create_and_store_token(user_id=soc_acc.user_id)
        return tokens
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired authorization code",
    )
