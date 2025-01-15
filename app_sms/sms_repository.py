from core.BASE_repository import SQLAlchemyRepository

from app_sms.models import SMSCode


class SMSCodeRepository(SQLAlchemyRepository):
    model = SMSCode
