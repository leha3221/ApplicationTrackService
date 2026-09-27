"""Функции загрузки и сохранения данных приложения в формате JSON."""

import json

from employees import Employee
from requests import Request


def load_json(filename: str, default: list) -> list:
    """Загрузить список данных из JSON-файла."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON-файл должен содержать список.")
            return data
    except FileNotFoundError:
        return default.copy()
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в файле {filename}.") from error


def save_json(filename: str, data: list) -> None:
    """Сохранить список данных в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_employees(filename: str) -> list[Employee]:
    """Загрузить сотрудников из JSON и создать объекты Employee."""
    raw_employees = load_json(filename, [])
    return [Employee.from_data(item) for item in raw_employees]


def save_employees(filename: str, employees: list[Employee]) -> None:
    """Сохранить сотрудников в JSON."""
    save_json(filename, [employee.to_dict() for employee in employees])


def load_requests(filename: str, employees: list[Employee]) -> list[Request]:
    """Загрузить заявления из JSON, связав их с объектами Employee."""
    raw_requests = load_json(filename, [])
    requests: list[Request] = []
    for item in raw_requests:
        request = Request.from_data(item, employees)
        if request is not None:
            requests.append(request)
    return requests


def save_requests(filename: str, requests: list[Request]) -> None:
    """Сохранить заявления в JSON."""
    save_json(filename, [request.to_dict() for request in requests])
