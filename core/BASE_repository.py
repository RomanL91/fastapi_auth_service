from typing import Type, TypeVar, Generic, Optional, List

from sqlalchemy.engine import Result
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete

T = TypeVar("T", bound=DeclarativeMeta)


class SQLAlchemyRepository(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_obj(self, **data) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        res: Result = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_all_objs(self, order_by=None) -> List[T]:
        stmt = select(self.model)
        if order_by:
            stmt = stmt.order_by(order_by)
        result: Result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_obj(self, **filter_by) -> Optional[T]:
        stmt = select(self.model).filter_by(**filter_by)
        try:
            res: Result = await self.session.execute(stmt)
            return res.scalar_one()
        except NoResultFound:
            return None

    async def update_obj(self, obj_id: str, **data) -> Optional[T]:
        stmt = (
            update(self.model).values(**data).filter_by(id=obj_id).returning(self.model)
        )
        res: Result = await self.session.execute(stmt)
        updated_obj = res.scalar_one_or_none()
        if updated_obj is None:
            raise ValueError(f"Object with id={obj_id} not found")
        return updated_obj

    async def delete_obj(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        if result.rowcount == 0:
            raise ValueError(f"Object with filters {filter_by} not found")
