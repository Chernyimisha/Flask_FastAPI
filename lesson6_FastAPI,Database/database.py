# SQLite — это облегченная система управления реляционными базами данных на
# основе SQL.
# Чтобы создать соединение с базой данных, нам нужно определить конфигурацию
# базы данных и использовать библиотеку ORM (Object-Relational Mapping), такую как
# Tortoise ORM, SQLAlchemy или Peewee.
# 🔥 Важно! Если вы не устанавливали SQLAlchemy и databases раньше, выполните команды:
# pip install sqlalchemy
# pip install databases[aiosqlite]

# Подключение к PostgreSQL
# Если мы хотим зменить SQLite на PostgreSQL, достоточно заменить данные в
# константе подключения к БД:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"
# Указав тип базы данных, имя пользователя, пароль, хост и название базы данных
# мы установим с ней соединение.


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
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
)

# Внимание! По умолчанию SQLite разрешает взаимодействовать с ним
# только одному потоку, предполагая, что каждый поток будет обрабатывать
# независимый запрос. Это сделано для предотвращения случайного
# использования одного и того же соединения для разных вещей (для
# разных запросов). Но в FastAPI при использовании обычных функций (def)
# несколько потоков могут взаимодействовать с базой данных для одного и
# того же запроса, поэтому нам нужно сообщить SQLite, что он должен
# разрешать это с помощью connect_args={"check_same_thread": False}.
# Для баз данных других типов параметр connect_args не нужен!

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)

# Прежде чем работать над созданием API и проходить всю цепочку CRUD для
# клиента сгенерируем несколько тестовых пользователей в базе данных.


@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i}', email=f'mail{i}@mail.ru')
        await database.execute(query)
    return {'message': f'{count} fake users create'}


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


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

# curl -X 'POST' 'http://127.0.0.1:8000/users/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
# "name": "Alex", "email": "my@mail.ru"}'

# Создание API операций CRUD в FastAPI - это простой процесс. Мы можем
# использовать функции и методы Python для выполнения основных функций
# создания, чтения, обновления и удаления данных из базы данных. Мы можем
# протестировать наш API с помощью таких инструментов, как Postman или Swagger
# UI, чтобы убедиться, что он работает правильно.

if __name__ == "__main__":
    uvicorn.run("database:app", host="127.0.0.1", port=8000, reload=True)

