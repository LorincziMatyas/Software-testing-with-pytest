# Description: This file contains the tests for the relational manager.
# The tests are written in the pytest framework.

import datetime
from src.relations_manager import Employee, RelationsManager

# Initialize the database
rm = RelationsManager()
rm.topup_database()


# Check if there is a team leader called John Doe whose birthdate is 31.01.1970.
def test_leader():
    # if len(rm.employee_list) == 0:
    #     topup_database()

    employees = rm.get_all_employees()

    john = [
        e
        for e in employees
        if e.first_name == "John"
        and e.last_name == "Doe"
        and e.birth_date == datetime.date(1970, 1, 31)
    ]

    assert len(john) == 1
    assert rm.is_leader(john[0])


#   Check if John Doe’s team members are Myrta Torkelson and Jettie Lynch.
def test_team_members():
    # if len(rm.employee_list) == 0:
    #     topup_database()

    employees = rm.get_all_employees()

    john = [e for e in employees if e.first_name == "John" and e.last_name == "Doe"]
    assert len(john) == 1
    assert rm.is_leader(john[0])

    members = rm.get_team_members(john[0])
    assert len(members) == 2

    member_names = [m.first_name + " " + m.last_name for m in members]
    assert "Myrta Torkelson" in member_names
    assert "Jettie Lynch" in member_names


#   Make sure that Tomas Andre is not John Doe’s team member.
def test_not_team_member():
    # if len(rm.employee_list) == 0:
    #     topup_database()

    employees = rm.get_all_employees()

    john = [e for e in employees if e.first_name == "John" and e.last_name == "Doe"]
    assert len(john) == 1
    assert rm.is_leader(john[0])

    members = rm.get_team_members(john[0])
    assert len(members) == 2

    member_names = [m.first_name + " " + m.last_name for m in members]
    assert "Tomas Andre" not in member_names


#   Check if Gretchen Walford’s base salary equals 4000$.
def test_base_salary():
    # if len(rm.employee_list) == 0:
    #     topup_database()

    employees = rm.get_all_employees()

    gretchen = [
        e for e in employees if e.first_name == "Gretchen" and e.last_name == "Watford"
    ]
    assert len(gretchen) == 1
    assert gretchen[0].base_salary == 4000


#   Make sure Tomas Andre is not a team leader. Check what happens if you try to retrieve his team members.
def test_not_leader():
    # if len(rm.employee_list) == 0:
    #     topup_database()

    employees = rm.get_all_employees()

    tomas = [e for e in employees if e.first_name == "Tomas" and e.last_name == "Andre"]
    assert len(tomas) == 1
    assert not rm.is_leader(tomas[0])


#   Make sure that Jude Overcash is not stored in the database.
def test_not_in_database():
    # if len(rm.employee_list) == 0:
    #     topup_database()

    employees = rm.get_all_employees()

    jude = [
        e for e in employees if e.first_name == "Jude" and e.last_name == "Overcash"
    ]
    assert len(jude) == 0


# Add employees to the database
