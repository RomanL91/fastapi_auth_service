from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError

from core.BASE_unit_of_work import UnitOfWork

from app_wishlist_Items.models import WishlistItem

from app_wishlist_Items.schemas import WishlistItemCreate, VievedProductsCreate


class ItemsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_item_in_wishlist(self, item_data: WishlistItemCreate) -> WishlistItem:
        #  TODO сильное копирование DRY!!!
        async with self.uow as uow:
            try:
                item = await uow.wishlist.get_or_create(
                    client_uuid=item_data.client_uuid,
                    user_id=item_data.user_id,
                    product_id=item_data.product_id,
                )
                if item_data.user_id:
                    item.user_id = item_data.user_id
                if not item_data.is_active:
                    item.is_active = False
                await uow.commit()
                return item
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unexpected data retrieval error",
                )

    async def add_item_in_viewedlist(self, item_data: VievedProductsCreate) -> None:
        #  TODO сильное копирование DRY!!!
        async with self.uow as uow:
            try:
                item = await uow.viewed.get_or_create(
                    client_uuid=item_data.client_uuid,
                    user_id=item_data.user_id,
                    product_id=item_data.product_id,
                    deltatime_min=30,
                )
                if item_data.user_id and item:
                    item.user_id = item_data.user_id
                await uow.commit()
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unexpected data retrieval error",
                )

    async def get_all_prod_by_client_uuid_or_user_id(
        self,
        client_uuid: UUID | None = None,
        user_id: UUID | None = None,
    ):
        async with self.uow as uow:
            items = await uow.wishlist.get_all_objs_by(
                client_uuid,
                user_id,
            )
            if user_id:
                for i in items:
                    if not i.user_id:
                        i.user_id = user_id
                await uow.commit()
            return items

    async def get_all_prod_viewed_by_client_uuid_or_user_id(
        self,
        client_uuid: UUID | None = None,
        user_id: UUID | None = None,
    ):
        async with self.uow as uow:
            items = await uow.viewed.get_all_objs_by(
                client_uuid,
                user_id,
            )
            if user_id:
                for i in items:
                    if not i.user_id:
                        i.user_id = user_id
                await uow.commit()
            return items
