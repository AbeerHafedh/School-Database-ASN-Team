from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

class GradeOut(BaseModel):
    subject: str
    grade: int

class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    phone_number: str
    class_id: int
    grades: list[GradeOut]

class StudentIn(BaseModel):
    name: str
    age: int
    phone_number: str
    class_id: int

class ClassOut(BaseModel):
    id: int
    name: str

class ClassIn(BaseModel):
    name: str

class SubjectOut(BaseModel):
    id: int
    name: str

class SubjectIn(BaseModel):
    name: str

class TeacherOut(BaseModel):
    id: int
    name: str
    salary: float
    subject_id: int

class TeacherIn(BaseModel):
    name: str
    salary: float
    subject_id: int

class GradeFullOut(BaseModel):
    id: int
    student: str
    subject: str
    grade: int

class GradeIn(BaseModel):
    student_id: int
    subject_id: int
    grade: int

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome"}

@app.get("/students", response_model=list[StudentOut])
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

@app.get("/classes", response_model=list[ClassOut])
def get_classes():
    with Session(engine) as session:
        classes = session.exec(select(Class)).all()
        return [{"id": c.id, "name": c.name} for c in classes]

@app.get("/subjects", response_model=list[SubjectOut])
def get_subjects():
    with Session(engine) as session:
        subjects = session.exec(select(Subject)).all()
        return [{"id": s.id, "name": s.name} for s in subjects]

@app.get("/teachers", response_model=list[TeacherOut])
def get_teachers():
    with Session(engine) as session:
        teachers = session.exec(select(Teacher)).all()
        return [{"id": t.id, "name": t.name, "salary": t.salary, "subject_id": t.subject_id} for t in teachers]

@app.get("/grades", response_model=list[GradeFullOut])
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

@app.post("/students", response_model=StudentOut)
def create_student(student: StudentIn):
    with Session(engine) as session:
        db_student = Student(name=student.name, age=student.age, phone_number=student.phone_number, class_id=student.class_id)
        session.add(db_student)
        session.commit()
        session.refresh(db_student)
        return {
            "id": db_student.id,
            "name": db_student.name,
            "age": db_student.age,
            "phone_number": db_student.phone_number,
            "class_id": db_student.class_id,
            "grades": []
        }

@app.post("/classes", response_model=ClassOut)
def create_class(class_: ClassIn):
    with Session(engine) as session:
        db_class = Class(name=class_.name)
        session.add(db_class)
        session.commit()
        session.refresh(db_class)
        return {"id": db_class.id, "name": db_class.name}

@app.post("/subjects", response_model=SubjectOut)
def create_subject(subject: SubjectIn):
    with Session(engine) as session:
        db_subject = Subject(name=subject.name)
        session.add(db_subject)
        session.commit()
        session.refresh(db_subject)
        return {"id": db_subject.id, "name": db_subject.name}

@app.post("/teachers", response_model=TeacherOut)
def create_teacher(teacher: TeacherIn):
    with Session(engine) as session:
        db_teacher = Teacher(name=teacher.name, salary=teacher.salary, subject_id=teacher.subject_id)
        session.add(db_teacher)
        session.commit()
        session.refresh(db_teacher)
        return {"id": db_teacher.id, "name": db_teacher.name, "salary": db_teacher.salary, "subject_id": db_teacher.subject_id}

@app.post("/grades", response_model=GradeFullOut)
def create_grade(grade: GradeIn):
    with Session(engine) as session:
        db_grade = Grade(student_id=grade.student_id, subject_id=grade.subject_id, grade=grade.grade)
        session.add(db_grade)
        session.commit()
        session.refresh(db_grade)
        return {
            "id": db_grade.id,
            "student": db_grade.student.name if db_grade.student else "Unknown",
            "subject": db_grade.subject.name if db_grade.subject else "Unknown",
            "grade": db_grade.grade
        }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        session.delete(student)
        session.commit()
        return {"message": f"Student with id {student_id} deleted successfully"}