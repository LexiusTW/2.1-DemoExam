from datetime import date
from typing import Literal
from fastapi import FastAPI
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