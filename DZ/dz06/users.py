from fastapi import APIRouter, HTTPException
from tools import get_password_hash
from sqlalchemy import select, delete, insert, update
from database import database, users
from models import User, UserIn
from typing import List


router = APIRouter()


@router.get("/users/", response_model=List[User])
async def get_all_users() -> List[User]:
    """Получение списка всех пользователей: GET /users/"""
    query = users.select()
    users_list = await database.fetch_all(query)
    if users_list:
        return users_list
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


@router.get("/users/{user_id}", response_model=User)
async def get_single_user(user_id: int) -> User:
    """Получение информации о конкретном пользователе: GET /users/{user_id}/"""
    query = users.select().where(users.c.id == user_id)
    db_user = await database.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.post("/users/", response_model=User)
async def create_user(user: UserIn) -> dict:
    """Создание нового пользователя: POST /users/"""
    hashed_password = await get_password_hash(user.password)
    user_dict = user.dict()
    user_dict['password'] = hashed_password
    query = users.insert().values(**user_dict)
    user_id = await database.execute(query)
    return {**user_dict, 'id': user_id}


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserIn) -> User:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = users.select().where(users.c.id == user_id)
    db_user = await database.fetch_one(query)
    if db_user:
        updated_user = user.dict(exclude_unset=True)
        if 'password' in updated_user:
            updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = users.update().where(users.c.id == user_id).values(updated_user)
        await database.execute(query)
        return await database.fetch_one(users.select().where(users.c.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{user_id}/"""
    query = users.select().where(users.c.id == user_id)
    db_user = await database.fetch_one(query)
    if db_user:
        query = users.delete().where(users.c.id == user_id)
        await database.execute(query)
        return {'detail': f'Пользователь с id={db_user.id} удален'}
    raise HTTPException(status_code=404, detail="Пользователь не найден")
