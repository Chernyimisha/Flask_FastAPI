from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# Этот код создает две конечные точки: одну для корневого URL-адреса, другую для
# URL-адреса /items/{item_id}. Функции read_root() и read_item() обрабатывают
# GET-запросы и возвращают JSON-объекты.


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Этот код создает конечную точку для URL-адреса /items/{item_id}, которая
# принимает параметр item_id типа int и параметр q типа str со значением по
# умолчанию None. Если параметр q задан, функция возвращает JSON-объект с
# обоими параметрами, иначе — только с item_id.
# Мы также можем определить несколько параметров URL-адреса в пути, например
# /users/{user_id}/orders/{order_id}, а затем определить соответствующие параметры в
# функции для доступа к ним.


@app.get("/users/{user_id}/orders/{order_id}")
async def read_item(user_id: int, order_id: int):
    # обработка данных
    return {"user_id": user_id, "order_id": order_id}


# Использование параметров запроса с FastAPI может быть любым удобным для
# решения поставленной задачи.


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# В этом примере мы определяем новый маршрут /items/, который принимает два
# параметра запроса skip и limit. Значения по умолчанию для этих параметров равны
# 15
# 0 и 10 соответственно. Когда мы вызываем этот маршрут без каких-либо
# параметров запроса, он возвращает значения по умолчанию.
# Например перейдя по адресу http://127.0.0.1:8000/items/ получим json c {"skip": 0,
# "limit": 10}.
# Мы также можем передать параметры запроса в URL-адресе, например
# http://127.0.0.1:8000/items/?skip=20&limit=30. В таком случае ответ будет
# следующим json объектом {"skip": 20, "limit": 30}.


# Форматирование ответов API
# FastAPI позволяет форматировать ответы API в различных форматах, например, в
# JSON или HTML. Для этого нужно использовать соответствующие функции модуля
# fastapi.responses.

# ● HTML текст


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello World</h1>"


# Этот код создает конечную точку для корневого URL-адреса, которая возвращает
# HTML-страницу с текстом "Hello World". Функция read_root() использует класс
# HTMLResponse для форматирования ответа в HTML.

# ● JSON объект


@app.get("/message")
async def read_message():
    message = {"message": "Hello World"}
    return JSONResponse(content=message, status_code=200)


# В этом примере мы импортируем класс JSONResponse из модуля FastAPI.responses.
# Внутри функции read_message мы определяем словарь, содержащий ключ
# сообщения со значением «Hello World». Затем мы возвращаем объект
# JSONResponse со словарем сообщений в качестве содержимого и кодом состояния
# 200.
