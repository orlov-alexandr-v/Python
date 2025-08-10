from fastapi import FastAPI, Depends

from uvicorn import run
from authx import AuthX

from user.router import router_user
from task.router import router_task
from security.security import router_scrt, auth


app = FastAPI(docs_url='/')
auth.handle_errors(app=app)

#Роутер пользователя
app.include_router(router=router_user, tags=["user"], dependencies=[Depends(auth.access_token_required)])
#Роутер задач
app.include_router(router=router_task, tags=["task"], dependencies=[Depends(auth.access_token_required)])
#Роутер защиты
app.include_router(router=router_scrt, tags=["security"])


if __name__ == "__main__":
    run("main:app", host="localhost", port=8000, reload=True)
