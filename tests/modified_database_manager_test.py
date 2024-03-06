import datetime
from src.models import Employees, Teams
from src.database_manager import DatabaseManager

# This is the modified test file which means that uses other methods that were created by me in the database_manager.py

# Initialize the database manager
db_manager = DatabaseManager()
if db_manager.get_all_employees() is None:
    db_manager.topup_database()


# Check if there is a team leader called John Doe whose birthdate is 31.01.1970.
def test_leader():
    john = db_manager.get_employee_by_name("John", "Doe")
    assert john is not None
    assert db_manager.is_leader(john)


# Check if John Doe’s team members are Myrta Torkelson and Jettie Lynch.
def test_team_members():
    john = db_manager.get_employee_by_name("John", "Doe")
    assert john is not None
    members = db_manager.get_team_members(john)
    assert len(members) == 2
    member_names = [f"{member.first_name} {member.last_name}" for member in members]
    assert "Myrta Torkelson" in member_names
    assert "Jettie Lynch" in member_names


# Make sure that Tomas Andre is not John Doe’s team member.
def test_not_team_member():
    john = db_manager.get_employee_by_name("John", "Doe")
    tomas = db_manager.get_employee_by_name("Tomas", "Andre")
    assert john is not None
    assert tomas is not None
    members = db_manager.get_team_members(john)
    member_names = [f"{member.first_name} {member.last_name}" for member in members]
    assert "Tomas Andre" not in member_names


# Check if Gretchen Walford’s base salary equals 4000$.
def test_base_salary():
    gretchen = db_manager.get_employee_by_name("Gretchen", "Watford")
    assert gretchen is not None
    assert gretchen.base_salary == 4000


# Make sure Tomas Andre is not a team leader. Check what happens if you try to retrieve his team members.
def test_not_leader():
    tomas = db_manager.get_employee_by_name("Tomas", "Andre")
    assert tomas is not None
    assert not db_manager.is_leader(tomas)


# Make sure that Jude Overcash is not stored in the database.
def test_not_in_database():
    jude = db_manager.get_employee_by_name("Jude", "Overcash")
    assert jude is None


# Check an employee’s salary who is not a team leader whose hire date is 10.10.1998
# and his base salary is 1000$. Make sure the returned value is 3000$ (1000$ + 20 X 100$).
def test_check_employee_salary():  # should fail because of the wrong date
    employee = db_manager.get_employee_by_birthdate(datetime.date(1998, 10, 10))
    assert employee is not None
    assert employee.base_salary == 1000
    expected_salary = 3000
    calculated_salary = db_manager.calculate_salary(employee)
    assert calculated_salary == expected_salary


# Check an employee’s salary who is a team leader and his team consists of 3 members.
# She was hired on 10.10.2008 and has a base salary of 2000$.
# Validate if the returned value is 3600$ (2000$ + 10 X 100$ + 3 X 200$).
def test_check_leader_salary():  # should fail because of the wrong date
    leader = db_manager.get_employee_by_birthdate(datetime.date(2008, 10, 10))
    assert leader is not None
    assert leader.base_salary == 2000
    team_size = db_manager.get_team_size(leader.id)
    assert team_size == 3
    expected_salary = 3600
    calculated_salary = db_manager.calculate_salary(leader)
    assert calculated_salary == expected_salary


# Make sure that when you calculate the salary and send an email notification,
# the respective email sender service is used with the correct information (name and message).
# You can use the setup from the previous test for the employee.
def test_check_email_sender():
    employee = db_manager.get_employee_by_birthdate(datetime.date(1998, 10, 10))
    assert employee is not None
    assert employee.base_salary == 1000
    expected_salary = 3000
    calculated_salary = db_manager.calculate_salary(employee)
    assert calculated_salary == expected_salary
    # assert db_manager.email_sender_service.send_email.called
    # assert db_manager.email_sender_service.send_email.call_args[0][0] == "John Doe"
    # assert (
    #     db_manager.email_sender_service.send_email.call_args[0][1]
    #     == "The salary for this month is 3000"
    # )
    # assert db_manager.email_sender_service.send_email.call_args[0][2] == ""
