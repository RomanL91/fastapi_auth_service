from httpx import AsyncClient

from fastapi import HTTPException, status

from core.settings import settings
from core.BASE_unit_of_work import IUnitOfWork


class SocAccService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_access_key_from_oauth_service(
        self,
        url: str,
        payload_template: dict,
        headers: dict = {},
    ):
        async with AsyncClient() as client:
            response = await client.post(
                url=url,
                headers=headers,
                data=payload_template,
            )
            response_data = response.json()
            access_token = response_data.get("access_token", False)

            if access_token:
                return access_token

    async def fetch_user_info(
        self,
        url: str,
        headers: dict = None,
        data: dict = None,
        request_method: str = "GET",
    ):
        client = AsyncClient()
        # Выбираем метод запроса (GET или POST)
        if request_method == "POST":
            response = await client.post(url, headers=headers, data=data)
            user_info_response = response.json().get("user")
        else:
            response = await client.get(url, headers=headers)
            user_info_response = response.json()
        return user_info_response

    async def get_or_create_google_account(
        self,
        google_id: str,
        email: str | None,
        full_name: str | None,
        avatar_url: str | None,
    ):
        async with self.uow as uow:
            # 1) Ищем соц. аккаунт именно по Google ID:
            social_acc = await uow.social_acc.get_obj(
                provider="google", provider_id=google_id
            )
            if social_acc:
                # можно обновить поля
                await uow.social_acc.update_obj(
                    social_acc.id,
                    full_name=full_name,
                    avatar_url=avatar_url,
                    email=email,
                )
                await uow.commit()
                return social_acc

            # 2) Если нет Google-аккаунта, ищем соц.акк по email
            if email:
                maybe_acc = await uow.social_acc.get_obj(email=email)
                if maybe_acc:
                    # Если у этого аккаунта уже есть user, привязываемся к нему
                    # (у нас будет тот же User, но другой SocialAccount)
                    new_social_acc = await uow.social_acc.create_obj(
                        user_id=maybe_acc.user_id,
                        provider="google",
                        provider_id=google_id,
                        email=email,
                        full_name=full_name,
                        avatar_url=avatar_url,
                    )
                    await uow.commit()
                    return new_social_acc

            # 3) Иначе создаём нового User, если не нашли ничего
            new_user = await uow.user.create_obj(
                username=full_name, email=email, avatar_path=avatar_url
            )
            new_social_acc = await uow.social_acc.create_obj(
                user_id=new_user.id,
                provider="google",
                provider_id=google_id,
                email=email,
                full_name=full_name,
                avatar_url=avatar_url,
            )
            await uow.commit()
            return new_social_acc

    async def authenticate_google_user(self, **kwargs):
        settings.google_auth.data_post = kwargs  # готовим пакет для отправки

        access_token_google = await self.get_access_key_from_oauth_service(
            url=settings.google_auth.google_token_url,
            payload_template=settings.google_auth.data_post,
        )
        if access_token_google is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error getting Google token",
            )

        data_user_from_google = await self.fetch_user_info(
            url=settings.google_auth.google_user_info_url,
            headers=settings.google_auth.get_headers(access_token_google),
        )

        social_acc = await self.get_or_create_google_account(
            google_id=data_user_from_google["id"],
            email=data_user_from_google["email"],
            full_name=data_user_from_google["name"],
            avatar_url=data_user_from_google["picture"],
        )

        return social_acc
