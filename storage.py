"""Загрузка и сохранение данных в JSON."""

import json


def load_json(filename: str, default: list) -> list:
    """Загрузить список из JSON-файла."""
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
    """Сохранить список в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_employees(filename: str) -> list[dict]:
    """Загрузить сотрудников."""
    return load_json(filename, [])


def save_employees(filename: str, employees: list[dict]) -> None:
    """Сохранить сотрудников."""
    save_json(filename, employees)


def load_requests(filename: str) -> list[dict]:
    """Загрузить заявления."""
    return load_json(filename, [])


def save_requests(filename: str, requests: list[dict]) -> None:
    """Сохранить заявления."""
    save_json(filename, requests)
