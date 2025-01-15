from abc import ABC, abstractmethod

from core.DB_manager import db_manager

from app_jwt.jwt_repository import JWTokenRepository
from app_sms.sms_repository import SMSCodeRepository
from app_users.users_repository import UserRepository
from app_phone_numbers.phone_num_repository import PhoneNumberRepository
from app_phone_numbers.phone_num_repository import PhoneNumberRepository
from app_social_account.soc_acc_repository import SocialAccountRepository


class IUnitOfWork(ABC):

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = db_manager.get_scope_session()

    async def __aenter__(self):
        self.session = self.session_factory()
        self.jwt = JWTokenRepository(self.session)
        self.sms = SMSCodeRepository(self.session)
        self.user = UserRepository(self.session)
        self.phone = PhoneNumberRepository(self.session)
        self.social_acc = SocialAccountRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
