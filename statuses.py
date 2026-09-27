"""Класс статуса заявления и функции работы со справочником статусов."""

from storage import load_json, save_json


STATUSES_FILE = "data/statuses.json"


class Status:
    """Статус заявления из справочника."""

    def __init__(self, code: str, name: str) -> None:
        """Создать объект статуса."""
        self.code = code
        self.name = name

    def __str__(self) -> str:
        """Вернуть строковое представление статуса."""
        return f"{self.code}. {self.name}"

    def to_dict(self) -> dict:
        """Преобразовать статус в структуру для сохранения в JSON."""
        return {"code": self.code, "name": self.name}

    @classmethod
    def from_data(cls, data: dict) -> "Status":
        """Создать статус из данных, загруженных из JSON."""
        return cls(data["code"], data["name"])


def load_statuses(filename: str = STATUSES_FILE) -> list[Status]:
    """Загрузить статусы из JSON и создать объекты Status."""
    raw_statuses = load_json(filename, [])
    return [Status.from_data(item) for item in raw_statuses]


def save_statuses(
    statuses: list[Status],
    filename: str = STATUSES_FILE,
) -> None:
    """Сохранить статусы в JSON."""
    save_json(filename, [status.to_dict() for status in statuses])


def get_status_name(statuses: list[Status], code: str) -> str:
    """Вернуть название статуса по его коду."""
    for status in statuses:
        if status.code == code:
            return status.name
    return "Неизвестный статус"


def find_status(statuses: list[Status], query: str) -> list[Status]:
    """Найти статусы по названию."""
    query = query.lower()
    return [
        status
        for status in statuses
        if query in status.name.lower()
    ]


def show_statuses(statuses: list[Status]) -> None:
    """Вывести статусы на экран."""
    if not statuses:
        print("Статусы не найдены.")
        return
    print("\n=== СТАТУСЫ ЗАЯВЛЕНИЙ ===")
    for status in statuses:
        print(status)
