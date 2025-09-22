from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from typing import Optional, List
from fastapi import FastAPI
from sqlalchemy import text


engine = create_engine('sqlite:///school.db')

class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    age: int
    phone_number: str
    class_id: Optional[int] = Field(default=None, foreign_key="class.id")
    grades: List["Grade"] = Relationship(back_populates="student")

class Class(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

class Subject(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    grades: List["Grade"] = Relationship(back_populates="subject")

class Grade(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    grade: int
    student: Optional[Student] = Relationship(back_populates="grades")
    subject: Optional[Subject] = Relationship(back_populates="grades")

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
        if session.exec(select(Student)).first():
            return
        web = Subject(name="Web")
        math = Subject(name="Math")
        science = Subject(name="Science")
        session.add_all([web, math, science])
        session.commit()
        c1 = Class(name="Class A")
        c2 = Class(name="Class B")
        c3 = Class(name="Class C")
        session.add_all([c1, c2, c3])
        session.commit()
        st1 = Student(name="Abeer Hafedh", age=22, phone_number="07701111111", class_id=c1.id)
        st2 = Student(name="Sarah Mohammed", age=22, phone_number="07702222222", class_id=c2.id)
        st3 = Student(name="Nawal Haider", age=22, phone_number="07803333333", class_id=c3.id)
        session.add_all([st1, st2, st3])
        session.commit()
        t1 = Teacher(name="Hussien", salary=800, subject_id=web.id)
        t2 = Teacher(name="Rana", salary=500, subject_id=science.id)
        t3 = Teacher(name="Ali", salary=600, subject_id=math.id)
        session.add_all([t1, t2, t3])
        session.commit()
        ct1 = ClassTeacher(teacher_id=t1.id, class_id=c1.id)
        ct2 = ClassTeacher(teacher_id=t2.id, class_id=c2.id)
        ct3 = ClassTeacher(teacher_id=t3.id, class_id=c3.id)
        session.add_all([ct1, ct2, ct3])
        session.commit()
        grades = [
            Grade(student_id=st1.id, subject_id=math.id, grade=95),
            Grade(student_id=st1.id, subject_id=science.id, grade=90),
            Grade(student_id=st1.id, subject_id=web.id, grade=85),
            Grade(student_id=st2.id, subject_id=math.id, grade=88),
            Grade(student_id=st2.id, subject_id=science.id, grade=92),
            Grade(student_id=st2.id, subject_id=web.id, grade=80),
            Grade(student_id=st3.id, subject_id=math.id, grade=76),
            Grade(student_id=st3.id, subject_id=science.id, grade=89),
            Grade(student_id=st3.id, subject_id=web.id, grade=91),
        ]
        session.add_all(grades)
        session.commit()

add_data()

app = FastAPI()

@app.get("/students")
def get_students():
    with Session(engine) as session:
        students = session.exec(select(Student)).all()
        result = []
        for s in students:
            grades = [{"subject": g.subject.name if g.subject else "Unknown", "grade": g.grade} for g in s.grades]
            result.append({
                "id": s.id,
                "name": s.name,
                "age": s.age,
                "phone_number": s.phone_number,
                "class_id": s.class_id,
                "grades": grades
            })
        return result

@app.get("/classes")
def get_classes():
    with Session(engine) as session:
        classes = session.exec(select(Class)).all()
        return [{"id": c.id, "name": c.name} for c in classes]

@app.get("/subjects")
def get_subjects():
    with Session(engine) as session:
        subjects = session.exec(select(Subject)).all()
        return [{"id": s.id, "name": s.name} for s in subjects]

@app.get("/teachers")
def get_teachers():
    with Session(engine) as session:
        teachers = session.exec(select(Teacher)).all()
        return [{"id": t.id, "name": t.name, "salary": t.salary, "subject_id": t.subject_id} for t in teachers]

@app.get("/grades")
def get_grades():
    with Session(engine) as session:
        grades = session.exec(select(Grade)).all()
        result = []
        for g in grades:
            result.append({
                "id": g.id,
                "student": g.student.name if g.student else "Unknown",
                "subject": g.subject.name if g.subject else "Unknown",
                "grade": g.grade
            })
        return result
@app.get("/")
def root():
    return {"message": "Welcome"}



# with Session(engine) as session:
#     session.exec(text("DELETE FROM student"))
#     session.exec(text("DELETE FROM class"))
#     session.exec(text("DELETE FROM subject"))
#     session.exec(text("DELETE FROM teacher"))
#     session.exec(text("DELETE FROM classteacher"))
#     session.exec(text("DELETE FROM Grade"))
#     session.commit()