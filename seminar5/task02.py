# Задание №2
# Создать API для получения списка фильмов по жанру. Приложение должно
# иметь возможность получать список фильмов по заданному жанру.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Movie с полями id, title, description и genre.
# Создайте список movies для хранения фильмов.
# Создайте маршрут для получения списка фильмов по жанру (метод GET).
# Реализуйте валидацию данных запроса и ответа.
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Genre(str, Enum):
    БОЕВИК = "боевик"
    ФАНТАСТИКА = "фантастика"
    МЕЛОДРАММА = "мелодрамма"
    КОМЕДИЯ = "комедия"
    ДЕТЕКТИВ = "детектив"


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: Genre

    def __repr__(self):
        return f'{self.id}. {self.title}, {self.description}, {self.genre}'


class MovieInf(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Genre


# movies = [{1, 'Rembo 1', 'Фильм с Сильвестором Сталлоне', 'боевик'},
#           {2, 'Rembo 2', 'Фильм с Сильвестором Сталлоне', 'боевик'},
#           {3, 'Gadjuka', 'Фильм с Сильвестором Сталлоне', 'боевик'},
#           {4, 'Тупой, еще тупее', 'Фильм с Джиммом Керри', 'комедия'},
#           {5, 'Она', None, 'мелодрамма'},
#           {6, 'Звездные войны', None, 'фантастика'},
#           {7, 'Спрут', None, 'детектив'},
#           {8, 'Rembo 3', None, 'боевик'},
#           ]
movies = []


@app.get("/movie/{genre}", response_model=list[Movie])
async def list_movies(genre):
    logger.info(f'Отработал GET запрос на чтение списка фильмов из жанра {genre}.')
    result = []
    for movie in movies:
        if movie.genre == genre:
            result.append(movie)
    return result


@app.post("/newmovie/")
async def create_task(newmovie: MovieInf):
    logger.info("Отработал POST запрос на добавление нового фильма.")
    movies.append(Movie(id=len(movies) + 1, title=newmovie.title, description=newmovie.description, genre=newmovie.genre))
    return {'New movie': movies[-1]}

if __name__ == '__main__':
    uvicorn.run(
        "task02:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )
