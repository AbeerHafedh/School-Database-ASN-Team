from sqlmodel import SQLModel, Field, create_engine, Session, select
import json
from typing import Optional
from sqlalchemy import text


engine = create_engine('sqlite:///school.db')


class Class(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str


class Subject(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str


class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    age: int
    phone_number: str
    class_id: Optional[int] = Field(default=None, foreign_key="class.id")

class Teacher(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    salary: float
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")

class ClassTeacher(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    teacher_id: Optional[int] = Field(default=None, foreign_key="teacher.id")
    class_id: Optional[int] = Field(default=None, foreign_key="class.id")

def createDb():
    SQLModel.metadata.create_all(engine)
createDb()

def addClass(name):
    with Session(engine) as session:
        obj = Class(name=name)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        print(obj)
addClass("Class A")
addClass("Class B")
addClass("Class C")

def getAllClasses():
    with Session(engine) as session:
        obj = session.exec(select(Class)).all()
        print(obj)
getAllClasses()



def addStudent(name: str, age: int, phone_number: str, class_id: int):
    with Session(engine) as session:
        obj = Student(name=name, age=age, phone_number=phone_number, class_id=class_id)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        print(obj)

def getAllStudents():
    with Session(engine) as session:
        obj = session.exec(select(Student)).all()
        print(obj)

addStudent("Abeer Hafedh", 22, "07701111111", 1)
addStudent("Sarah Mohammed", 22, "07702222222", 2)
addStudent("Nawal Haider", 22, "07803333333", 3)

getAllStudents()


def addTeacher(name: str, salary: float, subject_id: int):
    with Session(engine) as session:
        obj = Teacher(name=name, salary=salary, subject_id=subject_id)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        print(obj)

def addClassTeacher(teacher_id: int, class_id: int):
    with Session(engine) as session:
        obj = ClassTeacher(teacher_id=teacher_id, class_id=class_id)
        session.add(obj)
        session.commit()
        print(obj)

def getAllTeachers():
    with Session(engine) as session:
        obj = session.exec(select(Teacher)).all()
        print(obj)

def getAllClassTeachers():
    with Session(engine) as session:
        obj = session.exec(select(ClassTeacher)).all()
        print(obj)

with Session(engine) as session:
    sub = session.exec(select(Subject).where(Subject.name == "Math")).first()
    if not sub:
        sub = Subject(name="Math")
        session.add(sub)
        session.commit()
        session.refresh(sub)
    subject_id = sub.id


addTeacher("Ahmed", 300, subject_id)
addTeacher("Rana", 500, subject_id)
addTeacher("Ali", 600, subject_id)

addClassTeacher(1, 1)
addClassTeacher(2, 2)
addClassTeacher(3, 3)

getAllTeachers()
getAllClassTeachers()

