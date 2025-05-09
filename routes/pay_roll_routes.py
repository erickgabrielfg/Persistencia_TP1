from fastapi import HTTPException
from typing import List
from fastapi import APIRouter
from model.pay_roll import PayRoll
from logger import logger
from services.pay_roll_service import read_csv_pay_roll, write_csv_pay_roll
from services.employee_service import get_all_employees_ids
from fastapi.responses import Response
from io import BytesIO, StringIO
import zipfile
import csv

router = APIRouter(prefix="/pay_rolls", tags=["Folha de Pagamentos"])

@router.post("/pay_roll", response_model=PayRoll)
def create_pay_roll(pay_roll: PayRoll):
    pay_rolls = read_csv_pay_roll()

    for employee_id in pay_roll.employees:
        if not any(employee_id == emp_id for emp_id in get_all_employees_ids()):
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    pay_rolls.append(pay_roll)
    write_csv_pay_roll(pay_rolls)
    logger.info(f"Folha de pagamento com ID {pay_roll.id} adicionada com sucesso")
    return pay_roll

@router.get("/pay_rolls", response_model=List[PayRoll])
def get_pay_rolls():
    logger.info("Retornando todas as folhas de pagamento")
    return read_csv_pay_roll()

@router.get("/pay_roll/{pay_roll_id}", response_model=PayRoll)
def get_pay_roll(pay_roll_id: int):
    for pr in read_csv_pay_roll():
        if pr.id == pay_roll_id:
            logger.info(f"Retornando folha de pagamento com ID: {pay_roll_id}")
            return pr
    raise HTTPException(status_code=404, detail="Folha de Pagamento não encontrada")

@router.put("/pay_roll/{pay_roll_id}", response_model=PayRoll)
def update_pay_roll(pay_roll_id: int, pay_roll: PayRoll):
    pay_rolls = read_csv_pay_roll()

    for employee_id in pay_roll.employees:
        if not any(employee_id == emp_id for emp_id in get_all_employees_ids()):
            raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    for i, pr in enumerate(pay_rolls):
        if pr.id == pay_roll_id:
            pay_rolls[i] = pay_roll
            write_csv_pay_roll(pay_rolls)
            logger.info(f"Folha de Pagamento com ID {pay_roll_id} atualizada com sucesso")
            return pay_roll
    raise HTTPException(status_code=404, detail="Folha de Pagamento não encontrada")

@router.delete("/pay_rolls/{pay_roll_id}")
def delete_pay_roll(pay_roll_id: int):
    pay_rolls = read_csv_pay_roll()

    for i, pr in enumerate(pay_rolls):
        if pr.id == pay_roll_id:
            del pay_rolls[i]
            write_csv_pay_roll(pay_rolls)
            logger.info(f"Folha de pagamento com ID {pay_roll_id} deletada com sucesso")
            return {"message": "Folha de pagamento deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Folha de pagamento não encontrada")

@router.get("pay_roll/zip")
def get_pay_roll_zip():
    departments = read_csv_pay_roll()
    if not departments:
        raise HTTPException(status_code=404, detail="Nenhuma folha de pagamento encontrada")

    csv_string_io = StringIO()
    writer = csv.DictWriter(csv_string_io, fieldnames=departments[0].dict().keys())
    writer.writeheader()
    for dept in departments:
        writer.writerow(dept.dict())

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("pay_roll.csv", csv_string_io.getvalue())

    zip_buffer.seek(0)

    logger.info("pay_roll.csv convertido para .zip")

    return Response(
        content=zip_buffer.read(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=pay_roll.zip"}
    )


