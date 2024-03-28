# Задание №1
# Создать API для управления списком задач. Приложение должно иметь
# возможность создавать, обновлять, удалять и получать список задач.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Task с полями id, title, description и status.
# Создайте список tasks для хранения задач.
# Создайте маршрут для получения списка задач (метод GET).
# Создайте маршрут для создания новой задачи (метод POST).
# Создайте маршрут для обновления задачи (метод PUT).
# Создайте маршрут для удаления задачи (метод DELETE).
# Реализуйте валидацию данных запроса и ответа.
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str

    def __repr__(self):
        return f'{self.id}. {self.title}, {self.description}, {self.status}'


class TaskInf(BaseModel):
    title: str
    description: Optional[str] = None
    status: str


@app.get("/tasks/")
async def read_tasks():
    logger.info('Отработал GET запрос на чтение списка задач.')
    result = {}
    for i, task in enumerate(tasks):
        result[i + 1] = task
    return {'List task': result}


@app.post("/newtask/")
async def create_task(newtask: TaskInf):
    logger.info("Отработал POST запрос на добавление новой задачи.")
    tasks.append(Task(id=len(tasks) + 1, title=newtask.title, description=newtask.description, status=newtask.status))
    return {'New task': tasks[-1]}

# example curl request:
# curl -X 'POST' 'http://127.0.0.1:8000/newtask/' -H 'accept: application/json' -H 'Content-Type: application/json
# ' -d '{"title": "Задача №1", "description": "Убрать мусор", "status": "Активна"}'

# example response:
# >>>{"New task":{"id":4,"title":"Задача №1","description":"Убрать мусор","status":"Активна"}}



@app.put("/edit_task/{task_id}")
async def update_task(task_id: int, newtask: TaskInf):
    logger.info(f"Отработал PUT запрос для item id = {task_id}.")
    if task_id <= len(tasks):
        old_task = tasks[task_id - 1]
        tasks[task_id] = Task(id=task_id, title=newtask.title, description=newtask.description, status=newtask.status)
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"old_task": old_task, "new_task": tasks[task_id]}

# example curl request:
# curl -X 'PUT' 'http://127.0.0.1:8000/edit_task/1' -H 'accept: application/json' -H 'Content-Type: application/js
# on' -d '{"title": "Задача №1", "description": "Убрать мусор", "status": "Неактивна"}'

# example response:
# >>> {"old_task":{"id":1,"title":"Задача №1","description":"Убрать мусор","status":"Активна"},
# >>> "new_task":{"id":1,"title":"Задача №1","description":"Убрать мусор","status":"Неактивна"}}


@app.delete("/del_items/{task_id}")
async def delete_task(task_id: int):
    logger.info(f"Отработал DELETE запрос для item id = {task_id}.")
    if task_id <= len(tasks):
        del_task = tasks[task_id - 1]
        del tasks[task_id - 1]
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return {'DELETE': f'Task {del_task} deleted'}

# example curl request:
# curl -X 'DELETE' 'http://127.0.0.1:8000/del_items/1' -H 'accept: application/json' -H 'Content-Type: application
# /json'

# example response:
# >>> {"DELETE":"Task id=1 title='Задача №1' description='Убрать мусор' status='Активна' deleted"}


if __name__ == '__main__':
    uvicorn.run(
        "task01:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )
