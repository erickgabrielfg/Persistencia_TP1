from fastapi import APIRouter, HTTPException
from typing import List
from model.pay_roll import PayRoll
from services.pay_roll_service import escrever_dados_csv_pay_roll, ler_dados_csv_pay_roll
from logger import logger

router = APIRouter()

@router.post("/pay_roll", response_model=PayRoll)
def create_pay_roll(pay_roll: PayRoll):
    pay_rolls = ler_dados_csv_pay_roll()
    pay_rolls.append(pay_roll)
    escrever_dados_csv_pay_roll(pay_rolls)
    logger.info("Folha de pagamento criada com sucesso")
    return pay_roll

@router.get("/pay_rolls", response_model=List[PayRoll])
def get_pay_rolls():
    logger.info("Listando todas as folhas de pagamento")
    return ler_dados_csv_pay_roll()

@router.get("/pay_rolls/{pay_roll_id}", response_model=PayRoll)
def get_pay_roll(pay_roll_id: int):
    logger.info("Retornando folha de ID:", pay_roll_id)
    for p in ler_dados_csv_pay_roll():
        if p.id == pay_roll_id:
            return p
    raise HTTPException(status_code=404, detail="Folha de pagamento não encontrada")

@router.put("/pay_rolls/{pay_roll_id}", response_model=PayRoll)
def update_pay_roll(pay_roll_id: int, pay_roll: PayRoll):
    pay_rolls = ler_dados_csv_pay_roll()
    for i, p in enumerate(pay_rolls):
        if p.id == pay_roll_id:
            pay_rolls[i] = pay_roll
            escrever_dados_csv_pay_roll(pay_rolls)
            logger.info(f"Folha de pagamento com ID {pay_roll_id} atualizada com sucesso")
            return pay_roll
    raise HTTPException(status_code=404, detail="Folha de pagamento não encontrada")

@router.delete("/pay_rolls/{pay_roll_id}")
def delete_pay_roll(pay_roll_id: int):
    pay_rolls = ler_dados_csv_pay_roll()
    for i, p in enumerate(pay_rolls):
        if p.id == pay_roll_id:
            del pay_rolls[i]
            escrever_dados_csv_pay_roll(pay_rolls)
            logger.info(f"Folha de pagamento com ID {pay_roll_id} deletada com sucesso")
            return {"message": "Folha de pagamento deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Folha de pagamento não encontrada")
