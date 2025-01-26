from fastapi import APIRouter

from api_v1.auth_phone_sms.views import router as phone_router
from api_v1.oath2_google.views import router as oath2_google_router
from api_v1.jwt.views import router as jwt_router
from api_v1.user.views import router as user_router
from api_v1.address.views import router as address_router
from api_v1.wishlist_items.views import router as wishlist_ruoter
from api_v1.viewed_prod.views import router as viewed_router

router = APIRouter()

router.include_router(router=phone_router, prefix="/auth_phone")
router.include_router(router=oath2_google_router, prefix="/auth_user")
router.include_router(router=jwt_router, prefix="/token")
router.include_router(router=user_router, prefix="/user")
router.include_router(router=address_router, prefix="/address")
router.include_router(router=wishlist_ruoter, prefix="/wishlist")
router.include_router(router=viewed_router, prefix="/viewed")
# router.include_router(router=auth_phone_router, prefix="/auth_user")
