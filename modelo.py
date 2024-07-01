from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Tabla intermedia para la relación muchos a muchos entre estudiantes y carreras
enrollment_career = Table('enrollment_career', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('career_id', Integer, ForeignKey('careers.id'), primary_key=True)
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    enrollment_number = Column(String, unique=True, nullable=False)
    dni = Column(String, unique=True, nullable=False) 
    careers = relationship('Career', secondary=enrollment_career, back_populates='students')

class Career(Base):
    __tablename__ = 'careers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    students = relationship('Student', secondary=enrollment_career, back_populates='careers')
