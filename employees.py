


def get_next_employee_id(employees: list[dict]) -> int:
    """Вернуть следующий свободный идентификатор сотрудника."""
    if not employees:
        return 1
    return max(employee["id"] for employee in employees) + 1


def add_employee(
    employees: list[dict],
    employee_id: int,
    fio: str,
    department: str,
    age: int,
) -> dict:
    
    employee = {
        "id": employee_id,
        "fio": fio,
        "department": department,
        "age": age,
    }
    employees.append(employee)
    return employee


def find_employees(employees: list[dict], query: str) -> list[dict]:
    
    query = query.lower()
    return [
        employee
        for employee in employees
        if query in employee["fio"].lower()
        or query in employee["department"].lower()
    ]


def show_employees(employees: list[dict]) -> None:
    
    if not employees:
        print("Сотрудники не найдены.")
        return

    print("\n=== СОТРУДНИКИ ===")
    for employee in employees:
        print(
            f"ID: {employee['id']} | "
            f"ФИО: {employee['fio']} | "
            f"Подразделение: {employee['department']} | "
            f"Возраст: {employee['age']}"
        )


def sort_employees_by_age(employees: list[dict]) -> list[dict]:
   
    return sorted(employees, key=lambda employee: employee["age"])
