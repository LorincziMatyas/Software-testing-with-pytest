from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from src.models import Bonuses, Employees, Teams, Base
import datetime


class DatabaseManager:
    def __init__(self, db_url="sqlite:///employees.db"):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # Add methods
    def add_employee(self, employee: Employees):
        session = self.Session()
        session.add(employee)
        session.commit()
        session.close()

    def add_team(self, team: Teams):
        session = self.Session()
        session.add(team)
        session.commit()
        session.close()

    def add_bonus(self, bonus: Bonuses):
        session = self.Session()
        session.add(bonus)
        session.commit()
        session.close()

    # Get methods
    def get_bonuses(self) -> list:
        session = self.Session()
        bonuses = session.query(Bonuses).all()
        session.close()
        return bonuses

    def get_yearly_bonus(self) -> int:
        session = self.Session()
        query = select(Bonuses.value).filter(Bonuses.type == "yearly_bonus")
        bonus = session.execute(query).scalar()
        session.close()
        return int(bonus) if bonus else 0

    def get_leader_bonus_per_member(self) -> int:
        session = self.Session()
        query = select(Bonuses.value).filter(Bonuses.type == "leader_bonus_per_member")
        bonus = session.execute(query).scalar()
        session.close()
        return int(bonus) if bonus else 0

    def get_employee_by_birthdate(self, birthdate):
        return (
            self.session.query(Employees)
            .filter(Employees.birth_date == birthdate)
            .first()
        )

    def get_employee_by_base_salary(self, base_salary):
        return (
            self.session.query(Employees)
            .filter(Employees.base_salary == base_salary)
            .first()
        )

    def get_employee_by_name_and_birthdate(
        self, first_name: str, last_name: str, birth_date: datetime.date
    ) -> Employees:
        session = self.Session()
        employee = (
            session.query(Employees)
            .filter_by(
                first_name=first_name, last_name=last_name, birth_date=birth_date
            )
            .first()
        )
        session.close()
        return employee

    def get_employee(self, employee_id: int) -> Employees:
        session = self.Session()
        employee = session.query(Employees).filter_by(id=employee_id).first()
        session.close()
        return employee

    def get_employee_by_name(self, first_name: str, last_name: str) -> Employees:
        session = self.Session()
        employee = (
            session.query(Employees)
            .filter_by(first_name=first_name, last_name=last_name)
            .first()
        )
        session.close()
        return employee

    def get_team_size(self, leader_id: int) -> int:
        session = self.Session()
        team_size = session.query(Teams).filter(Teams.leader_id == leader_id).count()
        session.close()
        return team_size

    # Original methods
    def is_leader(self, employee: Employees) -> bool:
        session = self.Session()
        team = session.query(Teams).filter(Teams.leader_id == employee.id).first()
        session.close()
        return team is not None

    def get_all_employees(self) -> list:
        session = self.Session()
        employees = session.query(Employees).all()
        session.close()
        return employees

    def get_team_members(self, leader: Employees) -> list:
        session = self.Session()
        team_members = session.query(Teams).filter(Teams.leader_id == leader.id).all()
        team_member_ids = [team.employee_id for team in team_members]
        members = (
            session.query(Employees).filter(Employees.id.in_(team_member_ids)).all()
        )
        session.close()
        return members

    def calculate_salary(self, employee: Employees) -> int:
        salary = employee.base_salary
        years_at_company = datetime.date.today().year - employee.hire_date.year
        yearly_bonus = self.get_yearly_bonus()
        salary += years_at_company * yearly_bonus

        if self.is_leader(employee):
            leader_bonus_per_member = self.get_leader_bonus_per_member()
            team_members_count = len(self.get_team_members(employee))
            salary += team_members_count * leader_bonus_per_member

        return salary

    def calculate_salary_and_send_email(self, employee: Employees) -> None:
        salary = self.calculate_salary(employee)

        print(
            f"{employee.first_name} {employee.last_name}, your salary: {salary} has been transferred to you."
        )

    def calculate_salary_and_send_email_modified(self, employee: Employees) -> tuple:
        salary = self.calculate_salary(employee)

        print(
            f"{employee.first_name} {employee.last_name}, your salary: {salary} has been transferred to you."
        )

        return (
            salary,
            f"{employee.first_name} {employee.last_name}",
            f"{employee.first_name} {employee.last_name}, your salary: {salary} has been transferred to you.",
        )

    # Other methods
    def remove_employee(self, employee_id: int):
        session = self.Session()
        employee = session.query(Employees).filter_by(id=employee_id).first()
        if employee:
            session.delete(employee)
            session.commit()
        session.close()

    def update_employee(self, employee: Employees):
        session = self.Session()
        existing_employee = session.query(Employees).filter_by(id=employee.id).first()
        if existing_employee:
            existing_employee.first_name = employee.first_name
            existing_employee.last_name = employee.last_name
            existing_employee.base_salary = employee.base_salary
            existing_employee.birth_date = employee.birth_date
            existing_employee.hire_date = employee.hire_date
            session.commit()
        session.close()

    def topup_database(self) -> None:
        session = self.Session()

        # Clear the tables
        # session.query(Employees).delete()
        # session.query(Teams).delete()
        # session.query(Bonuses).delete()

        employees = [
            Employees(
                id=1,
                first_name="John",
                last_name="Doe",
                base_salary=3000,
                birth_date=datetime.date(1970, 1, 31),
                hire_date=datetime.date(1990, 10, 1),
            ),
            Employees(
                id=2,
                first_name="Myrta",
                last_name="Torkelson",
                base_salary=1000,
                birth_date=datetime.date(1980, 1, 1),
                hire_date=datetime.date(2000, 1, 1),
            ),
            Employees(
                id=3,
                first_name="Jettie",
                last_name="Lynch",
                base_salary=1500,
                birth_date=datetime.date(1987, 1, 1),
                hire_date=datetime.date(2015, 1, 1),
            ),
            Employees(
                id=4,
                first_name="Gretchen",
                last_name="Watford",
                base_salary=4000,
                birth_date=datetime.date(1960, 1, 1),
                hire_date=datetime.date(1990, 1, 1),
            ),
            Employees(
                id=5,
                first_name="Tomas",
                last_name="Andre",
                base_salary=1600,
                birth_date=datetime.date(1995, 1, 1),
                hire_date=datetime.date(2015, 1, 1),
            ),
            Employees(
                id=6,
                first_name="Scotty",
                last_name="Bomba",
                base_salary=1300,
                birth_date=datetime.date(1977, 1, 1),
                hire_date=datetime.date(2008, 1, 1),
            ),
        ]

        teams = [
            Teams(id=1, leader_id=1, employee_id=2),
            Teams(id=2, leader_id=1, employee_id=3),
            Teams(id=3, leader_id=4, employee_id=5),
            Teams(id=4, leader_id=4, employee_id=6),
        ]

        bonuses = [
            Bonuses(id=1, type="yearly_bonus", value=100),
            Bonuses(id=2, type="leader_bonus_per_member", value=200),
        ]

        for employee in employees:
            session.add(employee)

        for team in teams:
            session.add(team)

        for bonus in bonuses:
            session.add(bonus)

        session.commit()
        session.close()
