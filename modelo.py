from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    enrollment_number = Column(String, unique=True, index=True)
    dni = Column(String, unique=True, index=True)
    careers = relationship("Career", secondary="enrollment_career", back_populates="students")

class Career(Base):
    __tablename__ = "careers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    students = relationship("Student", secondary="enrollment_career", back_populates="careers")

# Tabla intermedia para la relación many-to-many entre estudiantes y carreras
enrollment_career = Table(
    "enrollment_career",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("career_id", Integer, ForeignKey("careers.id"))
)
