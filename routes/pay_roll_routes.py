from fastapi import HTTPException
from typing import List
from fastapi import APIRouter
from model.pay_roll import PayRoll
from logger import logger
from services.pay_roll_service import read_csv_pay_roll, write_csv_pay_roll
from services.employee_service import get_all_employees_ids

router = APIRouter()

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