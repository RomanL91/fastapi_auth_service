from uuid import UUID

from core.BASE_unit_of_work import UnitOfWork

from app_sms.models import SMSCode


class SMSCodeService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def chec_sms_code(
        self,
        code: str,
        phone_id: UUID,
    ) -> SMSCode:
        async with self.uow as uow:
            sms = await uow.sms.get_unused_code_for_phone(
                code,
                phone_id,
            )
            if sms:
                sms.is_used = True
                sms.is_active = False
                await uow.commit()
                return sms
            return None
