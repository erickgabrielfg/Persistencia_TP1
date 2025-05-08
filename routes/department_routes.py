from fastapi import APIRouter, HTTPException
from typing import List
from model.department import Department
from services.department_service import ler_dados_csv_department, escrever_dados_csv_department
from logger import logger

router = APIRouter()

@router.post("/departments", response_model=Department)
def create_department(department: Department):
    departments = ler_dados_csv_department()
    departments.append(department)
    escrever_dados_csv_department(departments)
    logger.info("Departamento criado com sucesso")
    return department

@router.get("/departments", response_model=List[Department])
def get_departments():
    logger.info("Retornando todos os departamentos")
    return ler_dados_csv_department()

@router.get("/departments/{department_id}", response_model=Department)
def get_department(department_id: int):
    for d in ler_dados_csv_department():
        if d.id == department_id:
            logger.info(f"Retornando departamento de ID: {department_id}")
            return d
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@router.put("/departments/{department_id}", response_model=Department)
def update_department(department_id: int, department: Department):
    departments = ler_dados_csv_department()
    for i, d in enumerate(departments):
        if d.id == department_id:
            departments[i] = department
            escrever_dados_csv_department(departments)
            logger.info(f"Departamento com ID {department_id} atualizado com sucesso")
            return department
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@router.delete("/departments/{department_id}")
def delete_department(department_id: int):
    departments = ler_dados_csv_department()
    for i, d in enumerate(departments):
        if d.id == department_id:
            del departments[i]
            escrever_dados_csv_department(departments)
            logger.info(f"Departamento com ID {department_id} deletado com sucesso")
            return {"message": "Departamento deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Departamento não encontrado")
