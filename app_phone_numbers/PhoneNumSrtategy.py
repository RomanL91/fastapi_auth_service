from abc import ABC, abstractmethod
from random import randint

from core.BASE_unit_of_work import UnitOfWork

from app_sms.models import SMSCode
from app_phone_numbers.schemas import PhoneNumberResponse


class PhoneNumberStrategy(ABC):
    @abstractmethod
    async def execute(self, uow: UnitOfWork, phone_number: str) -> PhoneNumberResponse:
        """
        Метод для выполнения стратегии.
        Должен возвращать объект PhoneNumberResponse с ID телефонного номера.
        """
        pass

    async def _create_sms_code(self, uow: UnitOfWork, user_id: str) -> SMSCode:
        """
        Базовый метод, который:
        1) Генерирует 6-значный код (с ведущими нулями)
        2) Создаёт запись SMSCode в БД
        3) Возвращает созданную запись SMSCode
        """
        # Генерируем код вида "0123" (всегда 4 цифр, даже если < 10000)
        generated_code = f"{randint(0, 9999):04d}"

        sms_code = await uow.sms.create_obj(user_id=user_id, code=generated_code)
        return sms_code


class ExistingPhoneStrategy(PhoneNumberStrategy):
    async def execute(self, uow: UnitOfWork, phone_number: str) -> PhoneNumberResponse:
        """
        Стратегия обработки существующего номера телефона.
        """
        # Здесь можно не делать ещё один запрос,
        # так как я уже получил запись из БД на уровне сервиса (TODO можно потом оптимизировать)
        async with uow as uow:
            phone_record = await uow.phone.get_obj(phone_number=phone_number)
            if not phone_record:
                raise ValueError(f"Phone number {phone_number} not found")

            # Создаём SMS-код для этого пользователя
            sms_code = await self._create_sms_code(uow, user_id=phone_record.user_id)
            # Сохраняем изменения
            await uow.commit()
            return PhoneNumberResponse(id=phone_record.id)


class NewPhoneStrategy(PhoneNumberStrategy):
    async def execute(self, uow: UnitOfWork, phone_number: str) -> PhoneNumberResponse:
        """
        Стратегия обработки нового номера телефона.
        Создаёт пользователя и связывает его с номером телефона.
        """
        async with uow as uow:
            # Создаём нового пользователя
            new_user = await uow.user.create_obj(username=phone_number, email=None)

            # Создаём запись для номера телефона
            new_phone_record = await uow.phone.create_obj(
                phone_number=phone_number, user_id=new_user.id
            )
            # И тут создаём SMS-код для этого пользователя
            sms_code = await self._create_sms_code(uow, user_id=new_user.id)
            # Фиксируем изменения
            await uow.commit()

            return PhoneNumberResponse(id=new_phone_record.id)


class PhoneNumberContext:
    """
    Контекст, который внутри себя решает, какую стратегию вызвать,
    но не делает лишних запросов в БД.
    """

    def __init__(
        self, existing_strategy: PhoneNumberStrategy, new_strategy: PhoneNumberStrategy
    ):
        self.existing_strategy = existing_strategy
        self.new_strategy = new_strategy

    async def execute(
        self, uow: UnitOfWork, phone_number: str, is_existing: bool
    ) -> PhoneNumberResponse:
        # Если флаг is_existing = True, вызываем ExistingPhoneStrategy
        if is_existing:
            return await self.existing_strategy.execute(uow, phone_number)
        else:
            return await self.new_strategy.execute(uow, phone_number)
