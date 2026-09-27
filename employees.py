"""Класс сотрудника и функции работы с коллекцией сотрудников."""


class Employee:
    """Сотрудник организации."""

    def __init__(
        self,
        employee_id: int,
        fio: str,
        department: str,
        age: int,
    ) -> None:
        """Создать объект сотрудника."""
        self.id = employee_id
        self.fio = fio
        self.department = department
        self.age = age

    def __str__(self) -> str:
        """Вернуть строковое представление сотрудника."""
        return (
            f"ID: {self.id} | "
            f"ФИО: {self.fio} | "
            f"Подразделение: {self.department} | "
            f"Возраст: {self.age}"
        )

    def to_dict(self) -> dict:
        """Преобразовать сотрудника в структуру для сохранения в JSON."""
        return {
            "id": self.id,
            "fio": self.fio,
            "department": self.department,
            "age": self.age,
        }

    @classmethod
    def from_data(cls, data: dict) -> "Employee":
        """Создать сотрудника из данных, загруженных из JSON."""
        return cls(
            data["id"],
            data["fio"],
            data["department"],
            data["age"],
        )


def get_next_employee_id(employees: list[Employee]) -> int:
    """Вернуть следующий свободный ID сотрудника."""
    if not employees:
        return 1
    return max(employee.id for employee in employees) + 1


def find_employee_by_id(
    employees: list[Employee],
    employee_id: int,
) -> Employee | None:
    """Найти сотрудника по идентификатору."""
    return next(
        (employee for employee in employees if employee.id == employee_id),
        None,
    )


def add_employee(
    employees: list[Employee],
    employee_id: int,
    fio: str,
    department: str,
    age: int,
) -> Employee:
    """Создать объект сотрудника и добавить его в коллекцию."""
    employee = Employee(employee_id, fio, department, age)
    employees.append(employee)
    return employee


def find_employees(employees: list[Employee], query: str) -> list[Employee]:
    """Найти сотрудников по ФИО или подразделению."""
    query = query.lower()
    return [
        employee
        for employee in employees
        if query in employee.fio.lower()
        or query in employee.department.lower()
    ]


def show_employees(employees: list[Employee]) -> None:
    """Вывести список сотрудников на экран."""
    if not employees:
        print("Сотрудники не найдены.")
        return

    print("\n=== СОТРУДНИКИ ===")
    for employee in employees:
        print(employee)


def sort_employees_by_age(employees: list[Employee]) -> list[Employee]:
    """Вернуть сотрудников, отсортированных по возрасту."""
    return sorted(employees, key=lambda employee: employee.age)
