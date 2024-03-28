from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from datetime import datetime


class Status(str, Enum):
    """Перечисление статусов задач"""
    DONE = 'Выполнен'
    IN_PROGRESS = 'Выполняется'


class UserIn(BaseModel):
    """Модель пользователя без id"""
    name: str = Field(..., max_length=25, min_length=3,
                      title='Задается name пользователя', pattern=r'^[а-яА-ЯёЁa-zA-Z]+$')
    surname: str = Field(..., max_length=25, min_length=3,
                         title='Задается surname пользователя', pattern=r'^[а-яА-ЯёЁa-zA-Z]+$')
    email: EmailStr = Field(..., title='Задается email пользователя')
    password: str = Field(..., title='Задается пароль пользователя')


class GoodsIn(BaseModel):
    """Модель товара без id"""
    name: str = Field(..., max_length=50, min_length=3,
                      title='Задается name товара', pattern=r'^[a-zA-Z0-9_-]+$')
    description: str = Field(..., max_length=1000)
    price: float


class OrderIn(BaseModel):
    """Модель заказа без id"""
    status: Status
    id_user: int = Field(..., title="user_id", ge=0)
    id_goods: int = Field(..., title="goods_id", ge=0)


class User(UserIn):
    """Модель пользователя с id"""
    id: int


class Goods(GoodsIn):
    """Модель товара c id"""
    id: int


class Order(OrderIn):
    """Модель заказа с id"""
    id: int
    date: datetime
