from fastapi import APIRouter, HTTPException
from typing import List
from model.department import Department
from services.department_service import read_csv_department, write_csv_department
from logger import logger
from fastapi.responses import Response
from io import BytesIO, StringIO
import zipfile
import csv

router = APIRouter(prefix="/departments", tags=["Departamentos"])

@router.post("/departments", response_model=Department)
def create_department(department: Department):
    departments = read_csv_department()
    departments.append(department)
    write_csv_department(departments)
    logger.info("Departamento criado com sucesso")
    return department

@router.get("/departments", response_model=List[Department])
def get_departments():
    logger.info("Retornando todos os departamentos")
    return read_csv_department()

@router.get("/departments/{department_id}", response_model=Department)
def get_department(department_id: int):
    for d in read_csv_department():
        if d.id == department_id:
            logger.info(f"Retornando departamento de ID: {department_id}")
            return d
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@router.put("/departments/{department_id}", response_model=Department)
def update_department(department_id: int, department: Department):
    departments = read_csv_department()
    for i, d in enumerate(departments):
        if d.id == department_id:
            departments[i] = department
            write_csv_department(departments)
            logger.info(f"Departamento com ID {department_id} atualizado com sucesso")
            return department
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@router.delete("/departments/{department_id}")
def delete_department(department_id: int):
    departments = read_csv_department()
    for i, d in enumerate(departments):
        if d.id == department_id:
            del departments[i]
            write_csv_department(departments)
            logger.info(f"Departamento com ID {department_id} deletado com sucesso")
            return {"message": "Departamento deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@router.get("/departments/name", response_model=List[Department])
def get_department_by_name(name: str):
    departments  = read_csv_department()
    if not name:
        raise HTTPException(status_code=400, detail="Nome do departamento não pode ser vazio")
    filtered_departments = [d for d in departments if d.name == name]
    if not filtered_departments:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    logger.info(f"Retornando departamentos com o nome: {name}")
    return filtered_departments

@router.get("departments/zip")
def get_departments_zip():
    departments = read_csv_department()
    if not departments:
        raise HTTPException(status_code=404, detail="Nenhum departamento encontrado")

    # Gera o CSV em memória usando StringIO (texto)
    csv_string_io = StringIO()
    writer = csv.DictWriter(csv_string_io, fieldnames=departments[0].dict().keys())
    writer.writeheader()
    for dept in departments:
        writer.writerow(dept.dict())

    # Cria o arquivo zip com o CSV dentro
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("departments.csv", csv_string_io.getvalue())

    zip_buffer.seek(0)

    logger.info("department.csv convertido para .zip")

    return Response(
        content=zip_buffer.read(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=departments.zip"}
    )


