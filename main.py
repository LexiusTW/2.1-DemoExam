from datetime import date
from typing import Annotated, Literal, Optional
from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Orders(BaseModel):
    id: int
    dateStart: date
    endDate: Optional[date] = None
    device: str
    problemType: str
    description: str
    client: str
    status: Literal["в ожидании", "в работе", "выполнено"] = "в ожидании"
    master: Optional[str] = ""
    comments: Optional[list] = []

class UpdateOrdersDTO(BaseModel):
    id: int
    status: Optional[str] = ""
    description: Optional[str] = ""
    master: Optional[str] = ""
    comment: Optional[str] = ""

repo = [Orders(id = 1,
    dateStart = "2020-02-20",
    device = "Телефон",
    problemType = "Окислились контакты",
    description = "Перестал заряжаться после поподания в воду",
    client = "Игорь",
    status = "в ожидании",
    master = "Максим"),
    Orders(id = 2,
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

@app.get("/orders")
def get_orders(param = None):
    global message
    buffer = message
    message = ""
    if(param):
        return {"repo" : [o for o in repo if o.id == int(param)], "message" : buffer}
    return {"repo" : repo, "message" : buffer}

@app.post("/")
def add_order(order: Annotated[Orders, Form()]):
    repo.append(order)
    return {"status-code": 200, "message": "Заявка успешно добавлена"}

@app.post("/update")
def update_order(order: Annotated[UpdateOrdersDTO, Form()]):
    global message
    for o in repo:
        if order.id == o.id:
            if o.status != order.status:
                o.status = order.status
                message += f"Статус заявки №{o.id} изменен\n"
                if order.status == "выполнена":
                    message += f"Заявка №{o.id} завершена\n"
                    o.endDate = date.today()
            o.comments.append(order.comment)
            o.description = order.description
            o.master = order.master
        return {"status-code": 200, "message": "Данные обновлены"}
    
def complete_orders():
    return [o for o in repo if o.status == "выполнена"]

def count_complete():
    return len(complete_orders())

def problem_type():
    dict = {}
    for o in repo:
        if o.problemType in dict.keys():
            dict[o.problemType] += 1
        else:
            dict[o.problemType] = 1
    return dict

def avg_time():
    times = []
    for ord in complete_orders():
        times.append(ord.endDate - ord.startDate)
    timesum = sum([t.days for t in times])
    ordCount = count_complete()
    result = timesum/ordCount
    return result

@app.get("/statistic")
def get_stat():
    return {"count_complete" : count_complete(),
            "problem_type" : problem_type(),
            "avg_time" : avg_time()}