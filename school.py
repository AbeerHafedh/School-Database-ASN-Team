from sqlmodel import SQLModel, Field, create_engine, Session, select
import json
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
addClass('Abeer Hafedh')
addClass('Sarah Mohammed')
addClass('Nawal Haider')


def getAllClasses():
    with Session(engine) as session:
        obj = session.exec(select(Class)).all()
        print(obj)
getAllClasses()
