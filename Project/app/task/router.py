from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import HTMLResponse

from uvicorn import run
from typing import Annotated, Any

from security.security import auth
from task.schems import TaskSchema
from database.db import create_table_task, connect_database


router_task = APIRouter(prefix="/task", dependencies=[Depends(auth.get_token_from_request)])


@router_task.get("/")
def main():
    return HTMLResponse("<h1>Task</h1>")

@router_task.post("/create", dependencies=[Depends(auth.access_token_required)])
def create_task(task: Annotated[TaskSchema, Depends(TaskSchema)]) -> Any:
    """
    Создание задачи пользователя.
    """
    conn = connect_database()
    cur = conn.cursor()
    cur.execute("INSERT INTO task (title, discription, fk_user) VALUES (?, ?, ?);",
    (task.title, task.discription, task.id_user))
    conn.commit()

    return {"msg": task}

@router_task.get("/get", dependencies=[Depends(auth.access_token_required)])
def get_tasks(id_user: int) -> Any:
    """
    Получения списка задач пользователя.
    """
    conn = connect_database()
    cur = conn.cursor()
    tasks = cur.execute("SELECT * FROM task WHERE fk_user = ?",
    (id_user,)).fetchall()

    return {"tasks": tasks}

@router_task.delete("/delete", dependencies=[Depends(auth.access_token_required)])
def delete_task(id_user: int, id_task:int) -> Any:
    """
    Удаление задачи у пользователя.
    """
    conn = connect_database()
    cur = conn.execute("DELETE FROM task WHERE fk_user = ? AND id_task = ?",
    (id_user, id_task))
    conn.commit()

    return {"msg": f"Task {id_task} delete for user {id_user}"}
