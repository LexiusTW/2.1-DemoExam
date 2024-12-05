from datetime import date
from typing import Annotated, Literal, Optional
from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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

repo = [Orders(id = 1,
    dateStart = "2020-02-20",
    device = "Телефон",
    problemType = "Окислились контакты",
    description = "Перестал заряжаться после поподания в воду",
    client = "Игорь",
    status = "в ожидании",
    master = "Максим")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

message = ""
ifUpdateStatus = False

@app.get("/")
def get_orders():
    if ifUpdateStatus == True:
        buffer = message
        message = ""
        ifUpdateStatus = False
        return repo, buffer
    return repo

@app.get("/search/{id}")
def search_order(id: int):
    return [o for o in repo if o.id == id]

@app.post("/")
def add_order(order: Annotated[Orders, Form()]):
    repo.append(order)
    return {"status-code": 200, "message": "Заявка успешно добавлена"}

@app.post("/update")
def update_order(order: Annotated[UpdateOrdersDTO, Form()]):
    global message
    global ifUpdateStatus
    for o in repo:
        if order.id == o.id:
            if o.status != order.status:
                o.status = order.status
                message = f"Статус заявки №{o.id} изменен"
                ifUpdateStatus = True
            o.description = order.description
            o.master = order.master
        return {"status-code": 200, "message": "Данные обновлены"}