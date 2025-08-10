from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import HTMLResponse

from authx import RequestToken

from uvicorn import run
from typing import Annotated
from security.security import auth

from user.schems import UserSchema
from database.db import create_table_user, connect_database


router_user = APIRouter(prefix="/user", dependencies=[Depends(auth.get_token_from_request)])


@router_user.get("/")
def main():
    return HTMLResponse("<h1>User</h1>")


@router_user.get("/get", dependencies=[Depends(auth.access_token_required)])
def get_users():
    conn = connect_database()
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM user").fetchall()

    return {"users": [{"id_user": i["id_user"], "username": i["username"]} for i in users]}

@router_user.delete("/delete", dependencies=[Depends(auth.access_token_required)])
def delete_user(id_user: int):
    conn = connect_database()
    cur = conn.execute("DELETE FROM user WHERE id_user = ?", (id_user,))
    conn.commit()

    return {"msg": f"User {id_user} delete"}
