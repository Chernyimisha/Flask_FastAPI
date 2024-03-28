# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str

    def __repr__(self):
        return f'{self.id}. {self.title}, {self.description}, {self.status}'


class TaskInf(BaseModel):
    title: str
    description: str
    status: bool


@app.get("/tasks/")
async def read_tasks():
    logger.info('Отработал GET запрос на чтение списка задач.')
    result = {}
    for i, task in enumerate(tasks):
        result[i + 1] = task
    return {'List task': result}


@app.get("/tasks/{task_id}")
async def read_task(task_id):
    logger.info(f'Отработал GET запрос на чтение задачи №: {task_id}.')
    if task_id <= len(tasks):
        return {'task № {id}': result}
    else:
        raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks/")
async def create_task(newtask: TaskInf):
    logger.info("Отработал POST запрос на добавление новой задачи.")
    tasks.append(Task(id=len(tasks) + 1,
                      title=newtask.title,
                      description=newtask.description,
                      status='Выполнена' if newtask.status is True else 'Не выполнена'))
    return {'New task': tasks[-1]}


# example curl request:
# curl -X 'POST' 'http://127.0.0.1:8000/tasks/' -H 'accept: application/json' -H 'Content-Type: application/json
# ' -d '{"title": "Задача №1", "description": "Убрать мусор", "status": false}'

# example response:
# >>>{"New task":{"id":1,"title":"Задача №1","description":"Убрать мусор","status":"Не выполнена"}}


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, newtask: TaskInf):
    logger.info(f"Отработал PUT запрос для задачи id = {task_id}.")
    if task_id <= len(tasks):
        old_task = tasks[task_id - 1]
        tasks[task_id - 1] = Task(id=task_id,
                                  title=newtask.title,
                                  description=newtask.description,
                                  status='Выполнена' if newtask.status is True else 'Не выполнена')
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"old_task": old_task, "new_task": tasks[task_id - 1]}


# example curl request:
# curl -X 'PUT' 'http://127.0.0.1:8000/tasks/1' -H 'accept: application/json' -H 'Content-Type: application/js
# on' -d '{"title": "Задача №1", "description": "Убрать мусор", "status": "true"}'

# example response:
# >>> {"old_task":{"id":1,"title":"Задача №1","description":"Убрать мусор","status":"Не выполнена"},
# >>> "new_task":{"id":1,"title":"Задача №1","description":"Убрать мусор","status":"Выполнена"}}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    logger.info(f"Отработал DELETE запрос для item id = {task_id}.")
    if task_id <= len(tasks):
        del_task = tasks[task_id - 1]
        del tasks[task_id - 1]
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return {'DELETE': f'Task {del_task} deleted'}


# example curl request:
# curl -X 'DELETE' 'http://127.0.0.1:8000/tasks/1' -H 'accept: application/json' -H 'Content-Type: application
# /json'

# example response:
# >>> {"DELETE":"Task id=1 title='Задача №1' description='Убрать мусор' status='Выполнена' deleted"}


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )
