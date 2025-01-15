from core.BASE_unit_of_work import UnitOfWork
from app_phone_numbers.schemas import PhoneNumberResponse
from app_phone_numbers.PhoneNumSrtategy import (
    ExistingPhoneStrategy,
    NewPhoneStrategy,
    PhoneNumberContext,
)


class PhoneNumberService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.context = PhoneNumberContext(
            existing_strategy=ExistingPhoneStrategy(),
            new_strategy=NewPhoneStrategy(),
        )

    async def get_or_create_phone_number(
        self, phone_number: str
    ) -> PhoneNumberResponse:
        """
        Получить ID записи о телефонном номере или создать новую запись.
        """
        # 1. Сначала проверяем в БД — есть ли такой номер
        async with self.uow as uow:
            phone_record = await uow.phone.get_obj(phone_number=phone_number)
            # Флаг существования
            is_existing = phone_record is not None

        # 2. На основе флага вызываем нужную стратегию
        return await self.context.execute(self.uow, phone_number, is_existing)
