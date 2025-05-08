from model.pay_roll import PayRoll
from pathlib import Path
import csv

PASTA_DADOS = Path("data")
PASTA_DADOS.mkdir(exist_ok=True)

ARQUIVO_PAY_ROLL = PASTA_DADOS / "pay_roll.csv"

def ler_dados_csv_pay_roll():
    pay_rolls = []
    if ARQUIVO_PAY_ROLL.exists() and ARQUIVO_PAY_ROLL.stat().st_size > 0:
        with open(ARQUIVO_PAY_ROLL, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pay_rolls.append(PayRoll(
                    id=int(row["id"]),
                    discounts=float(row["discounts"]),
                    net_salary=float(row["net_salary"]),
                    gross_salary=float(row["gross_salary"]),
                    reference_month=row["reference_month"]
                ))
    return pay_rolls

def escrever_dados_csv_pay_roll(pay_rolls):
    with open(ARQUIVO_PAY_ROLL, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "discounts", "net_salary", "gross_salary", "reference_month"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in pay_rolls:
            writer.writerow(p.model_dump())