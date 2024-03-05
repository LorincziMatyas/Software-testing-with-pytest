import datetime
from src.models import Employees, Teams
from src.database_manager import DatabaseManager

# Initialize the database manager
db_manager = DatabaseManager()
db_manager.topup_database()


def test_leader():
    john = db_manager.get_employee_by_name_and_birthdate(
        "John", "Doe", datetime.date(1970, 1, 31)
    )
    assert john is not None
    assert db_manager.is_leader(john)


def test_team_members():
    john = db_manager.get_employee_by_name_and_birthdate(
        "John", "Doe", datetime.date(1970, 1, 31)
    )
    assert john is not None
    members = db_manager.get_team_members(john)
    assert len(members) == 2
    member_names = [f"{member.first_name} {member.last_name}" for member in members]
    assert "Myrta Torkelson" in member_names
    assert "Jettie Lynch" in member_names


def test_not_team_member():
    john = db_manager.get_employee_by_name_and_birthdate(
        "John", "Doe", datetime.date(1970, 1, 31)
    )
    tomas = db_manager.get_employee_by_name_and_birthdate(
        "Tomas", "Andre", datetime.date(1995, 1, 1)
    )
    assert john is not None
    assert tomas is not None
    members = db_manager.get_team_members(john)
    member_names = [f"{member.first_name} {member.last_name}" for member in members]
    assert "Tomas Andre" not in member_names


def test_base_salary():
    gretchen = db_manager.get_employee_by_name_and_birthdate(
        "Gretchen", "Watford", datetime.date(1960, 1, 1)
    )
    assert gretchen is not None
    assert gretchen.base_salary == 4000


def test_not_leader():
    tomas = db_manager.get_employee_by_name_and_birthdate(
        "Tomas", "Andre", datetime.date(1995, 1, 1)
    )
    assert tomas is not None
    assert not db_manager.is_leader(tomas)


def test_not_in_database():
    jude = db_manager.get_employee_by_name_and_birthdate("Jude", "Overcash", None)
    assert jude is None


# should fail because of the wrong date
def test_check_employee_salary():
    employee = db_manager.get_employee_by_birthdate(datetime.date(1998, 10, 10))

    assert employee is not None
    assert employee.base_salary == 1000

    expected_salary = 3000
    calculated_salary = db_manager.calculate_salary(employee.id)
    assert calculated_salary == expected_salary


# should fail because of the wrong date
def test_check_leader_salary():
    leader = db_manager.get_employee_by_birthdate(datetime.date(2008, 10, 10))
    assert leader is not None
    assert leader.base_salary == 2000
    team_size = db_manager.get_team_size(leader.id)
    assert team_size == 3
    expected_salary = 3600
    calculated_salary = db_manager.calculate_salary(leader.id)
    assert calculated_salary == expected_salary


# Make sure that when you calculate the salary and send an email notification, the respective email sender service is used with the correct information (name and message). You can use the setup from the previous test for the employee.
def test_check_email_sender():
    employee = db_manager.get_employee_by_birthdate(datetime.date(1998, 10, 10))
    assert employee is not None
    assert employee.base_salary == 1000
    expected_salary = 3000
    calculated_salary = db_manager.calculate_salary(employee.id)
    assert calculated_salary == expected_salary
    assert db_manager.email_sender_service.send_email.called
    assert db_manager.email_sender_service.send_email.call_args[0][0] == "John Doe"
    assert (
        db_manager.email_sender_service.send_email.call_args[0][1]
        == "The salary for this month is 3000"
    )
    # assert db_manager.email_sender_service.send_email.call_args[0][2] == ""
