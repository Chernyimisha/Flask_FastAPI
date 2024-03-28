from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    return templates.TemplateResponse("item.html", {"request": request, "name": name})


# В этом примере мы импортируем класс Jinja2Templates из модуля
# FastAPI.templating. Мы создаем экземпляр этого класса и передаем каталог, в
# котором расположены наши шаблоны. В функции read_item мы получаем параметр
# имени из пути URL и генерируем динамический HTML-ответ, используя шаблон
# Jinja2 (item.html). Шаблон получает объект запроса и параметр имени в качестве
# переменных контекста для отображения в ответе HTML.
