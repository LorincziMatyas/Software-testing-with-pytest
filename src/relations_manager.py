# relations_manager.py
# emploibol a managerbol data classt csinalni
# pythentic, attrs, sqlalchemy

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
