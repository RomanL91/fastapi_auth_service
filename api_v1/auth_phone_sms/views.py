from fastapi import APIRouter, status

# === Depends
from api_v1.api_dependencies import UOF_Depends

# === Services
from app_phone_numbers.phone_service import PhoneNumberService

# === Schemas
from app_phone_numbers.schemas import PhoneNumberRequest, PhoneNumberResponse


router = APIRouter(tags=["phone"])


@router.post(
    "/login/phone",
    status_code=status.HTTP_200_OK,
    response_model=PhoneNumberResponse,
    summary="Получить ID записи телефонного номера.",
    description="""
        Через данный endpoint будет создана новая запись в БД или
        получена существующая о телефонном номере. 
        Возращает ID записи.
    """,
)
async def login_phone(
    uow: UOF_Depends,
    phone_num_schema: PhoneNumberRequest,
) -> PhoneNumberResponse:
    # Инициализируем сервис
    service = PhoneNumberService(uow=uow)
    # Вызываем метод сервиса
    result = await service.get_or_create_phone_number(phone_num_schema.phone_number)
    # Возвращаем результат
    return result
