__all__ = (
    # организуем единую точку импорта
    "Base",
    "User",
    "JWToken",
    "SMSCode",
    "PhoneNumber",
    "SocialAccount",
)


from .BASE_model import Base

# for migrations
from app_users.models import User
from app_jwt.models import JWToken
from app_sms.models import SMSCode
from app_phone_numbers.models import PhoneNumber
from app_social_account.models import SocialAccount
