from pydantic import BaseModel

class Department(BaseModel):
    id: int
    name: str
    manager: str
    location: str
    number_of_employees: int