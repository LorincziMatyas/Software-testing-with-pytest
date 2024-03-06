import datetime
from src.database_manager import DatabaseManager

# Initialize the database manager
db_manager = DatabaseManager()
if db_manager.get_all_employees() is None:
    db_manager.topup_database()


# Check if there is a team leader called John Doe whose birthdate is 31.01.1970.
def test_john_doe_is_team_leader():
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    john = [e for e in employees if e.first_name == "John" and e.last_name == "Doe"]
    assert len(john) == 1
    john = john[0]
    assert john.birth_date == datetime.date(1970, 1, 31)
    assert db_manager.is_leader(john)


# Check if John Doe’s team members are Myrta Torkelson and Jettie Lynch.
def test_john_doe_team_members():
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    john = [e for e in employees if e.first_name == "John" and e.last_name == "Doe"]
    assert len(john) == 1
    john = john[0]
    members = db_manager.get_team_members(john)
    assert len(members) == 2
    member_names = [f"{member.first_name} {member.last_name}" for member in members]
    assert "Myrta Torkelson" in member_names
    assert "Jettie Lynch" in member_names


# Make sure that Tomas Andre is not John Doe’s team member.
def test_tomas_andre_not_in_john_doe_team():
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    john = [e for e in employees if e.first_name == "John" and e.last_name == "Doe"]
    assert len(john) == 1
    john = john[0]
    members = db_manager.get_team_members(john)
    member_names = [f"{member.first_name} {member.last_name}" for member in members]
    assert "Tomas Andre" not in member_names


# Check if Gretchen Walford’s base salary equals 4000$.
def test_gretchen_watford_base_salary():
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    gretchen = [
        e for e in employees if e.first_name == "Gretchen" and e.last_name == "Watford"
    ]
    assert len(gretchen) == 1
    gretchen = gretchen[0]
    assert gretchen.base_salary == 4000


# Make sure Tomas Andre is not a team leader. Check what happens if you try to retrieve his team members.
def test_tomas_andre_not_team_leader():
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    tomas = [e for e in employees if e.first_name == "Tomas" and e.last_name == "Andre"]
    assert len(tomas) == 1
    tomas = tomas[0]
    assert not db_manager.is_leader(tomas)


# Make sure that Jude Overcash is not stored in the database.
def test_jude_overcash_not_in_database():
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    jude = [
        e for e in employees if e.first_name == "Jude" and e.last_name == "Overcash"
    ]
    assert len(jude) == 0


# Check an employee’s salary who is not a team leader whose hire date is 10.10.1998
# and his base salary is 1000$. Make sure the returned value is 3000$ (1000$ + 20 X 100$).
def test_employee_salary_without_leadership_bonus():  # should fail because of the wrong date
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    not_leaders = [
        e
        for e in employees
        if db_manager.is_leader(e) is False
        and e.hire_date == datetime.date(1998, 10, 10)
        and e.base_salary == 1000
    ]
    assert len(not_leaders) == 1
    not_leader = not_leaders[0]
    expected_salary = 3000
    calculated_salary = db_manager.calculate_salary(not_leader)
    assert calculated_salary == expected_salary


# Check an employee’s salary who is a team leader and his team consists of 3 members.
# She was hired on 10.10.2008 and has a base salary of 2000$.
# Validate if the returned value is 3600$ (2000$ + 10 X 100$ + 3 X 200$).
def test_leader_salary_with_team_bonus():  # should fail because of the wrong date
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    leaders = [
        e
        for e in employees
        if db_manager.is_leader(e) is True
        and e.hire_date == datetime.date(2008, 10, 10)
        and e.base_salary == 2000
    ]
    assert len(leaders) == 1
    leader = leaders[0]
    number_of_members = len(db_manager.get_team_members(leader.id))
    assert number_of_members == 3
    expected_salary = 3600
    calculated_salary = db_manager.calculate_salary(leader)
    assert calculated_salary == expected_salary


# Make sure that when you calculate the salary and send an email notification,
# the respective email sender service is used with the correct information (name and message).
# You can use the setup from the previous test for the employee.
def test_check_email_sender():
    db_manager = DatabaseManager()
    if db_manager.get_all_employees() is None:
        db_manager.topup_database()
    employees = db_manager.get_all_employees()
    assert employees is not None
    salary, name, message = db_manager.calculate_salary_and_send_email_modified(
        employees[0]
    )
    assert salary == 3000
    assert name == "John Doe"
    assert message == "John Doe, your salary: 3000 has been transferred to you."
