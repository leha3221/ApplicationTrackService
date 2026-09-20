"""Функции работы с кадровыми заявлениями."""

from datetime import date


REQUEST_TYPES = {
    "1": "Отпуск",
    "2": "Перевод",
    "3": "Увольнение",
    "4": "Прием на работу",
}


def get_type_and_status(choice: str, age: int) -> tuple[str, str]:
    """Определить тип заявления и его начальный статус."""
    request_type = REQUEST_TYPES[choice]

    statuses = {
        "1": "На согласовании у руководителя",
        "2": "На согласовании у HR",
        "3": "На согласовании у HR и руководителя",
        "4": "На регистрации в HR",
    }
    status = statuses[choice]

    if age < 18:
        status = "Отклонено: сотрудник младше 18 лет"
    elif age > 70:
        status = "Требуется дополнительная проверка (возраст > 70)"

    return request_type, status


def get_next_request_id(requests: list[dict]) -> int:
    """Вернуть следующий свободный номер заявления."""
    if not requests:
        return 1
    return max(request["id"] for request in requests) + 1


def create_request(
    requests: list[dict],
    employees: list[dict],
    employee_id: int,
    choice: str,
) -> dict:
    """Создать заявление для существующего сотрудника."""
    employee = next(
        (item for item in employees if item["id"] == employee_id),
        None,
    )
    if employee is None:
        raise ValueError("Сотрудник с таким ID не найден.")

    request_type, status = get_type_and_status(choice, employee["age"])
    request = {
        "id": get_next_request_id(requests),
        "employee_id": employee_id,
        "type": request_type,
        "status": status,
        "date": date.today().isoformat(),
    }
    requests.append(request)
    return request


def cancel_request(requests: list[dict], request_id: int) -> None:
    """Удалить заявление по его номеру."""
    for request in requests:
        if request["id"] == request_id:
            requests.remove(request)
            return
    raise ValueError("Заявление с таким номером не найдено.")


def find_requests(
    requests: list[dict],
    employees: list[dict],
    query: str,
) -> list[dict]:
    """Найти заявления по ФИО, типу или статусу."""
    query = query.lower()
    employee_map = {employee["id"]: employee for employee in employees}
    result = []

    for request in requests:
        employee = employee_map.get(request["employee_id"], {})
        fio = employee.get("fio", "")
        if (
            query in fio.lower()
            or query in request["type"].lower()
            or query in request["status"].lower()
        ):
            result.append(request)

    return result


def sort_requests(requests: list[dict], sort_choice: str) -> list[dict]:
    """Вернуть заявления, отсортированные выбранным способом."""
    keys = {
        "1": lambda request: request["date"],
        "2": lambda request: request["type"],
        "3": lambda request: request["status"],
    }
    return sorted(requests, key=keys[sort_choice])


def get_request_statistics(requests: list[dict]) -> dict[str, int]:
    """Сформировать статистику заявлений по типам."""
    statistics = {request_type: 0 for request_type in REQUEST_TYPES.values()}
    for request in requests:
        statistics[request["type"]] += 1
    return statistics


def show_requests(requests: list[dict], employees: list[dict]) -> None:
    """Вывести заявления на экран."""
    if not requests:
        print("Заявления не найдены.")
        return

    employee_map = {employee["id"]: employee for employee in employees}
    print("\n=== ЗАЯВЛЕНИЯ ===")
    for request in requests:
        employee = employee_map.get(request["employee_id"], {})
        print(
            f"№ {request['id']} | "
            f"ФИО: {employee.get('fio', 'Неизвестно')} | "
            f"Тип: {request['type']} | "
            f"Дата: {request['date']} | "
            f"Статус: {request['status']}"
        )
