from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from authx import AuthX
from typing import Annotated
from hashlib import sha256

from security.config import config
from database.db import connect_database, create_all


auth = AuthX(config=config)

router_scrt = APIRouter()

@router_scrt.post('/register')
async def register(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Регистрация пользователя.
    """
##    create_all() #Создание таблиц в базеданных
    conn = connect_database()
    cursor = conn.cursor()
    user_data = {
        "username": user.username,
        "password": sha256(str(user.password).encode()).hexdigest()
    }
    user_exsits = cursor.execute("SELECT username FROM user WHERE username = ?", (user.username,)).fetchone()
    if user_exsits:
        raise HTTPException(detail=f"Username {user.username} exists database!", status_code=409)

    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?);",
    (user_data.get("username"), user_data.get("password")))
    conn.commit()

    return {"user": user.username}


@router_scrt.get('/login')
async def login(username: str, password: str, response: Response):
    """
    Аутентификация пользователя
    """
    conn = connect_database()
    cursor = conn.cursor()
    user_db = cursor.execute("SELECT * FROM user WHERE username = ?", (str(username),)).fetchone()
    try:
        if username == user_db["username"] and sha256(password.encode()).hexdigest() == user_db["password"]:
            token = auth.create_access_token(uid=username)
            response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
            return {"access_token": token}
    except:
        raise HTTPException(401, detail={"message": "Invalid credentials"})
