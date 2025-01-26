from uuid import UUID

from fastapi import (
    status,
    APIRouter,
)

from api_v1.api_dependencies import UOF_Depends

# === Services
from app_wishlist_Items.wishlistitems_service import ItemsService

# === Schemas
from app_wishlist_Items.schemas import VievedProductsCreate, VievedProductsRead


router = APIRouter(tags=["vieweditems"])


@router.post(
    "/add_viewed",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Добавить ID товара в просмотренные товары.",
    description="""
        <h1>К прочтению</h1>
        Данный endpoint для добавления товара в "просмотренные".<br>
        Пользователь или аноним, в зависимости от статуса авторизации,
        могут просматривать карточки товаров.<br>
        Ожидается, что при переходе на карточку товара, клиентский код будет
        делать **POST** запрос, для того чтобы отметить действия.<br>
        Ожидается, что `client_uuid` и `product_id` будут предоставлены обязательно!<br>
        Если же педеатеся `user_id` - **убедись, что такой есть в БД, иначе Unexpected data retrieval error (400)**.<br><hr>
        **`Если все верно - в БД будет запись и возврашен 204 код статуса.`** <br><hr>
        Стоит отметить, что **используется магическое значение 30, а именно 30 минут** - именно 
        на такое значение происходит фильтрация: если конкретный пользователь/аноним в течении 30 минут
        постоянно проваливается в одну и ту же карточку - новая запись не создается, код ответа 204.
    """,
)
async def add_viewed(
    uow: UOF_Depends,
    item: VievedProductsCreate,
):
    item_service = ItemsService(uow=uow)
    await item_service.add_item_in_viewedlist(item)
    return None


@router.get(
    "/by_client_uuid_or_user_id",
    status_code=status.HTTP_200_OK,
    response_model=list[VievedProductsRead],
    summary="Получить список 'просмотренных' товаров. Подписать.",
    description="""
        Данный endpoint отдает список 'просмотренных' товаров.<br>
        Требуется `client_uuid` и/или `user_id` чтобы получить список.<br>
        Между query параметрами используется логическое `OR`, поэтому найдет
        все 'просмотренные' товары, которые пользователь добавлял будучи авторизированным,
        а так же все товары которые были добавлены в 'просмотренное' с этого устройства (*client_uuid*).<br><hr>
        Есть еще один интересный кейс использования данного endpoint.<br>
        Если передаем `client_uuid` и `user_id` вместе, то все **ViewedProduct** экземпляры,
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
    wishlist_items = await item_service.get_all_prod_viewed_by_client_uuid_or_user_id(
        client_uuid=client_uuid,
        user_id=user_id,
    )
    return wishlist_items
