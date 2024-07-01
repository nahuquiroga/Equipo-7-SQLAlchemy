# En main.py
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from crud import (
    create_student, create_career,
    enroll_student_in_career, get_students_in_career, get_career_by_name,
    get_careers, get_student_by_dni
)
import modelo  # Importar el modelo para asegurarse de que las tablas se crean

# Inicialización de la base de datos
modelo.Base.metadata.create_all(bind=engine)

def generate_enrollment_number(db):
    # Obtener el último número de matrícula usado
    last_student = db.query(modelo.Student).order_by(modelo.Student.id.desc()).first()
    last_enrollment_number = int(last_student.enrollment_number) if last_student else 0
    new_enrollment_number = last_enrollment_number + 1
    return str(new_enrollment_number)

def initialize_careers(db):
    careers = [
        "Tecnicatura universitaria en Comunicación Digital",
        "Tecnicatura universitaria en Acompañante Terapéutico",
        "Tecnicatura universitaria en Programación",
        "Tecnicatura universitaria en Logística y Transporte",
        "Tecnicatura universitaria en Prótesis Dental",
        "Tecnicatura universitaria en Automatización y Control",
        "Tecnicatura universitaria en Diseño y Desarrollo de Producto",
        "Tecnicatura universitaria en Gestión de las Organizaciones",
        "Licenciatura en Ciencia Política",
        "Licenciatura en Ciencia de Datos",
        "Licenciatura en Logística y Transporte",
        "Licenciatura en Enseñanza de Matemática",
        "Licenciatura en Administración"
    ]
    
    for career_name in careers:
        career = get_career_by_name(db, career_name)
        if not career:
            create_career(db, name=career_name)

def main():
    db: Session = SessionLocal()
    print("Bienvenidos al sistema de Inscripción de la Universidad Almirante Brown")
    
    # Inicializar carreras predefinidas
    initialize_careers(db)
    
    while True:
        print("\n1. Inscribir estudiante")
        print("2. Mostrar estudiantes inscritos en una carrera")
        print("3. Mostrar cantidad de estudiantes por carrera")
        print("4. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '4':
            break
        elif choice == '1':
            enroll_student(db)
        elif choice == '2':
            show_students_in_career(db)
        elif choice == '3':
            show_students_count_by_career(db)

    db.close()

def show_students_count_by_career(db):
    careers = get_careers(db)
    
    print("\nCantidad de estudiantes por carrera:")
    for career in careers:
        num_students = len(get_students_in_career(db, career.id))
        print(f"{career.name}: {num_students} estudiantes")

def enroll_student(db):
    student_name = input("\nIngrese nombre del estudiante: ")
    student_last_name = input("Ingrese apellido del estudiante: ")
    student_dni = input("Ingrese DNI del estudiante: ")

    # Verificar si el estudiante ya está registrado
    existing_student = get_student_by_dni(db, student_dni)
    if existing_student:
        print(f"El estudiante con DNI {student_dni} ya se encuentra registrado.")
        return

    enrollment_number = generate_enrollment_number(db)
    student = create_student(db, name=student_name, last_name=student_last_name, enrollment_number=enrollment_number, dni=student_dni)

    print("\nSeleccione la carrera a la que desea inscribirse:")
    careers = get_careers(db)  # Obtener todas las carreras disponibles
    for i, career in enumerate(careers, start=1):
        print(f"{i}. {career.name}")
    
    career_choice = int(input("Ingrese el número de la carrera: "))
    selected_career = careers[career_choice - 1]

    enroll_student_in_career(db, student.id, selected_career.id)

    students_in_career = get_students_in_career(db, selected_career.id)
    num_students = len(students_in_career)

    print(f"\nEstudiantes en la carrera {selected_career.name}:")
    for student in students_in_career:
        print(f"Nombre: {student.name} {student.last_name}, Matrícula: {student.enrollment_number}")
    
    print(f"\nActualmente hay {num_students} personas inscritas en la carrera {selected_career.name}")
    print(f"\nEstudiante {student_name} {student_last_name} inscrito correctamente con matrícula {enrollment_number}")

def show_students_in_career(db):
    print("\nSeleccione la carrera para ver los estudiantes inscritos:")
    careers = get_careers(db)
    for i, career in enumerate(careers, start=1):
        print(f"{i}. {career.name}")

    career_choice = int(input("Ingrese el número de la carrera: "))
    selected_career = careers[career_choice - 1]

    students_in_career = get_students_in_career(db, selected_career.id)

    print(f"\nEstudiantes en la carrera {selected_career.name}:")
    for student in students_in_career:
        print(f"Nombre: {student.name} {student.last_name}, Matrícula: {student.enrollment_number}")

if __name__ == "__main__":
    main()
