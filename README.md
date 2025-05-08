# 💼 Sistema de RH

Projeto desenvolvido para a disciplina de **Desenvolvimento de Software para Persistência**. Este sistema tem como objetivo gerenciar dados de recursos humanos, como funcionários, departamentos e folhas de pagamento, utilizando persistência em arquivos XML.

## 🧱 Estrutura do Sistema

### 📁 Entidades

#### 1. Funcionário

| Atributo         | Tipo      | Descrição                     |
|------------------|-----------|-------------------------------|
| `id`             | Inteiro   | Identificador único           |
| `nome`           | Texto     | Nome completo do funcionário  |
| `cpf`            | Texto     | CPF do funcionário            |
| `cargo`          | Texto     | Cargo ocupado                 |
| `data_admissao`  | Texto     | Data de admissão (YYYY-MM-DD) |

#### 2. Departamento

| Atributo               | Tipo      | Descrição                        |
|------------------------|-------------------------------------------|
| `id`                   | Inteiro   | Identificador único              |
| `nome`                 | Texto     | Nome do departamento             |
| `gerente`              | Texto     | Nome do gerente responsável      |
| `localizacao`          | Texto     | Localização física               |
| `numero_funcionarios`  | Inteiro   | Número de funcionários no setor  |

#### 3. Folha de Pagamento

| Atributo            | Tipo     | Descrição                                |
|---------------------|----------|------------------------------------------|
| `id`                | Inteiro  | Identificador único                      |
| `funcionario_id`    | Inteiro  | Referência ao ID do funcionário          |
| `salario_bruto`     | Float    | Valor bruto do salário                   |
| `descontos`         | Float    | Valor total de descontos aplicados       |
| `salario_liquido`   | Float    | Valor líquido após descontos             |
| `mes_referencia`    | Texto    | Mês de referência (ex: "2025-05")        |

---

## ⚙️ Funcionalidades

### ✅ CRUD (Create, Read, Update, Delete)

- Cadastrar, listar, editar e remover:
  - Funcionários
  - Departamentos
  - Folhas de pagamento

### 📋 Listagens

- Listar todos os:
  - Funcionários
  - Departamentos
  - Folhas de pagamento

### 🔍 Filtros

- Buscar **funcionários por cargo**
  - Exemplo: "Analista", "Gerente"
- Buscar **folhas de pagamento por mês de referência**
  - Exemplo: "2025-05"
- Buscar **departamentos por localização**
  - Exemplo: "Campinas"

### 🔢 Contagens Número total de funcionários cadastrados
- Número de departamentos existentes

---

## 🧩 Funcionalidades Extras (Requisitos da disciplina)

| Funcionalidade         | Descrição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| 🔐 **Hash (SHA256)**   | Validar integridade dos arquivos XML                                   |
| 🗜️ **Compactação ZIP** | Baixar um backup completo dos cadastros                                   |
| 📝 **Log**             | Registrar eventos importantes (ex: contratações, demissões, alterações)  |
| 🧾 **Exportação XML**  | Exportar funcionários ou fol de pagamento em formato XML              |

---

## 🧰 Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI** – API RESTful
- **XML** – Persistência dos dados
- **logging** – Registro de operações
- **hashlib**  Geração e verificação de hashes
- **zipfile** – Compactação dos arquivos de dados

---

## 🚀 Como Executar

uvicorn main:app --reload