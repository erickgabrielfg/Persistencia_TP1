from datetime import date
from pydantic import BaseModel


class PayRoll(BaseModel):
    id: int
    employeeId: int
    discounts: float
    netSalary: float
    grossSalary: float
    referenceMonth: date