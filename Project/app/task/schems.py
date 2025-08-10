from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    discription: str
    id_user: int
