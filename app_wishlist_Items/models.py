from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.BASE_model import Base


class WishlistItem(Base):
    """
    Модель списка избранных товаров
    """

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    client_uuid: Mapped[UUID] = mapped_column(
        nullable=True,
        index=True,
    )

    # Связь
    user: Mapped["User"] = relationship(  # type: ignore
        back_populates="wishlist_items",
    )


class ViewedProduct(Base):
    """
    Модель просмотренных товаров
    """

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    client_uuid: Mapped[UUID] = mapped_column(
        nullable=True,
        index=True,
    )

    # Связь
    user: Mapped["User"] = relationship(  # type: ignore
        back_populates="vieved_products",
    )
