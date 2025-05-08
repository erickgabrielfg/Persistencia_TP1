from fastapi import APIRouter, HTTPException
from typing import List
from model.employee import Employee
from services.employee_service import ler_dados_csv_employee, escrever_dados_csv_employee
from services.department_service import ler_dados_csv_department
from logger import logger

router = APIRouter()

@router.post("/employee", response_model=Employee)
def create_employee(employee: Employee):
    if not any(d.id == employee.id_department for d in ler_dados_csv_department()):
        raise HTTPException(status_code=400, detail="Departamento não encontrado")
    employees = ler_dados_csv_employee()
    employees.append(employee)
    escrever_dados_csv_employee(employees)
    logger.info("Funcionário criado com sucesso")
    return employee

@router.get("/employees", response_model=List[Employee])
def get_employees():
    logger.info("Retornando todos os funcionários")
    return ler_dados_csv_employee()

@router.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    for e in ler_dados_csv_employee():
        if e.id == employee_id:
            logger.info(f"Retornando funcionário de ID: {employee_id}")
            return e
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")

@router.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: Employee):
    if not any(d.id == employee.id_department for d in ler_dados_csv_department()):
        raise HTTPException(status_code=400, detail="Departamento não encontrado")
    employees = ler_dados_csv_employee()
    for i, e in enumerate(employees):
        if e.id == employee_id:
            employees[i] = employee
            escrever_dados_csv_employee(employees)
            logger.info(f"Funcionário com ID {employee_id} atualizado com sucesso")
            return employee
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")

@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    employees = ler_dados_csv_employee()
    for i, e in enumerate(employees):
        if e.id == employee_id:
            del employees[i]
            escrever_dados_csv_employee(employees)
            logger.info(f"Funcionário com ID {employee_id} deletado com sucesso")
            return {"message": "Funcionário deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")