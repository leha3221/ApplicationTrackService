from storage import load_json, save_json


STATUSES_FILE = "data/statuses.json"


def load_statuses(filename: str = STATUSES_FILE) -> list[dict]:
    return load_json(filename, [])


def save_statuses(
    statuses: list[dict],
    filename: str = STATUSES_FILE,
) -> None:
    save_json(filename, statuses)


def get_status_name(statuses: list[dict], code: str) -> str:
    for status in statuses:
        if status["code"] == code:
            return status["name"]
    return "Неизвестный статус"


def find_status(statuses: list[dict], query: str) -> list[dict]:
    query = query.lower()
    return [
        status
        for status in statuses
        if query in status["name"].lower()
    ]


def show_statuses(statuses: list[dict]) -> None:
    if not statuses:
        print("Статусы не найдены.")
        return
    print("\n=== СТАТУСЫ ЗАЯВЛЕНИЙ ===")
    for status in statuses:
        print(f"{status['code']}. {status['name']}")
