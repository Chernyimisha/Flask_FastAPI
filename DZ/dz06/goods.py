from fastapi import APIRouter, HTTPException
from database import database, goods
from models import Goods, GoodsIn
from typing import List


router = APIRouter()


@router.get("/goods/", response_model=List[Goods])
async def get_all_goods() -> List[Goods]:
    """Получение списка всех товаров: GET /goods/"""
    query = goods.select()
    goods_list = await database.fetch_all(query)
    if goods_list:
        return goods_list
    raise HTTPException(status_code=404, detail="Нет ни одного товара")


@router.get("/goods/{goods_id}", response_model=Goods)
async def get_single_goods(goods_id: int) -> Goods:
    """Получение информации о конкретном товаре: GET /goods/{goods_id}/"""
    query = goods.select().where(goods.c.id == goods_id)
    db_goods = await database.fetch_one(query)
    if db_goods:
        return db_goods
    raise HTTPException(status_code=404, detail="Товар не найден")


@router.post("/goods/", response_model=Goods)
async def create_goods(good: GoodsIn) -> dict:
    """Создание нового товара: POST /goods/"""
    good_dict = good.dict()
    query = goods.insert().values(**good_dict)
    good_id = await database.execute(query)
    return {**good_dict, 'id': good_id}


@router.put("/goods/{goods_id}", response_model=Goods)
async def update_goods(goods_id: int, good: GoodsIn) -> Goods:
    """Обновление информации о товаре: PUT /goods/{goods_id}/"""
    query = goods.select().where(goods.c.id == goods_id)
    db_goods = await database.fetch_one(query)
    if db_goods:
        updated_goods = good.dict(exclude_unset=True)
        query = goods.update().where(goods.c.id == goods_id).values(updated_goods)
        await database.execute(query)
        return await database.fetch_one(goods.select().where(goods.c.id == goods_id))
    raise HTTPException(status_code=404, detail="Товар не найден")


@router.delete("/goods/{goods_id}")
async def delete_goods(goods_id: int) -> dict:
    """Удаление товара: DELETE /goods/{goods_id}/"""
    query = goods.select().where(goods.c.id == goods_id)
    db_goods = await database.fetch_one(query)
    if db_goods:
        query = goods.delete().where(goods.c.id == goods_id)
        await database.execute(query)
        return {'detail': f'Товар с id={db_goods.id} удален'}
    raise HTTPException(status_code=404, detail="Товар не найден")