from fastapi import APIRouter

from api_v1.auth_phone_sms.views import router as phone_router

router = APIRouter()

router.include_router(router=phone_router, prefix="/auth_phone")
# router.include_router(router=oath2_google_router, prefix="/auth_user")
# router.include_router(router=oauth2_vk_router, prefix="/auth_user")
# router.include_router(router=auth_phone_router, prefix="/auth_user")
# router.include_router(router=user_router, prefix="/user")
# router.include_router(router=jwt_router, prefix="/token")
