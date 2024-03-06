import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Create a SQLAlchemy base
Base = sqlalchemy.orm.declarative_base()


class Employees(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    base_salary = Column(Integer)
    birth_date = Column(Date)
    hire_date = Column(Date)


class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    leader_id = Column(Integer, ForeignKey("employees.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))


class Bonuses(Base):
    __tablename__ = "bonuses"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    value = Column(Integer)
