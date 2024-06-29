# En main.py
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from crud import (
    create_student, create_career,
    enroll_student_in_career, get_students_in_career, get_career_by_name,
    get_careers, get_student_by_dni
)
import modelo  # Importar el modelo para asegurarse de que las tablas se crean
import pandas as pd

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

def export_to_csv(db):
    # Obtener todos los estudiantes
    students = db.query(modelo.Student).all()

    # Convertir a DataFrame de pandas para exportar a CSV
    df_students = pd.DataFrame([{
        'Nombre': student.name,
        'Apellido': student.last_name,
        'Matrícula': student.enrollment_number,
        'DNI': student.dni,
        'Carrera': ''  # Columna de carrera inicialmente vacía
    } for student in students])

    # Obtener y actualizar la información de la carrera para cada estudiante
    for student in students:
        student_careers = get_careers(db, student.id)
        if student_careers:
            # Suponiendo que el estudiante se inscribe en la primera carrera de la lista
            selected_career = student_careers[0]
            df_students.loc[df_students['Matrícula'] == student.enrollment_number, 'Carrera'] = selected_career.name

    # Ordenar y seleccionar las columnas en el orden deseado
    df_students = df_students[['Nombre', 'Apellido', 'Matrícula', 'DNI', 'Carrera']]

    # Guardar el DataFrame ordenado y organizado como CSV
    df_students.to_csv('students_sorted.csv', index=False, encoding='utf-8-sig')

def main():
    db: Session = SessionLocal()
    print("Bienvenidos al sistema de Inscripción de la Universidad Almirante Brown")
    
    # Inicializar carreras predefinidas
    initialize_careers(db)
    
    while True:
        print("\n1. Inscribir estudiante")
        print("2. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '2':
            break
        elif choice == '1':
            student_name = input("\nIngrese nombre del estudiante: ")
            student_last_name = input("Ingrese apellido del estudiante: ")
            student_dni = input("Ingrese DNI del estudiante: ")

            # Verificar si el estudiante ya está registrado
            existing_student = get_student_by_dni(db, student_dni)
            if existing_student:
                print(f"El estudiante con DNI {student_dni} ya se encuentra registrado.")
                continue

            enrollment_number = generate_enrollment_number(db)
            student = create_student(db, name=student_name, last_name=student_last_name, enrollment_number=enrollment_number, dni=student_dni)

            print("\nSeleccione la carrera a la que desea inscribirse:")
            careers = get_careers(db, student.id)  # Obtener todas las carreras disponibles
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

        continue_option = input("\nPresione Enter para continuar o 'q' para salir: ")
        if continue_option.lower() == 'q':
            break

    # Exportar los datos a CSV después de la ejecución del ciclo
    export_to_csv(db)
    db.close()

if __name__ == "__main__":
    main()
