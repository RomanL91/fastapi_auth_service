from core.BASE_repository import SQLAlchemyRepository

from app_phone_numbers.models import PhoneNumber


class PhoneNumberRepository(SQLAlchemyRepository):
    model = PhoneNumber
