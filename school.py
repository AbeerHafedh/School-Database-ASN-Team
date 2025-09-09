from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from sqlmodel import Session
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

def add_data():
    with Session(engine) as session:
        web = Subject(name="Web")
        math = Subject(name="Math")
        science = Subject(name="Science")
        session.add_all([math, science])
        session.commit()
        session.refresh(math)
        session.refresh(science)

        c1 = Class(name="Class A")
        c2 = Class(name="Class B")
        c3 = Class(name="Class C")
        session.add_all([c1, c2, c3])
        session.commit()
        session.refresh(c1)
        session.refresh(c2)
        session.refresh(c3)

        st1 = Student(name="Abeer Hafedh", age=22, phone_number="07701111111", class_id=c1.id)
        st2 = Student(name="Sarah Mohammed", age=22, phone_number="07702222222", class_id=c2.id)
        st3 = Student(name="Nawal Haider", age=22, phone_number="07803333333", class_id=c3.id)
        session.add_all([st1, st2, st3])
        session.commit()

        t1 = Teacher(name="Hussien", salary=800, subject_id=math.id)
        t2 = Teacher(name="Rana", salary=500, subject_id=science.id)
        t3 = Teacher(name="Ali", salary=600, subject_id=math.id)
        session.add_all([t1, t2, t3])
        session.commit()
        session.refresh(t1)
        session.refresh(t2)
        session.refresh(t3)

        ct1 = ClassTeacher(teacher_id=t1.id, class_id=c1.id)
        ct2 = ClassTeacher(teacher_id=t2.id, class_id=c2.id)
        ct3 = ClassTeacher(teacher_id=t3.id, class_id=c3.id)
        session.add_all([ct1, ct2, ct3])
        session.commit()

        print("All data added successfully!")

add_data()

def print_all_data(session):
    students = session.exec(select(Student)).all()
    classes = session.exec(select(Class)).all()
    subjects = session.exec(select(Subject)).all()
    teachers = session.exec(select(Teacher)).all()
    class_teachers = session.exec(select(ClassTeacher)).all()

    print("\n--- Students ---")
    for s in students:
        print(f"{s.id} | {s.name} | Age: {s.age} | Phone: {s.phone_number} | ClassID: {s.class_id}")

    print("\n--- Classes ---")
    for c in classes:
        print(f"{c.id} | {c.name}")

    print("\n--- Subjects ---")
    for sub in subjects:
        print(f"{sub.id} | {sub.name}")

    print("\n--- Teachers ---")
    for t in teachers:
        print(f"{t.id} | {t.name} | Salary: {t.salary} | SubjectID: {t.subject_id}")

    print("\n--- ClassTeachers ---")
    for ct in class_teachers:
        print(f"{ct.id} | TeacherID: {ct.teacher_id} | ClassID: {ct.class_id}")

with Session(engine) as session:
    print_all_data(session)

# with Session(engine) as session:
#     session.exec(text("DELETE FROM student"))
#     session.exec(text("DELETE FROM class"))
#     session.exec(text("DELETE FROM subject"))
#     session.exec(text("DELETE FROM teacher"))
#     session.exec(text("DELETE FROM classteacher"))
#     session.commit()
