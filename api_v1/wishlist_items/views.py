from uuid import UUID

from fastapi import (
    status,
    APIRouter,
)

from api_v1.api_dependencies import UOF_Depends

# === Services
from app_wishlist_Items.wishlistitems_service import ItemsService

# === Schemas
from app_wishlist_Items.schemas import WishlistItemCreate, WishlistItemRead


router = APIRouter(tags=["wishlistitems"])


@router.post(
    "/add_wishlist",
    status_code=status.HTTP_201_CREATED,
    response_model=WishlistItemRead,
    summary="Добавить ID товара в избранное.",
    description="""
        <h1>К прочтению</h1>
        Данный endpoint для добавления товара в "избранное".<br>
        Пользователь или аноним, в зависимости от статуса авторизации, 
        могут отметить товар как "избранный".<br><hr>
        Исходя из этого, `user_id` не обязателен, однако, если ты его передаешь будь уверен, что такой есть в БД, иначе `400 = Unexpected data retrieval error`!<br>
        Но вот `client_uuid` - уникальный ID от клиентского кода **всегда должен быть**!<br><hr>
        Поле `product_id` - ID товара, который мы хотим добавить в "избранное".<br><hr>
        Зачем `is_active`?<br>
        - Всё просто, **добавляем** в "избранное" - **is_active: true**.<br>
        - **Удаляем** из "избранного" - **is_active: false**.<br><hr>
        <h3>
        Данный endpoint должен помочь не потерять данные пользовательского выбора.<br>
        Сохраняй выбор анонима и пока жив `client_uuid` на клиенте - будут доступны "избранные" товары.<br>
        Если есть `user_id` - подписывай "на лету" и теперь это закреплено за конкретным пользователем.
        </h3>
    """,
)
async def add_wishlist(
    uow: UOF_Depends,
    item: WishlistItemCreate,
):
    item_service = ItemsService(uow=uow)
    wishlist_item = await item_service.add_item_in_wishlist(item)
    return wishlist_item


@router.get(
    "/by_client_uuid_or_user_id",
    status_code=status.HTTP_200_OK,
    response_model=list[WishlistItemRead],
    summary="Получить список 'избранных' товаров. Подписать.",
    description="""
        Данный endpoint отдает список 'избранных' товаров.<br>
        Требуется `client_uuid` и/или `user_id` чтобы получить список.<br>
        Между query параметрами используется логическое `OR`, поэтому найдет 
        все 'избранные' товары, которые пользователь добавлял будучи авторизированным,
        а так же все товары которые были добавлены в 'избранное' с этого устройства (*client_uuid*).<br><hr>
        Есть еще один интересный кейс использования данного endpoint.<br>
        Если передаем `client_uuid` и `user_id` вместе, то все **WishlistItem** экземпляры, 
        которые имели user_id == null (так как сначала были добавлены анонимом с устройсва с client_uuid) 
        **подпишутся этим user_id**.
    """,
)
async def get_all_items_wishlist_by_client_uuid_or_user_id(
    uow: UOF_Depends,
    client_uuid: UUID | None = None,
    user_id: UUID | None = None,
):
    item_service = ItemsService(uow=uow)
    wishlist_items = await item_service.get_all_prod_by_client_uuid_or_user_id(
        client_uuid=client_uuid,
        user_id=user_id,
    )
    return wishlist_items
