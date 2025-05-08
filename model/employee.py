from datetime import date
from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    id_department: int
    name: str
    cpf: str
    position: str
    admission_date: date