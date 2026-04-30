from fastapi import FastAPI
from database.db import Base, engine
from routes.students import router as students_router

app = FastAPI(title="API de Estudiantes")

Base.metadata.create_all(bind=engine)

app.include_router(students_router)