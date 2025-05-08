import uvicorn
from fastapi import FastAPI
from routes.department_routes import router as department_router
from routes.employee_routes import router as employee_router

app = FastAPI()

app.include_router(department_router)
app.include_router(employee_router)

if __name__=="__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)