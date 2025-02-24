from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Request,
    UploadFile,
    File,
)

from api_v1.api_dependencies import UOF_Depends, Access_JWT_Depends

# === Services
from app_users.user_service import UserService

# === Schemas
from app_users.schemas import UserSchema, UserUpdateSchema


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


@router.patch(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    summary="Обновить информацию о пользователе.",
    description="""
        **Через данный endpoint можно обновить информацию о пользователе.** <br>
    """,
)
async def update_user_info(
    user_update: UserUpdateSchema,
    uow: UOF_Depends,
    token: Access_JWT_Depends,
):
    user_id = token.get("user_id", None)
    if user_id:
        # Инициализируем сервис и вызываем метод `update_user_info`
        user_service = UserService(uow=uow)
        updated_user = await user_service.update_user_info(user_id, user_update)
        return UserSchema.model_validate(updated_user)
    # Иначе выкидываем исключение
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unexpected data retrieval error",
    )


@router.post(
    "/avatar",
    response_model=UserSchema,
    summary="Обновить аватарку пользователя",
    description="""
        **Обновляет аватарку текущего пользователя.**
        Загрузите файл изображения, и он будет сохранён на сервере.
    """,
    status_code=status.HTTP_200_OK,
)
async def update_user_avatar(
    token: Access_JWT_Depends,
    uow: UOF_Depends,
    request: Request,
    file: UploadFile = File(..., description="Новая аватарка пользователя"),
):
    user_id = token.get("user_id", None)

    if user_id:
        user_service = UserService(uow=uow)
        user = await user_service.payload_avatar(
            unique_name=user_id,
            request=request,
            file=file,
        )
        return user

    # Иначе выкидываем исключение
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unexpected data retrieval error",
    )
