from sqlalchemy.orm import Session
from modelo import Student, Career, enrollment_career

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_enrollment_number(db: Session, enrollment_number: str):
    return db.query(Student).filter(Student.enrollment_number == enrollment_number).first()

def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Student).offset(skip).limit(limit).all()

def create_student(db: Session, name: str, last_name: str, enrollment_number: str, dni: str):
    db_student = Student(name=name, last_name=last_name, enrollment_number=enrollment_number, dni=dni)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student_by_dni(db: Session, dni: str):
    return db.query(Student).filter(Student.dni == dni).first()

def get_career(db: Session, career_id: int):
    return db.query(Career).filter(Career.id == career_id).first()

def get_careers(db: Session, skip: int = 0, limit: int = 13):
    return db.query(Career).offset(skip).limit(limit).all()

def create_career(db: Session, name: str):
    db_career = Career(name=name)
    db.add(db_career)
    db.commit()
    db.refresh(db_career)
    return db_career

# Funciones para la inscripción de estudiantes en carreras
def enroll_student_in_career(db: Session, student_id: int, career_id: int):
    enrollment = enrollment_career.insert().values(student_id=student_id, career_id=career_id)
    db.execute(enrollment)
    db.commit()

def get_students_in_career(db: Session, career_id: int):
    career = db.query(Career).filter(Career.id == career_id).first()
    return career.students if career else []

def get_career_by_name(db: Session, career_name: str):
    return db.query(Career).filter(Career.name == career_name).first()
