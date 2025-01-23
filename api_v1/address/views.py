from fastapi import APIRouter, status, HTTPException

from api_v1.api_dependencies import UOF_Depends, Access_JWT_Depends

# === Services
from app_users.user_service import UserService

# === Schemas
from app_users.schemas import UserAddressSchema


router = APIRouter(tags=["address"])


@router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=UserAddressSchema,
    summary="Добавить информацию об адресе пользователя.",
    description="""
        Идея проста: при любой возможности (например, при заполнении формы заявки на покупку) можно собрать информацию об адресе пользователя и сохранить ее.<br>
        `street_line1` - обязательное поле.<br>
        В тоже время <br>
        `street_line2` - не обязательное.<br>
        **Пытаюсь предложить на твое умотрение как сохранять информацию, можно весь адресс целиком в `street_line1`, а можешь раздробить и часть адреса, например, номер дома, квартиры хранить уже `street_line2`.**<br>
        Из обязательных полей так же `city`.<br>
    """,
)
async def add_user_address(
    uow: UOF_Depends,
    token: Access_JWT_Depends,
    address_data: UserAddressSchema,
):
    user_id = token.get("user_id", None)
    if user_id:
        pass
        # Инициализируем сервис и вызываем метод `create_user_address`
        user_service = UserService(uow=uow)
        user_address = await user_service.create_user_address(
            user_id=user_id, address_data=address_data
        )
        return user_address
    # Иначе выкидываем исключение
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unexpected data retrieval error",
    )
