from fastapi import APIRouter, HTTPException
from database import database, orders, users, goods
from models import Order, OrderIn
from datetime import datetime
from typing import List


router = APIRouter()


async def validation_order(order: OrderIn):
    order_dict = order.dict()
    query = users.select().where(users.c.id == order_dict['id_user'])
    db_user = await database.fetch_one(query)
    query = goods.select().where(goods.c.id == order_dict['id_goods'])
    db_goods = await database.fetch_one(query)
    if db_user and db_goods:
        return True
    elif db_user:
        raise HTTPException(status_code=404, detail="Товар не найден")
    elif db_goods:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    else:
        raise HTTPException(status_code=404, detail="Пользователь и товар не найден")


@router.get("/orders/", response_model=List[Order])
async def get_all_orders() -> List[Order]:
    """Получение списка всех заказов: GET /orders/"""
    query = orders.select()
    orders_list = await database.fetch_all(query)
    if orders_list:
        return orders_list
    raise HTTPException(status_code=404, detail="Нет ни одного заказа")


@router.get("/orders/{order_id}", response_model=Order)
async def get_single_order(order_id: int) -> Order:
    """Получение информации о конкретном заказе: GET /orders/{order_id}/"""
    query = orders.select().where(orders.c.id == order_id)
    db_order = await database.fetch_one(query)
    if db_order:
        return db_order
    raise HTTPException(status_code=404, detail="Заказ не найден")


@router.post("/orders/", response_model=Order)
async def create_order(order: OrderIn) -> dict:
    """Создание нового заказа: POST /orders/"""
    if await validation_order(order):
        order_dict = order.dict()
        order_dict['date'] = datetime.now()
        query = orders.insert().values(**order_dict)
        order_id = await database.execute(query)
        return {**order_dict, 'id': order_id}


@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderIn) -> Order:
    """Обновление информации о заказе: PUT /orders/{order_id}/"""
    query = orders.select().where(orders.c.id == order_id)
    db_order = await database.fetch_one(query)
    if await validation_order(order) and db_order:
        updated_order = order.dict(exclude_unset=True)
        updated_order['date'] = datetime.now()
        query = orders.update().where(orders.c.id == order_id).values(updated_order)
        await database.execute(query)
        return await database.fetch_one(orders.select().where(orders.c.id == order_id))
    raise HTTPException(status_code=404, detail="Заказ не найден")


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int) -> dict:
    """Удаление товара: DELETE /orders/{order_id}/"""
    query = orders.select().where(orders.c.id == order_id)
    db_order = await database.fetch_one(query)
    if db_order:
        query = orders.delete().where(orders.c.id == order_id)
        await database.execute(query)
        return {'detail': f'Заказ с id={db_order.id} удален'}
    raise HTTPException(status_code=404, detail="Заказ не найден")

