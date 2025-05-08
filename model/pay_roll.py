from datetime import date
from pydantic import BaseModel


class PayRoll(BaseModel):
    id: int
    discounts: float
    net_salary: float
    gross_salary: float
    reference_month: date