from abc import ABC, abstractmethod
from core.BASE_unit_of_work import UnitOfWork
from app_phone_numbers.schemas import PhoneNumberResponse


class PhoneNumberStrategy(ABC):
    @abstractmethod
    async def execute(self, uow: UnitOfWork, phone_number: str) -> PhoneNumberResponse:
        """
        Метод для выполнения стратегии.
        Должен возвращать объект PhoneNumberResponse с ID телефонного номера.
        """
        pass


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
