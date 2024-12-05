from datetime import date
from typing import Annotated, Literal, Optional
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
    master: Optional[str] = ""

class UpdateOrdersDTO(BaseModel):
    id: int
    status: Optional[str] = ""
    description: Optional[str] = ""
    master: Optional[str] = ""

repo = []

@app.post("/")
def add_order(order: Annotated[Orders, Form()]):
    repo.append(order)
    return {"status-code": 200, "message": "Заявка успешно добавлена"}

@app.post("/")
def update_order(order: Annotated[UpdateOrdersDTO, Form()]):
    for o in repo:
        if order.id == o.id:
            o.status = order.status
            o.description = order.description
            o.master = order.master
        return {"status-code": 200, "message": "Данные обновлены"}