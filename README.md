# Examen-Final-29.04
# API REST de Estudiantes

## Descripción
Este proyecto implementa una **API REST** para la gestión de estudiantes utilizando **Python** y **FastAPI**.  
El objetivo es cumplir con los requerimientos del examen, aplicando conceptos de backend, rutas, persistencia de datos y manejo correcto de respuestas HTTP.

---

## Tecnologías utilizadas
- Python 3
- FastAPI
- Uvicorn
- SQLite
- SQLAlchemy
- Jinja2 (para renderizar HTML)
- Swagger UI

---

## Estructura del proyecto

api-estudiantes/
├── main.py
├── database/
│   └── db.py
├── models/
│   └── student.py
├── routes/
│   └── students.py
├── templates/
│   └── partials/
│       └── students_table.html
├── requirements.txt
└── README.md

---

## 🚀 Instalación y ejecución

### 1️⃣ Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd api-estudiantes

pip install -r requirements.txt

python -m uvicorn main:app --reload

## 🚀 Acceso a la aplicación
Swagger UI:
http://127.0.0.1:8000/docs


Tabla HTML de estudiantes:
http://127.0.0.1:8000/students/table


{
  "id": 1,
  "dni": "12345678",
  "name": "Juan Pérez",
  "age": 20,
  "grade": 15.5,
  "is_approved": true,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}

dni es obligatorio y único
created_at se genera automáticamente
updated_at se actualiza en cada modificación
is_approved es un valor manual

Crear un estudiante


POST /students
{
  "dni": "12345678",
  "name": "Juan Pérez",
  "age": 20,
  "grade": 15.5,
  "is_approved": true
}
``
Inserción masiva
POST /students/bulk
[
  {
    "dni": "55555555",
    "name": "Carlos Torres",
    "age": 23,
    "grade": 14,
    "is_approved": false
  },
  {
    "dni": "66666666",
    "name": "Lucía Ramos",
    "age": 21,
    "grade": 17,
    "is_approved": true
  }
]
