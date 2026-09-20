from employees import add_employee, find_employees, get_next_employee_id


def test_add_employee():
    employees = []
    employee = add_employee(employees, 1, "Иванов Иван", "IT", 25)

    assert employee["fio"] == "Иванов Иван"
    assert len(employees) == 1


def test_find_employees():
    employees = [
        {"id": 1, "fio": "Иванов Иван", "department": "IT", "age": 25}
    ]

    result = find_employees(employees, "иван")

    assert len(result) == 1


def test_next_employee_id():
    employees = [
        {"id": 1, "fio": "Иванов", "department": "IT", "age": 25},
        {"id": 4, "fio": "Петров", "department": "HR", "age": 30},
    ]

    assert get_next_employee_id(employees) == 5
