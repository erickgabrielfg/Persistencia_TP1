from fastapi import FastAPI, HTTPException
from typing import List
from pathlib import Path
from logger import logger
import csv
from model.department import Department
from model.employee import Employee
from model.pay_roll import PayRoll
app = FastAPI()

PASTA_DADOS = Path("data")
PASTA_DADOS.mkdir(exist_ok=True)

ARQUIVO_DEPARTMENT = PASTA_DADOS / "department.csv"
ARQUIVO_EMPLOYEE = PASTA_DADOS / "employee.csv"
ARQUIVO_PAY_ROLL = PASTA_DADOS / "pay_roll.csv"

def ler_dados_csv_department():
    departments = []
    if ARQUIVO_DEPARTMENT.exists() and ARQUIVO_DEPARTMENT.stat().st_size > 0:
        with open(ARQUIVO_DEPARTMENT, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                departments.append(Department(
                    id=int(row["id"]),
                    name=row["name"],
                    manager=row["manager"],
                    location=row["location"],
                    number_of_employees=int(row["number_of_employees"])
                ))
    return departments

def escrever_dados_csv_department(departments):
    with open(ARQUIVO_DEPARTMENT, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "name", "manager", "location", "number_of_employees"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for d in departments:
            writer.writerow(d.model_dump())

def ler_dados_csv_employee():
    employees = []
    if ARQUIVO_EMPLOYEE.exists() and ARQUIVO_EMPLOYEE.stat().st_size > 0:
        with open(ARQUIVO_EMPLOYEE, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                employees.append(Employee(
                    id=int(row["id"]),
                    id_department=int(row["id_department"]),
                    name=row["name"],
                    cpf=row["cpf"],
                    position=row["position"],
                    admission_date=row["admission_date"]
                ))
    return employees

def escrever_dados_csv_employee(employees):
    with open(ARQUIVO_EMPLOYEE, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "id_department", "name", "cpf", "position", "admission_date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for e in employees:
            writer.writerow(e.model_dump())

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

@app.post("/departments", response_model=Department)
def create_department(department: Department):
    departments = ler_dados_csv_department()
    departments.append(department)
    escrever_dados_csv_department(departments)
    logger.info("Departamento criado com sucesso")
    return department

@app.get("/departments", response_model=List[Department])
def get_departments():
    logger.info("Retornando todos os departamentos")
    return ler_dados_csv_department()

@app.get("/departments/{department_id}", response_model=Department)
def get_department(department_id: int):
    for d in ler_dados_csv_department():
        if d.id == department_id:
            logger.info("Retornando departamento de ID:", department_id)
            return d
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@app.put("/departments/{department_id}", response_model=Department)
def update_department(department_id: int, department: Department):
    departments = ler_dados_csv_department()
    for i, d in enumerate(departments):
        if d.id == department_id:
            departments[i] = department
            escrever_dados_csv_department(departments)
            logger.info(f"Departamento com ID {department_id} atualizado com sucesso")
            return department
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@app.delete("/departments/{department_id}")
def delete_department(department_id: int):
    departments = ler_dados_csv_department()
    for i, d in enumerate(departments):
        if d.id == department_id:
            del departments[i]
            escrever_dados_csv_department(departments)
            logger.info(f"Departamento com ID {department_id} deletado com sucesso")
            return {"message": "Departamento deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@app.post("/employee", response_model=Employee)
def create_employee(employee: Employee):
    if not any(d.id == employee.id_department for d in ler_dados_csv_department()):
        raise HTTPException(status_code=400, detail="Departamento não encontrado")
    employees = ler_dados_csv_employee()
    employees.append(employee)
    escrever_dados_csv_employee(employees)
    logger.info("Funcionário criado com sucesso")
    return employee

@app.get("/employees", response_model=List[Employee])
def get_employees():
    logger.info("Retornando todos os funcionários")
    return ler_dados_csv_employee()

@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    for e in ler_dados_csv_employee():
        if e.id == employee_id:
            logger.info(f"Retornando funcionário de ID: {employee_id}")
            return e
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")

@app.put("/employees/{employee_id}", response_model=Employee)
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

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    employees = ler_dados_csv_employee()
    for i, e in enumerate(employees):
        if e.id == employee_id:
            del employees[i]
            escrever_dados_csv_employee(employees)
            logger.info(f"Funcionário com ID {employee_id} deletado com sucesso")
            return {"message": "Funcionário deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")

@app.post("/pay_roll", response_model=PayRoll)
def create_pay_roll(pay_roll: PayRoll):
    pay_rolls = ler_dados_csv_pay_roll()
    pay_rolls.append(pay_roll)
    escrever_dados_csv_pay_roll(pay_rolls)
    logger.info("Folha de pagamento criada com sucesso")
    return pay_roll

@app.get("/pay_rolls", response_model=List[PayRoll])
def get_pay_rolls():
    logger.info("Listando todas as folhas de pagamento")
    return ler_dados_csv_pay_roll()

@app.get("/pay_rolls/{pay_roll_id}", response_model=PayRoll)
def get_pay_roll(pay_roll_id: int):
    logger.info("Retornando folha de ID:", pay_roll_id)
    for p in ler_dados_csv_pay_roll():
        if p.id == pay_roll_id:
            return p
    raise HTTPException(status_code=404, detail="Folha de pagamento não encontrada")

@app.put("/pay_rolls/{pay_roll_id}", response_model=PayRoll)
def update_pay_roll(pay_roll_id: int, pay_roll: PayRoll):
    pay_rolls = ler_dados_csv_pay_roll()
    for i, p in enumerate(pay_rolls):
        if p.id == pay_roll_id:
            pay_rolls[i] = pay_roll
            escrever_dados_csv_pay_roll(pay_rolls)
            logger.info(f"Folha de pagamento com ID {pay_roll_id} atualizada com sucesso")
            return pay_roll
    raise HTTPException(status_code=404, detail="Folha de pagamento não encontrada")

@app.delete("/pay_rolls/{pay_roll_id}")
def delete_pay_roll(pay_roll_id: int):
    pay_rolls = ler_dados_csv_pay_roll()
    for i, p in enumerate(pay_rolls):
        if p.id == pay_roll_id:
            del pay_rolls[i]
            escrever_dados_csv_pay_roll(pay_rolls)
            logger.info(f"Folha de pagamento com ID {pay_roll_id} deletada com sucesso")
            return {"message": "Folha de pagamento deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Folha de pagamento não encontrada")
