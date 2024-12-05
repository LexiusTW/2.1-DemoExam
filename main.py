from datetime import date
from typing import Annotated, Literal
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class Orders(BaseModel):
    id: int
    dateStart: date
    device: str
    problemType: str
    description: str
    client: str
    status: Literal["в ожидании", "в работе", "выполнено"] = "в ожидании"

repo = []

@app.post("/")
def add_order(order: Annotated[Orders, Form()]):
    repo.append(order)
    return {"status-code": 200, "message": "Заявка успешно добавлена"}