__all__ = (
    # организуем единую точку импорта
    "Base",
    "User",
    "UserAddress",
    "JWToken",
    "SMSCode",
    "PhoneNumber",
    "SocialAccount",
    "UserPointsBalance",
    "UserPointsTransaction",
    "WishlistItem",
    "ViewedProduct",
)


from .BASE_model import Base

# for migrations
from app_users.models import User, UserAddress
from app_jwt.models import JWToken
from app_sms.models import SMSCode
from app_phone_numbers.models import PhoneNumber
from app_social_account.models import SocialAccount
from app_bonus_points.models import UserPointsBalance, UserPointsTransaction
from app_wishlist_Items.models import WishlistItem, ViewedProduct
