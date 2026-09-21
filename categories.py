from storage import load_json, save_json


CATEGORIES_FILE = "data/categories.json"


def load_categories(filename: str = CATEGORIES_FILE) -> list[dict]:
    return load_json(filename, [])


def save_categories(
    categories: list[dict],
    filename: str = CATEGORIES_FILE,
) -> None:
    save_json(filename, categories)


def get_category_name(categories: list[dict], code: str) -> str:
    for category in categories:
        if category["code"] == code:
            return category["name"]
    return "Неизвестная категория"


def find_category(categories: list[dict], query: str) -> list[dict]:
    query = query.lower()
    return [
        category
        for category in categories
        if query in category["name"].lower()
    ]


def show_categories(categories: list[dict]) -> None:
    if not categories:
        print("Категории не найдены.")
        return
    print("\n=== КАТЕГОРИИ ЗАЯВЛЕНИЙ ===")
    for category in categories:
        print(f"{category['code']}. {category['name']}")
