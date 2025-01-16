from fastapi import APIRouter, HTTPException, status

# === Depends
from api_v1.api_dependencies import UOF_Depends

# === Services
from app_jwt.jwt_service import JWTService
from app_sms.sms_service import SMSCodeService
from app_phone_numbers.phone_service import PhoneNumberService

# === Schemas
from app_jwt.schemas import JWTPairResponse
from app_sms.schemas import SMSCodeRequest
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


@router.post(
    "/auth/phone",
    status_code=status.HTTP_201_CREATED,
    response_model=JWTPairResponse,
    summary="Получить ключи по `code` и `phone_number_id`",
    description="""
        **Эндпоинт для верификации SMS-кода и выдачи JWT-токенов.**<br>
        - Принимает 4-значный `code` (*получишь по смс*).<br> 
        - Принимает UUID поля `phone_number_id` (*это id записи телефоного номера, 
            чтобы получить: <a href=docs#/phone/login_phone_auth_api_v1_auth_phone_login_phone_post>ctrl+тык</a>*).<br>
        - Если код валиден, создаёт и возвращает пару токенов (ACCESS/REFRESH).<br>
        - Если код невалиден — выбрасывает 403 Forbidden.
    """,
)
async def auth_phone(
    uow: UOF_Depends,
    sms_schema: SMSCodeRequest,
):
    # Инициализируем сервисы
    sms_service = SMSCodeService(uow=uow)
    jwt_service = JWTService(uow=uow)

    sms_code = await sms_service.chec_sms_code(
        code=sms_schema.code,
        phone_id=sms_schema.phone_number_id,
    )
    if sms_code:  # если смс найдено
        # создаем jwt и возращаем
        tokens = await jwt_service.create_and_store_token(user_id=sms_code.user_id)
        return tokens
    # иначе возбуждаю 403
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired sms code"
    )
