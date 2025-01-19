from fastapi import APIRouter, status, HTTPException

from api_v1.api_dependencies import UOF_Depends, Access_JWT_Depends

# === Services
from app_users.user_service import UserService

# === Schemas
from app_users.schemas import UserSchema


router = APIRouter(tags=["user"])


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    summary="Получить информацию о пользователе.",
    description="""
        **Через данный endpoint можно получить информацию о пользователе в обмен 
        `на актуальный ключ доступа типа access`.** <br>
    """,
)
async def get_user_info(
    uow: UOF_Depends,
    token: Access_JWT_Depends,
):
    user_id = token.get("user_id", None)
    if user_id:
        # Инициализируем сервис и вызываем метод `get_user_info`
        user_service = UserService(uow=uow)
        user_info = await user_service.get_user_info(user_id=user_id)
        # Отдаем информацию о пользователе
        return UserSchema.model_validate(user_info)
    # Иначе выкидываем исключение
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unexpected data retrieval error",
    )
