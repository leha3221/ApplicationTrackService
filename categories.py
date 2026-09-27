"""Класс категории заявления и функции работы со справочником категорий."""

from storage import load_json, save_json


CATEGORIES_FILE = "data/categories.json"


class Category:
    """Категория (тип) заявления из справочника."""

    def __init__(self, code: str, name: str) -> None:
        """Создать объект категории."""
        self.code = code
        self.name = name

    def __str__(self) -> str:
        """Вернуть строковое представление категории."""
        return f"{self.code}. {self.name}"

    def to_dict(self) -> dict:
        """Преобразовать категорию в структуру для сохранения в JSON."""
        return {"code": self.code, "name": self.name}

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать категорию из данных, загруженных из JSON."""
        return cls(data["code"], data["name"])


def load_categories(filename: str = CATEGORIES_FILE) -> list[Category]:
    """Загрузить категории из JSON и создать объекты Category."""
    raw_categories = load_json(filename, [])
    return [Category.from_data(item) for item in raw_categories]


def save_categories(
    categories: list[Category],
    filename: str = CATEGORIES_FILE,
) -> None:
    """Сохранить категории в JSON."""
    save_json(
        filename,
        [category.to_dict() for category in categories],
    )


def get_category_name(categories: list[Category], code: str) -> str:
    """Вернуть название категории по её коду."""
    for category in categories:
        if category.code == code:
            return category.name
    return "Неизвестная категория"


def find_category(categories: list[Category], query: str) -> list[Category]:
    """Найти категории по названию."""
    query = query.lower()
    return [
        category
        for category in categories
        if query in category.name.lower()
    ]


def show_categories(categories: list[Category]) -> None:
    """Вывести категории на экран."""
    if not categories:
        print("Категории не найдены.")
        return
    print("\n=== КАТЕГОРИИ ЗАЯВЛЕНИЙ ===")
    for category in categories:
        print(category)
