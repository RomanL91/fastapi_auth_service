from uuid import UUID

from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update, or_
from sqlalchemy.engine import Result

from core.BASE_repository import SQLAlchemyRepository

from app_wishlist_Items.models import WishlistItem, ViewedProduct


class WishlistItemRepository(SQLAlchemyRepository):
    model = WishlistItem

    async def get_or_create(
        self,
        product_id: int,
        client_uuid: UUID | None = None,
        user_id: UUID | None = None,
        is_active: bool | None = None,
    ):
        # Построение условий поиска с использованием OR
        or_conditions = []
        if client_uuid:
            or_conditions.append(self.model.client_uuid == client_uuid)
        if user_id:
            or_conditions.append(self.model.user_id == user_id)

        # Конструируем запрос с OR условиями
        stmt = select(self.model).where(
            self.model.product_id == product_id, or_(*or_conditions)
        )
        result: Result = await self.session.execute(stmt)
        wishlist_item = result.scalar_one_or_none()

        if wishlist_item:
            if is_active:
                wishlist_item.is_active = is_active
            return wishlist_item

        item = await self.create_obj(
            product_id=product_id,
            client_uuid=client_uuid,
            user_id=user_id,
        )
        return item

    async def get_all_objs_by(
        self,
        client_uuid: UUID | None = None,
        user_id: UUID | None = None,
    ):
        or_conditions = []
        if client_uuid:
            or_conditions.append(self.model.client_uuid == client_uuid)
        if user_id:
            or_conditions.append(self.model.user_id == user_id)
        if not client_uuid and not user_id:
            return or_conditions

        stmt = (
            select(self.model)
            .where(self.model.is_active == True, or_(*or_conditions))
            .order_by(self.model.created_at)
            .limit(50)
        )
        result: Result = await self.session.execute(stmt)
        wishlist_item = result.scalars().all()
        return wishlist_item


class ViewedProductRepository(SQLAlchemyRepository):
    model = ViewedProduct

    async def get_or_create(
        # get_or_create TODO сильное копирование DRY!!! (см выше!)
        self,
        product_id: int,
        client_uuid: UUID | None = None,
        user_id: UUID | None = None,
        deltatime_min: int | None = 30,
    ):
        # Рассчитываем время отсечки TODO (фигня со временем)
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=deltatime_min)

        # Построение условий поиска с использованием OR
        or_conditions = []
        if client_uuid:
            or_conditions.append(self.model.client_uuid == client_uuid)
        if user_id:
            or_conditions.append(self.model.user_id == user_id)

        # Конструируем запрос с OR условиями
        stmt = (
            update(self.model)
            .where(
                self.model.product_id == product_id,
                or_(*or_conditions),
                self.model.created_at >= cutoff_time.replace(tzinfo=None),
            )
            .values(updated_at=datetime.now(timezone.utc))
            .execution_options(synchronize_session="fetch")
        )

        result: Result = await self.session.execute(stmt)
        wishlist_item = result.scalars().all()

        if wishlist_item:
            return None

        irem = await self.create_obj(
            product_id=product_id,
            client_uuid=client_uuid,
            user_id=user_id,
        )
        return irem

    async def get_all_objs_by(
        # TODO сильное копирование DRY!!!
        self,
        client_uuid: UUID | None = None,
        user_id: UUID | None = None,
    ):
        or_conditions = []
        if client_uuid:
            or_conditions.append(self.model.client_uuid == client_uuid)
        if user_id:
            or_conditions.append(self.model.user_id == user_id)
        if not client_uuid and not user_id:
            return or_conditions

        stmt = (
            select(self.model)
            .where(self.model.is_active == True, or_(*or_conditions))
            .order_by(self.model.updated_at)
            .limit(50)
        )
        result: Result = await self.session.execute(stmt)
        wishlist_item = result.scalars().all()
        return wishlist_item
