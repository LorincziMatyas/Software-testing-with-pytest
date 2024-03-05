import datetime
from src.employee_manager import EmployeeManager
from src.relations_manager import RelationsManager

# Check an employee’s salary who is not a team leader whose hire date
# is 10.10.1998 and his base salary is 1000$. Make sure the returned
# value is 3000$ (1000$ + 20 X 100$).


def check_employee_salary():
    rm = RelationsManager()
    em = EmployeeManager(rm)

    # Get all employees
    all_employees = rm.get_all_employees()

    # Filter the employee by not being a leader
    not_leader_employees = [e for e in all_employees if rm.is_leader(e) == False]

    # Filter the employee by hire date and base salary
    employee = [
        e
        for e in not_leader_employees
        if e.hire_date == datetime.date(1998, 10, 10) and e.base_salary == 1000
    ]

    # Check if the employee is found and only one employee is found
    assert len(employee) == 1

    # Calculate the salary
    calculated_salary = em.calculate_salary(employee[0])

    # Check if the calculated salary is 3000
    assert calculated_salary == 3000


# Check an employee’s salary who is a team leader and his team consists
# of 3 members. She was hired on 10.10.2008 and has a base salary of 2000$.
# Validate if the returned value is 3600$ (2000$ + 10 X 100$ + 3 X 200$).


def check_leader_salary():
    rm = RelationsManager()
    em = EmployeeManager(rm)

    # Get all employees
    all_employees = rm.get_all_employees()

    # Filter the employee by being a leader
    leader_employees = [e for e in all_employees if rm.is_leader(e) == True]

    # Filter the employee by hire date and base salary
    employee = [
        e
        for e in leader_employees
        if e.hire_date == datetime.date(2008, 10, 10) and e.base_salary == 2000
    ]

    # Check if the employee is found and only one employee is found
    assert len(employee) == 1

    # Calculate the salary
    calculated_salary = em.calculate_salary(employee[0])

    # Check if the calculated salary is 3600
    assert calculated_salary == 3600


# Make sure that when you calculate the salary and send an email notification,
# the respective email sender service is used with the correct information
# (name and message). You can use the setup from the previous test for the employee.


def check_email_sender():
    rm = RelationsManager()
    em = EmployeeManager(rm)

    # Get all employees
    employees = rm.get_all_employees()

    # Filter the employee by hire date and base salary
    employee = [
        e
        for e in employees
        if e.hire_date == datetime.date(1998, 10, 10) and e.base_salary == 1000
    ]

    #
    print(f"{employee[0].hire_date}")

    # Check if the employee is found and only one employee is found
    assert len(employee) == 1

    # Calculate the salary and send email
    em.calculate_salary_and_send_email(employee[0])

    # Check if the email is sent
    # assert email_sent == True
    # assert email_sender_service == True
    # assert email_sender_service_info == "name and message"
