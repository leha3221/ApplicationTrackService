"""Класс заявления и функции работы с коллекцией заявлений."""

from datetime import date

from employees import Employee, find_employee_by_id


REQUEST_TYPES = {
    "1": "Отпуск",
    "2": "Перевод",
    "3": "Увольнение",
    "4": "Прием на работу",
}


class Request:
    """Кадровое заявление сотрудника."""

    def __init__(
        self,
        request_id: int,
        employee: Employee,
        request_type: str,
        status: str,
        request_date: str,
    ) -> None:
        """Создать объект заявления, связав его с объектом сотрудника."""
        self.id = request_id
        self.employee = employee
        self.type = request_type
        self.status = status
        self.date = request_date

    def __str__(self) -> str:
        """Вернуть строковое представление заявления."""
        return (
            f"№ {self.id} | "
            f"ФИО: {self.employee.fio} | "
            f"Тип: {self.type} | "
            f"Дата: {self.date} | "
            f"Статус: {self.status}"
        )

    @staticmethod
    def resolve_type_and_status(
        choice: str,
        employee_age: int,
    ) -> tuple[str, str]:
        """Определить тип заявления и его начальный статус."""
        request_type = REQUEST_TYPES[choice]

        statuses = {
            "1": "На согласовании у руководителя",
            "2": "На согласовании у HR",
            "3": "На согласовании у HR и руководителя",
            "4": "На регистрации в HR",
        }
        status = statuses[choice]

        if employee_age < 18:
            status = "Отклонено: сотрудник младше 18 лет"
        elif employee_age > 70:
            status = "Требуется дополнительная проверка (возраст > 70)"

        return request_type, status

    def to_dict(self) -> dict:
        """Преобразовать заявление в структуру для сохранения в JSON."""
        return {
            "id": self.id,
            "employee_id": self.employee.id,
            "type": self.type,
            "status": self.status,
            "date": self.date,
        }

    @classmethod
    def from_data(
        cls,
        data: dict,
        employees: list[Employee],
    ) -> "Request | None":
        """Создать заявление из данных JSON, связав его с сотрудником.

        Если сотрудник с указанным ID не найден, заявление
        не создаётся (возвращается None).
        """
        employee = find_employee_by_id(employees, data["employee_id"])
        if employee is None:
            return None
        return cls(
            data["id"],
            employee,
            data["type"],
            data["status"],
            data["date"],
        )


def get_next_request_id(requests: list[Request]) -> int:
    """Вернуть следующий свободный номер заявления."""
    if not requests:
        return 1
    return max(request.id for request in requests) + 1


def create_request(
    requests: list[Request],
    employees: list[Employee],
    employee_id: int,
    choice: str,
) -> Request:
    """Создать заявление для существующего сотрудника."""
    employee = find_employee_by_id(employees, employee_id)
    if employee is None:
        raise ValueError("Сотрудник с таким ID не найден.")

    request_type, status = Request.resolve_type_and_status(
        choice,
        employee.age,
    )
    request = Request(
        get_next_request_id(requests),
        employee,
        request_type,
        status,
        date.today().isoformat(),
    )
    requests.append(request)
    return request


def cancel_request(requests: list[Request], request_id: int) -> None:
    """Удалить заявление по его номеру."""
    for request in requests:
        if request.id == request_id:
            requests.remove(request)
            return
    raise ValueError("Заявление с таким номером не найдено.")


def find_requests(requests: list[Request], query: str) -> list[Request]:
    """Найти заявления по ФИО сотрудника, типу или статусу."""
    query = query.lower()
    return [
        request
        for request in requests
        if query in request.employee.fio.lower()
        or query in request.type.lower()
        or query in request.status.lower()
    ]


def sort_requests(requests: list[Request], sort_choice: str) -> list[Request]:
    """Вернуть заявления, отсортированные выбранным способом."""
    keys = {
        "1": lambda request: request.date,
        "2": lambda request: request.type,
        "3": lambda request: request.status,
    }
    return sorted(requests, key=keys[sort_choice])


def get_request_statistics(requests: list[Request]) -> dict[str, int]:
    """Сформировать статистику заявлений по типам."""
    statistics = {request_type: 0 for request_type in REQUEST_TYPES.values()}
    for request in requests:
        statistics[request.type] += 1
    return statistics


def show_requests(requests: list[Request]) -> None:
    """Вывести заявления на экран."""
    if not requests:
        print("Заявления не найдены.")
        return

    print("\n=== ЗАЯВЛЕНИЯ ===")
    for request in requests:
        print(request)
