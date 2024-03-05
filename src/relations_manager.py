# relations_manager.py
# emploibol a managerbol data classt csinalni
# pydantic, attrs, sqlalchemy, sqlite

import datetime
from dataclasses import dataclass
from typing import Optional
from src.employee import Employee


@dataclass
class Employee:
    id: int
    first_name: str
    last_name: str
    base_salary: float
    birth_date: datetime.date
    hire_date: datetime.date


class RelationsManager:
    def __init__(self):
        self.employee_list = []
        self.teams = {1: [2, 3], 4: [5, 6]}

    def add_employee(self, employee: Employee):
        self.employee_list.append(employee)

    def remove_employee(self, employee_id: int):
        self.employee_list = [e for e in self.employee_list if e.id != employee_id]

    def update_employee(self, employee: Employee):
        for i, e in enumerate(self.employee_list):
            if e.id == employee.id:
                self.employee_list[i] = employee
                break

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        for e in self.employee_list:
            if e.id == employee_id:
                return e
        return None

    def is_leader(self, employee: Employee) -> bool:
        return employee.id in self.teams

    def get_all_employees(self) -> list:
        return self.employee_list

    def get_team_members(self, employee: Employee) -> list:
        if self.is_leader(employee):
            member_ids = self.teams[employee.id]
            members = [e for e in self.employee_list if e.id in member_ids]
            return members

    def topup_database(self) -> None:

        self.add_employee(
            Employee(
                id=1,
                first_name="John",
                last_name="Doe",
                base_salary=3000,
                birth_date=datetime.date(1970, 1, 31),
                hire_date=datetime.date(1990, 10, 1),
            )
        )

        self.add_employee(
            Employee(
                id=2,
                first_name="Myrta",
                last_name="Torkelson",
                base_salary=1000,
                birth_date=datetime.date(1980, 1, 1),
                hire_date=datetime.date(2000, 1, 1),
            )
        )

        self.add_employee(
            Employee(
                id=3,
                first_name="Jettie",
                last_name="Lynch",
                base_salary=1500,
                birth_date=datetime.date(1987, 1, 1),
                hire_date=datetime.date(2015, 1, 1),
            )
        )

        self.add_employee(
            Employee(
                id=4,
                first_name="Gretchen",
                last_name="Watford",
                base_salary=4000,
                birth_date=datetime.date(1960, 1, 1),
                hire_date=datetime.date(1990, 1, 1),
            )
        )

        self.add_employee(
            Employee(
                id=5,
                first_name="Tomas",
                last_name="Andre",
                base_salary=1600,
                birth_date=datetime.date(1995, 1, 1),
                hire_date=datetime.date(2015, 1, 1),
            )
        )

        self.add_employee(
            Employee(
                id=6,
                first_name="Scotty",
                last_name="Bomba",
                base_salary=1300,
                birth_date=datetime.date(1977, 1, 1),
                hire_date=datetime.date(2008, 1, 1),
            )
        )
