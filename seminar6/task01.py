# Разработать API для управления списком пользователей с
# использованием базы данных SQLite. Для этого создайте
# модель User со следующими полями:
# ○ id: int (идентификатор пользователя, генерируется
# автоматически)
# ○ username: str (имя пользователя)
# ○ email: str (электронная почта пользователя)
# ○ password: str (пароль пользователя)

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import uvicorn


DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128))
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
app = FastAPI()

# API должно поддерживать следующие операции:
# ○ Получение списка всех пользователей: GET /users/
# ○ Получение информации о конкретном пользователе: GET /users/{user_id}/
# ○ Создание нового пользователя: POST /users/
# ○ Обновление информации о пользователе: PUT /users/{user_id}/
# ○ Удаление пользователя: DELETE /users/{user_id}/
# Для валидации данных используйте параметры Field модели User.
# Для работы с базой данных используйте SQLAlchemy и модуль databases.


class User(BaseModel):
    id: int
    username: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=8, max_length=32)


class UserIn(BaseModel):
    username: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=8, max_length=32)


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(username=user.username, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


# @app.get("/fake_users/{count}")
# async def create_note(count: int):
#     for i in range(count):
#         query = users.insert().values(username=f'user{i}', email=f'mail{i}@mail.ru', password=f'1552215{i}')
#         await database.execute(query)
#     return {'message': f'{count} fake users create'}

if __name__ == "__main__":
    uvicorn.run("task01:app", host="127.0.0.1", port=8000, reload=True)


