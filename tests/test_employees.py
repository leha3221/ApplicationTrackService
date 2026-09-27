from employees import (
    Employee,
    add_employee,
    find_employee_by_id,
    find_employees,
    get_next_employee_id,
)


def test_employee_creation():
    employee = Employee(1, "Иванов Иван", "IT", 25)

    assert employee.id == 1
    assert employee.fio == "Иванов Иван"
    assert employee.department == "IT"
    assert employee.age == 25


def test_employee_str():
    employee = Employee(1, "Иванов Иван", "IT", 25)

    assert str(employee) == (
        "ID: 1 | ФИО: Иванов Иван | "
        "Подразделение: IT | Возраст: 25"
    )


def test_add_employee():
    employees = []
    employee = add_employee(employees, 1, "Иванов Иван", "IT", 25)

    assert employee.fio == "Иванов Иван"
    assert len(employees) == 1
    assert employees[0] is employee


def test_find_employees():
    employees = [Employee(1, "Иванов Иван", "IT", 25)]

    result = find_employees(employees, "иван")

    assert len(result) == 1


def test_find_employee_by_id():
    employees = [Employee(1, "Иванов Иван", "IT", 25)]

    assert find_employee_by_id(employees, 1) is employees[0]
    assert find_employee_by_id(employees, 99) is None


def test_next_employee_id():
    employees = [
        Employee(1, "Иванов", "IT", 25),
        Employee(4, "Петров", "HR", 30),
    ]

    assert get_next_employee_id(employees) == 5
