from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from fastapi.responses import HTMLResponse

from database.db import SessionLocal
from models.student import Student

router = APIRouter(prefix="/students", tags=["Students"])
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE
# =========================
@router.post("/", status_code=201)
def create_student(student: dict, db: Session = Depends(get_db)):
    if db.query(Student).filter(Student.dni == student["dni"]).first():
        raise HTTPException(status_code=400, detail="DNI ya existe")

    new_student = Student(
        dni=student["dni"],
        name=student["name"],
        age=student["age"],
        grade=student["grade"],
        is_approved=student["is_approved"],
        updated_at=datetime.utcnow()
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# =========================
# BULK INSERT
# =========================
@router.post("/bulk", status_code=201)
def bulk_create_students(students: List[dict], db: Session = Depends(get_db)):
    new_students = []

    for student in students:
        if db.query(Student).filter(Student.dni == student["dni"]).first():
            continue

        new_student = Student(
            dni=student["dni"],
            name=student["name"],
            age=student["age"],
            grade=student["grade"],
            is_approved=student["is_approved"],
            updated_at=datetime.utcnow()
        )
        new_students.append(new_student)

    db.add_all(new_students)
    db.commit()

    return {"message": f"{len(new_students)} estudiantes creados correctamente"}


# =========================
# AVERAGE
# =========================
@router.get("/average")
def get_average_grade(db: Session = Depends(get_db)):
    students = db.query(Student).all()

    if not students:
        return {"average": 0}

    total = sum(student.grade for student in students)
    return {"average": total / len(students)}


# =========================
# HTML TABLE (FRAGMENT)
# =========================

from fastapi.responses import HTMLResponse

@router.get("/table", response_class=HTMLResponse)
def get_students_table(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    template = templates.get_template("partials/students_table.html")
    html_content = template.render(students=students)
    return html_content



# =========================
# READ ALL
# =========================
@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# =========================
# UPDATE
# =========================
@router.put("/{id}")
def update_student(id: int, student_data: dict, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    student.dni = student_data["dni"]
    student.name = student_data["name"]
    student.age = student_data["age"]
    student.grade = student_data["grade"]
    student.is_approved = student_data["is_approved"]
    student.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(student)
    return student


# =========================
# DELETE
# =========================
@router.delete("/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    db.delete(student)
    db.commit()
    return {"message": "Estudiante eliminado correctamente"}


# =========================
# READ BY ID 
# =========================
@router.get("/{id}")
def get_student_by_id(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return student
