from categories import Category, find_category, get_category_name


def test_category_creation():
    category = Category("1", "Отпуск")

    assert category.code == "1"
    assert category.name == "Отпуск"


def test_category_str():
    category = Category("1", "Отпуск")

    assert str(category) == "1. Отпуск"


def test_get_category_name():
    categories = [
        Category("1", "Отпуск"),
        Category("2", "Перевод"),
    ]
    assert get_category_name(categories, "1") == "Отпуск"


def test_get_unknown_category():
    categories = [Category("1", "Отпуск")]
    assert get_category_name(categories, "99") == "Неизвестная категория"


def test_find_category():
    categories = [
        Category("1", "Отпуск"),
        Category("2", "Перевод"),
    ]
    result = find_category(categories, "перев")
    assert len(result) == 1
    assert result[0].code == "2"
