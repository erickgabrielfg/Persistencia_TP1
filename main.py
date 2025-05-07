from fastapi import FastAPI, HTTPException
from typing import List
from pathlib import Path
from logger import logger
import os
import xml.etree.ElementTree as ET
from model.department import Department
from model.employee import Employee
from model.pay_roll import PayRoll
from xml.etree.ElementTree import ParseError

app = FastAPI()

PASTA_DADOS = Path("data")
PASTA_DADOS.mkdir(exist_ok=True)

ARQUIVO_DEPARTMENT = PASTA_DADOS / "department.xml"
ARQUIVO_PAY_ROLL = PASTA_DADOS / "pay_roll.xml"
ARQUIVO_EMPLOYEE = PASTA_DADOS / "employee.xml"

def ler_dados_xml_department():
    departments = []
    if os.path.exists(ARQUIVO_DEPARTMENT):
        if os.path.getsize(ARQUIVO_DEPARTMENT) == 0:
            root = ET.Element("departments")
            tree = ET.ElementTree(root)
            tree.write(ARQUIVO_DEPARTMENT)
        try:
            tree = ET.parse(ARQUIVO_DEPARTMENT)
            root = tree.getroot()
            for elem in root.findall("department"):
                department = Department(
                    id=int(elem.find("id").text),
                    name=elem.find("name").text,
                    manager=elem.find("manager").text,
                    location=elem.find("location").text,
                    number_of_employees=int(elem.find("number_of_employees").text)  
                )
                departments.append(department)
        except ParseError:
            raise HTTPException(status_code=500, detail="Arquivo XML de departamentos está corrompido.")
    return departments

def escrever_dados_xml_department(departments):
    root = ET.Element("departments")
    for department in departments:
        elem = ET.SubElement(root, "department")
        ET.SubElement(elem, "id").text = str(department.id)
        ET.SubElement(elem, "name").text = department.name
        ET.SubElement(elem, "manager").text = department.manager
        ET.SubElement(elem, "location").text = department.location
        ET.SubElement(elem, "number_of_employees").text = str(department.number_of_employees)

    tree = ET.ElementTree(root)
    with open(ARQUIVO_DEPARTMENT, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)

def ler_dados_xml_pay_roll():
    pay_rolls = []
    if os.path.exists(ARQUIVO_PAY_ROLL):
        tree = ET.parse(ARQUIVO_PAY_ROLL)
        root = tree.getroot()
        for elem in root.findall("pay_roll"):
            pay_roll = PayRoll(
                id=int(elem.find("id").text),
                employee_id=int(elem.find("employee_id").text),
                discounts=float(elem.find("discounts").text),
                net_salary=float(elem.find("net_salary").text),
                gross_salary=float(elem.find("gross_salary").text),
                reference_month=elem.find("reference_month").text
            )
            pay_rolls.append(pay_roll)
    return pay_rolls

def escrever_dados_xml_pay_roll(pay_rolls):
    root = ET.Element("pay_rolls")
    for pay_roll in pay_rolls:
        elem = ET.SubElement(root, "pay_roll")
        ET.SubElement(elem, "id").text = str(pay_roll.id)
        ET.SubElement(elem, "employee_id").text = str(pay_roll.employee_id)
        ET.SubElement(elem, "discounts").text = str(pay_roll.discounts)
        ET.SubElement(elem, "net_salary").text = str(pay_roll.net_salary)
        ET.SubElement(elem, "gross_salary").text = str(pay_roll.gross_salary)
        ET.SubElement(elem, "reference_month").text = pay_roll.reference_month

    tree = ET.ElementTree(root)
    with open(ARQUIVO_PAY_ROLL, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)

def ler_dados_xml_employee():
    employees = []
    if os.path.exists(ARQUIVO_EMPLOYEE):
        tree = ET.parse(ARQUIVO_EMPLOYEE)
        root = tree.getroot()
        for elem in root.findall("employee"):
            employee = Employee(
                id=int(elem.find("id").text),
                name=elem.find("name").text,
                cpf=elem.find("cpf").text,
                position=elem.find("position").text,
                admission_date=elem.find("admission_date").text
            )
            employees.append(employee)
    return employees

def escrever_dados_xml_employee(employees):
    root = ET.Element("employees")
    for employee in employees:
        elem = ET.SubElement(root, "employee")
        ET.SubElement(elem, "id").text = str(employee.id)
        ET.SubElement(elem, "name").text = employee.name
        ET.SubElement(elem, "cpf").text = employee.cpf
        ET.SubElement(elem, "position").text = employee.position
        ET.SubElement(elem, "admission_date").text = employee.admission_date

    tree = ET.ElementTree(root)
    with open(ARQUIVO_EMPLOYEE, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)

@app.post("/departments", response_model=Department)    
def create_department(department: Department):
    logger.info(f"Creating department: {department}")
    try:
        departments = ler_dados_xml_department()
        departments.append(department)
        escrever_dados_xml_department(departments)
        return department
    except Exception as e:
        logger.error(f"Erro ao criar departamento: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar departamento")

@app.get("/departments", response_model=List[Department])
def get_departments():
    logger.info("Buscando todos os departamentos")
    try:
        return ler_dados_xml_department()
    except Exception as e:
        logger.error(f"Erro ao ler departamentos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao obter departamentos")

@app.get("/departments/{department_id}", response_model=Department)
def get_department(department_id: int):
    logger.info(f"Buscando departamento com ID: {department_id}")
    departments = ler_dados_xml_department()
    for department in departments:
        if department.id == department_id:
            return department
    raise HTTPException(status_code=404, detail="Departamento não encontrado")
@app.put("/departments/{department_id}", response_model=Department)

@app.put("/departments/{department_id}", response_model=Department)
def update_department(department_id: int, department: Department):
    logger.info(f"Atualizando documento com ID: {department_id}")
    departments = ler_dados_xml_department()
    for i, dep in enumerate(departments):
        if dep.id == department_id:
            departments[i] = department
            escrever_dados_xml_department(departments)
            return department
    raise HTTPException(status_code=404, detail="Departamento não encontrado")

@app.delete("/departments/{department_id}")
def delete_department(department_id: int):
    logger.info(f"Deletando apartamento com ID: {department_id}")
    departments = ler_dados_xml_department()
    for i, dep in enumerate(departments):
        if dep.id == department_id:
            del departments[i]
            escrever_dados_xml_department(departments)
            return {"message": "Departamento deleatado com sucesso"}
    raise HTTPException(status_code=404, detail="Departamento não entrado")

@app.get("/employees", response_model=List[Employee])
def get_employees():
    logger.info("Buscando todos os funcionários")
    return ler_dados_xml_employee()

@app.post("/employee", response_model=Employee)    
def create_employee(employee: Employee):
    department = ler_dados_xml_department()
    if not any(department.id == employee.id_department for department in department):
        raise HTTPException(status_code=400, detail="Departamento não encontrado")
    logger.info(f"Creating employee: {employee}")
    try:
        employees = ler_dados_xml_employee()
        employees.append(employee)
        escrever_dados_xml_employee(employees)
        return employee
    except Exception as e:
        logger.error(f"Erro ao criar funcionário: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar funcionário")


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: int):
    logger.info(f"Deletando funcionário com ID: {employee_id}")
    employees = ler_dados_xml_employee()
    for employee in employees:
        if employee.id == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Funcionario não encontrado")

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    logger.info(f"Deletando funcionario com ID: {employee_id}")
    employees = ler_dados_xml_employee()
    for i, emp in enumerate(employees):
        if emp.id == employee_id:
            del employees[i]
            escrever_dados_xml_employee(employees)
            return {"message": "Funcionario deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Funcionario não encontrado")

@app.put("/employees/{employee_id}", response_model=Employee)
def updage_employee(employee_id: int, employee: Employee):
    department = ler_dados_xml_department()
    if not any(department.id == employee.id_department for department in department):
        raise HTTPException(status_code=400, detail="Departamento não encontrado")
    logger.info(f"Atualizando funcionário com ID: {employee_id}")
    employees = ler_dados_xml_employee()
    for i, emp in enumerate(employees):
        if emp.id == employee_id:
            employees[i] = employee
            escrever_dados_xml_employee(employees)
            return employee
    raise HTTPException(status_code=404, detail="Funcionario não encontrado")